#!/usr/bin/env python3
"""Tepore gateway — legge i beacon BLE HolyIoT in stalla e invia le letture online.

Gira su un dispositivo sempre acceso con Bluetooth (es. Raspberry Pi) e fa:
  1. scansione passiva degli advertisement BLE (nessuna connessione ai sensori);
  2. decodifica HolyIoT-25015 (temperatura, umidità, pressione) + MAC;
  3. invio periodico delle letture a un endpoint HTTP configurabile (backend cloud).

È volutamente "stupido": manda letture per MAC. La mappatura MAC -> cavallo
(interno/esterno) resta nell'app. Endpoint e token si impostano in config.json.

Setup rapido (Raspberry Pi OS):
    sudo apt install -y python3-pip bluetooth
    pip3 install -r requirements.txt
    cp config.example.json config.json   # poi modifica endpoint/token/gateway_id
    python3 tepore_gateway.py --config config.json
Vedi README.md per l'esecuzione come servizio (systemd) all'avvio.
"""
from __future__ import annotations

import argparse
import json
import logging
import signal
import time
from typing import Optional

import requests
from bleak import BleakScanner

HOLYIOT_COMPANY_ID = 0xFFFF          # manufacturer id dei beacon HolyIoT
DEVINFO_SERVICE_SUFFIX = "180a"      # service data che contiene il MAC

log = logging.getLogger("tepore-gateway")


def decode_holyiot(company_id: int, data: bytes) -> Optional[dict]:
    """Decodifica i manufacturer data HolyIoT. Ritorna {temp,hum} o {pressure} o None."""
    if company_id != HOLYIOT_COMPANY_ID or not data:
        return None
    # scarta un eventuale frame iBeacon (0x02 0x15 ...)
    if len(data) >= 23 and data[0] == 0x02 and data[1] == 0x15:
        return None
    if len(data) == 7:  # [counter][temp int16 BE][hum int16 BE]
        temp = int.from_bytes(data[1:3], "big", signed=True) / 10.0
        hum = int.from_bytes(data[3:5], "big", signed=True) / 10.0
        return {"temp": round(temp, 1), "hum": round(hum, 1)}
    if len(data) == 5:  # [counter][pressure 24 bit]
        pressure = ((data[1] << 16) | (data[2] << 8) | data[3]) / 100.0
        return {"pressure": round(pressure, 2)}
    return None


def mac_from_service_data(service_data: dict) -> Optional[str]:
    """Estrae il MAC dai service data 0x180A: [counter][MAC 6 byte][...]."""
    for uuid, raw in (service_data or {}).items():
        if str(uuid).lower().find(DEVINFO_SERVICE_SUFFIX) != -1 and len(raw) >= 7:
            return ":".join(f"{b:02X}" for b in raw[1:7])
    return None


class Readings:
    """Ultima lettura per ogni MAC, in memoria."""

    def __init__(self) -> None:
        self._by_mac: dict[str, dict] = {}

    def update(self, mac: str, fields: dict, rssi: Optional[int]) -> None:
        r = self._by_mac.setdefault(mac, {"mac": mac})
        r.update(fields)
        if rssi is not None:
            r["rssi"] = rssi
        r["ts"] = int(time.time() * 1000)

    def snapshot(self) -> list[dict]:
        return [dict(r) for r in self._by_mac.values()]


def make_callback(readings: Readings):
    def callback(device, adv) -> None:
        mac = mac_from_service_data(getattr(adv, "service_data", {})) or getattr(device, "address", None)
        if not mac:
            return
        mac = mac.upper()
        fields: dict = {}
        for cid, data in (getattr(adv, "manufacturer_data", {}) or {}).items():
            decoded = decode_holyiot(cid, bytes(data))
            if decoded:
                fields.update(decoded)
        if not fields:
            return  # advertisement non nostro / senza dati utili
        readings.update(mac, fields, getattr(adv, "rssi", None))
    return callback


def post_readings(cfg: dict, items: list[dict]) -> None:
    if not items:
        return
    payload = {"gateway_id": cfg["gateway_id"], "readings": items}
    headers = {"Content-Type": "application/json"}
    token = cfg.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.post(cfg["endpoint"], json=payload, headers=headers, timeout=15)
        if resp.status_code // 100 == 2:
            log.info("inviate %d letture -> %s", len(items), resp.status_code)
        else:
            log.warning("endpoint ha risposto %s: %s", resp.status_code, resp.text[:200])
    except requests.RequestException as exc:
        log.warning("invio fallito (riprovo al prossimo ciclo): %s", exc)


async def run(cfg: dict) -> None:
    import asyncio

    readings = Readings()
    scanner = BleakScanner(detection_callback=make_callback(readings))
    await scanner.start()
    log.info("gateway '%s' avviato — scansione BLE attiva", cfg["gateway_id"])
    stop = asyncio.Event()

    def _stop(*_a):
        stop.set()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _stop)
        except ValueError:
            pass  # non nel thread principale

    interval = float(cfg.get("post_interval_s", 30))
    try:
        while not stop.is_set():
            try:
                await asyncio.wait_for(stop.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass
            post_readings(cfg, readings.snapshot())
    finally:
        await scanner.stop()
        log.info("gateway fermato")


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    for key in ("endpoint", "gateway_id"):
        if not cfg.get(key):
            raise SystemExit(f"config: manca il campo obbligatorio '{key}'")
    return cfg


def main() -> None:
    ap = argparse.ArgumentParser(description="Tepore BLE -> cloud gateway")
    ap.add_argument("--config", default="config.json", help="percorso del file di configurazione")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    cfg = load_config(args.config)
    import asyncio
    asyncio.run(run(cfg))


if __name__ == "__main__":
    main()
