# HolyIoT Beacon Reader

Webapp per leggere i beacon **BLE HolyIoT** dal telefono, usando la **Web Bluetooth API**.
Mostra tutto ciò che il beacon trasmette (RSSI, indirizzo, manufacturer/service data in
hex) e decodifica i formati noti:

- **iBeacon** — UUID, major, minor, potenza Tx
- **Eddystone** — URL, UID, e **TLM** (batteria in mV, temperatura in °C, uptime)
- **Sensori** — decoder best-effort dei manufacturer data + dump hex per mappare il
  formato esatto del tuo modello (temperatura / pressione / umidità / batteria)

## Requisiti (importante)

| Piattaforma | Funziona? | Note |
|---|---|---|
| **Android + Chrome** | ✅ Sì | Serve attivare un flag (sotto) |
| **iPhone / Safari** | ❌ No | Web Bluetooth non è supportato da Apple |
| iPhone con [Bluefy](https://apps.apple.com/app/bluefy/id1492822055) | ⚠️ Parziale | Browser BLE di terze parti |

La pagina **deve essere servita in HTTPS** (Web Bluetooth non funziona su `http://` né
aprendo il file locale). GitHub Pages va benissimo.

## Uso su Android

1. Apri in Chrome: `chrome://flags/#enable-experimental-web-platform-features`
   → imposta su **Enabled** e riavvia Chrome.
2. Attiva **Bluetooth** e **Localizzazione** (Android richiede la posizione per lo scan BLE).
3. Apri la webapp in HTTPS (URL GitHub Pages) e premi **Avvia scansione**.
4. Concedi il permesso Bluetooth. Avvicina il beacon: comparirà nella lista con RSSI live.

> Puoi installarla in home (menu Chrome → *Installa app*) per usarla a schermo intero.

## iPhone

Su iPhone nessuna webapp può leggere i beacon (limite di Safari/iOS). Opzioni:
- browser **Bluefy** (WebBLE) — apre questa stessa pagina;
- oppure un'app **nativa** (Swift + CoreBluetooth / CoreLocation) — passo successivo.

## Decodifica dei dati sensore

Il layout dei manufacturer data cambia da modello a modello HolyIoT. La webapp mostra la
riga `Manufacturer 0x…` in esadecimale: copiala e la mappiamo sui campi reali
(temperatura, pressione, batteria) per il tuo dispositivo specifico.
