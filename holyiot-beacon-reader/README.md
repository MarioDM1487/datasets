# Monitor Salute Animale (HolyIoT Beacon Reader)

Webapp per leggere i beacon **BLE HolyIoT** dal telefono (**Web Bluetooth API**) e
monitorare lo **stress da caldo** di un animale che indossa il sensore. Base del progetto
(Fase 1) per cavalli 🐎 e cani 🐕.

## Funzioni sensore

- **HolyIoT-25015** — temperatura (SHT40), umidità, **pressione** (LPS22HB), decodificati
  dall'advertisement (senza connessione né password)
- **iBeacon** — UUID, major, minor, potenza Tx
- **Eddystone** — URL, UID, e **TLM** (batteria in mV, temperatura in °C, uptime)
- **Govee H5075** — temperatura / umidità / batteria
- Lettura **batteria** via connessione GATT
- **Pausa** (congela la vista) e **📋 Copia** (hex negli appunti) per il debug

## Monitor salute (Fase 1)

- Profili per **specie** (cavallo / cane) con soglie indicative
- Assegnazione dei due sensori: **🩺 Corpo** (indossato) e **🌡️ Ambiente** (gemello)
- **Indice di stress da caldo**: Heat Index equino (°F+UR) per il cavallo, THI per il cane
- **Δ corpo−ambiente** come carico termico dell'animale
- **Allarme "troppo caldo"** con avviso visivo + beep

> ⚠️ Le soglie sono **indicative**, da tarare con un veterinario.

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
