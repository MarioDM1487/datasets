# Tepore Gateway (stalla → cloud)

Dispositivo sempre acceso in stalla che legge i sensori BLE HolyIoT 24/7 e invia le letture
online, così l'app mostra il cavallo **anche quando non sei presente**.

```
Sensori BLE  →  Gateway (Raspberry Pi, WiFi)  →  Cloud (backend)  →  App/Web (ovunque)
```

Il gateway è volutamente semplice: invia letture **per MAC**. La mappatura MAC → cavallo
(interno/esterno) resta nell'app.

## Hardware consigliato
- **Raspberry Pi** con WiFi + Bluetooth (es. **Pi Zero 2 W**, ~15€, o Pi 3/4).
- Alimentatore, microSD con **Raspberry Pi OS**.
- (In futuro: versione **ESP32** più economica per la produzione.)

## Installazione (Raspberry Pi OS)
```bash
sudo apt update && sudo apt install -y python3-pip bluetooth
git clone <questo-repo> && cd gateway         # oppure copia la cartella gateway/
pip3 install -r requirements.txt
cp config.example.json config.json            # poi modifica i campi (sotto)
python3 tepore_gateway.py --config config.json --verbose
```

### Configurazione (`config.json`)
| Campo | Descrizione |
|---|---|
| `gateway_id` | nome della postazione (es. `"stalla-nord-1"`) |
| `endpoint` | URL del backend a cui inviare le letture (POST) |
| `token` | token di scrittura (Authorization: Bearer) — opzionale finché non c'è il backend |
| `post_interval_s` | ogni quanti secondi inviare (default 30) |

### Avvio automatico all'accensione (systemd)
```bash
sudo cp tepore-gateway.service /etc/systemd/system/
# adatta User/percorsi dentro il file se non usi l'utente 'pi'
sudo systemctl daemon-reload
sudo systemctl enable --now tepore-gateway
journalctl -u tepore-gateway -f     # log in tempo reale
```

## Contratto dati (cosa invia il gateway)
`POST <endpoint>` con header `Authorization: Bearer <token>` e corpo JSON:
```json
{
  "gateway_id": "stalla-nord-1",
  "readings": [
    { "mac": "EB:19:FB:C0:84:F0", "ts": 1731325000000, "temp": 26.3, "hum": 45.0, "rssi": -50 },
    { "mac": "AA:BB:CC:DD:EE:FF", "ts": 1731325000000, "temp": 5.1,  "hum": 70.0, "rssi": -63 }
  ]
}
```
- `ts` = epoch in millisecondi. `temp` °C, `hum` %, `pressure` hPa (quando presente), `rssi` dBm.
- Campi assenti = non disponibili in quel momento.
- Il backend dovrebbe salvare **ultimo valore** e **storico** per `mac`, ed esporre in lettura
  (es. `GET /latest?mac=...`, `GET /history?mac=...&from=...`).

## Stato
- [x] Software gateway (scansione + decodifica + invio configurabile)
- [ ] Backend cloud (da scegliere: servizio gestito o server nostro)
- [ ] Lettura remota nell'app (modalità "cloud" quando non si è in stalla)
