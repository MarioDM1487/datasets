# Tepore — Comfort Cavallo (HolyIoT Beacon Reader)

App che legge i sensori **BLE HolyIoT** e monitora il **comfort termico** di un animale
sotto **coperta riscaldante**: non troppo freddo, non in sudorazione. Nasce per i **cavalli**
🐎 (in prospettiva anche **cani** 🐕).

- **Web app** (Android/Chrome, Web Bluetooth): `tepore.html`
- **App Android nativa** (Capacitor): progetto in `../tepore-app/`, APK compilato in cloud
- `manto.html` è il vecchio nome e reindirizza a `tepore.html` (i dati restano: stesso dominio)

> Nota storica: il progetto è nato come "monitor stress da caldo" (vedi `index.html`, tool di
> sviluppo). Oggi la logica è **ribaltata**: con la coperta l'obiettivo è **tenere l'animale
> più caldo dell'esterno** della giusta quantità.

## Come funziona (in breve)

Due sensori per ogni cavallo:
- **🩺 Interno** — sotto la coperta, misura il microclima a contatto con l'animale
  (temperatura + umidità);
- **🌡️ Esterno** — misura l'ambiente (uno per coperta).

L'app calcola il **Δ = interno − esterno**: quanto la coperta scalda l'animale rispetto
all'ambiente. È questo, non la temperatura assoluta, a dire se l'animale sta bene.

Per una spiegazione discorsiva e orientata alla presentazione/vendita vedi
[`come-funziona.md`](come-funziona.md).

## Soglie di comfort (Δ = interno − esterno)

Definite in un unico punto del codice (`tepore.html`, oggetto `TH`):

```js
const TH = { dFreddo: 2, dFresco: 5, dIdeale: 10, dCaldo: 13, humSweat: 80 };
```

| Δ (interno − esterno)                         | Stato               | Significato                     |
|-----------------------------------------------|---------------------|---------------------------------|
| **< 2 °C**                                    | 🔵 Troppo freddo    | la coperta non sta scaldando    |
| **2 – 5 °C**                                  | 🔵 Fresco           | isolamento un po' scarso        |
| **5 – 10 °C**                                 | 🟢 **Ideale**       | al caldo giusto                 |
| **10 – 13 °C**                                | 🟠 Caldo            | si scalda troppo                |
| **> 13 °C**, oppure **> 10 °C con umidità ≥ 80%** | 🔴 Sudorazione  | rischio sudore                  |

Regole precise applicate dal codice:
- **Sudorazione** se `Δ > 13` **oppure** (`Δ > 10` **e** umidità interna `≥ 80%`);
- altrimenti **Caldo** se `Δ > 10`;
- **Ideale** se `5 ≤ Δ ≤ 10`;
- **Fresco** se `2 ≤ Δ < 5`;
- **Troppo freddo** se `Δ < 2`.

Servono **entrambi** i sensori (interno + esterno): senza l'esterno il Δ non è calcolabile e
la Home lo segnala.

> ⚠️ Le soglie sono **indicative**, da tarare con un veterinario per razza, coperta e clima.
> Per cambiarle basta modificare l'oggetto `TH`.

## Funzioni dell'app

- **Oggi** — stato in parole, barra Freddo→Ideale→Sudore, tessere Interno/Esterno/Δ/umidità
- **Storico** — andamento interno vs esterno, % di tempo in comfort, Δ medio (campiona ogni
  30″ mentre l'app è aperta)
- **Avvisi** — eventi di *Troppo freddo* / *Sudorazione* con orario e valori
- **Cavalli** — più animali, ognuno con scheda e i **suoi** due sensori (con MAC), + Scollega
- **Sensori** — abbinamento; identificazione senza lampeggio: **MAC**, **📍 vicinanza**
  (avvicina al telefono), **🌬️ soffio** (l'umidità sale → "questo!")

## Sensore: cosa viene decodificato

- **HolyIoT-25015** — temperatura (SHT40), umidità, **pressione** (LPS22HB) e **MAC**,
  letti direttamente dall'**advertisement** (nessuna connessione né password). Il MAC è
  estratto dal service data `0x180A` (Web Bluetooth nasconde il MAC hardware).
- Il tool di sviluppo `index.html` legge anche iBeacon, Eddystone (TLM), Govee H5075 e la
  batteria via GATT — utile per il debug, non necessario all'app.

## Piattaforme

| Piattaforma | Web app (`tepore.html`) | App nativa (APK) |
|---|---|---|
| **Android + Chrome** | ✅ (serve il flag, sotto) | ✅ consigliata (Bluetooth nativo, niente flag) |
| **iPhone / Safari** | ❌ Web Bluetooth non supportato | ▶️ prossimo passo (Capacitor + sideload) |

### Web app su Android
1. Chrome: `chrome://flags/#enable-experimental-web-platform-features` → **Enabled**, riavvia.
2. Attiva **Bluetooth** e **Localizzazione** (Android richiede la posizione per lo scan BLE).
3. Apri la pagina in **HTTPS** (GitHub Pages) → tab **Sensori** → **Avvia monitoraggio**.

### App Android nativa (APK)
Non serve Mac né account: la build è nel cloud (GitHub Actions), vedi `../tepore-app/` e il
workflow `.github/workflows/android.yml`. L'APK si scarica dagli **Artifacts** della build e
si installa direttamente (consenti "installa app sconosciute"). Concedi i permessi
**Bluetooth** al primo avvio (e **Posizione** su Android più vecchi).

## Struttura dei file

| File | Cosa |
|---|---|
| `tepore.html` | l'app (unico file: HTML+CSS+JS, con commenti) |
| `tepore.webmanifest` | manifest PWA di Tepore |
| `manto.html` | redirect al nuovo nome (Tepore) |
| `index.html` | tool di sviluppo grezzo (debug beacon) |
| `come-funziona.md` | come funziona, per capire/presentare |
| `brand-brief.md` | marchio: nome, colori, logo |
| `../tepore-app/` | progetto Capacitor per l'APK Android |

> Le soglie di comfort sono indicative e vanno tarate con il veterinario.
