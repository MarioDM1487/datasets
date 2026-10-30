# Tepore — App multi-prodotto (architettura & ragionamento)

Obiettivo: **una sola app** in cui l'utente sceglie il **prodotto acquistato** e l'app si
configura da sola — numero di sensori, ruoli, logica di comfort, soglie, termini e icona.
Il "cavallo" di oggi diventa **un caso particolare** di un modello più generale.

> ✅ **Stato: implementato** in `tepore.html`. Al primo avvio compare **"Quale prodotto hai
> acquistato?"** con tre profili (Cavallo · Cane · Bambino); la scelta configura sensori,
> ruoli, soglie e termini. Vedi §9 per le soglie usate (indicative, da tarare).

---

## 1. Idea chiave: il "Profilo prodotto"
Oggi l'app ragiona per **cavallo**. Lo generalizziamo in **soggetto** (l'animale/persona
monitorata) + un **profilo prodotto** che definisce tutto il resto.

Un **profilo** descrive:
- **Tipo soggetto**: cavallo 🐎 · cane 🐕 · bambino 👶 · altro ⚙️
- **Sensori**: quanti e con quali **ruoli** (es. *interno*, *esterno*; oppure solo *ambiente*…)
- **Logica di comfort** + **soglie** (può essere diversa per prodotto)
- **Terminologia** ("sotto la coperta" vs "addosso" vs "nella culla") e **icona/colori**
- (futuro) **articolo/SKU** acquistato → preset automatico

## 2. Onboarding guidato dall'acquisto
Nuovo primo avvio:
> **"Quale prodotto hai acquistato?"** → [Coperta cavallo] [Cappottino cane] [Comfort bambino] [Altro]

La scelta imposta **numero di sensori e ruoli**. Poi il wizard di abbinamento assegna i
sensori fisici ai ruoli (con i metodi già pronti: **MAC · 📍 vicinanza · 🌬️ soffio**).
> Futuro: **QR sulla confezione** con i MAC dei sensori → assegnazione **automatica**.

## 3. Profili iniziali (proposta)

| Profilo | Sensori | Logica comfort | Note |
|---|---|---|---|
| **Cavallo — coperta** | 2 (interno + esterno) | **Δ interno−esterno** (attuale: ideale 5–10°C) | già fatto |
| **Cane — cappottino** | 2 (interno + esterno) | Δ interno−esterno, soglie **da tarare** (il cane termoregola diversamente) | indossato col padrone |
| **Cane — solo indossato** | 1 (addosso) | temperatura/umidità del microclima, soglie da definire | versione economica |
| **Bambino — comfort sonno** | 1–2 (addosso + ambiente cameretta) | **soprattutto surriscaldamento** + temperatura ambiente (ideale cameretta ~16–20°C) | ⚠️ vedi §6 |
| **Altro / generico** | scegli tu (1–4) + ruoli | scegli il modello (Δ o assoluto) + soglie | per casi custom/pilota |

> La logica di comfort è **pluggabile per profilo**: oggi le soglie stanno in un unico punto
> (`TH` in `tepore.html`); le spostiamo **dentro il profilo**.

## 4. Modello dati (evoluzione, retro-compatibile)
- `soggetti` (ex `horses`): ognuno con `profilo` (id del prodotto), `nome`, dati anagrafici
  liberi, e `ruoli` = { ruolo → MAC sensore }.
- `profili`: definizione (sensori, ruoli, logica, soglie, testi, icona). Prima **predefiniti
  nel codice**, poi eventualmente scaricabili/aggiornabili.
- **Migrazione**: i cavalli esistenti diventano soggetti con profilo `cavallo-coperta`
  (ruoli interno/esterno già mappati).

## 5. Impatto sull'app (cosa cambia)
- **Onboarding**: schermata "quale prodotto?" prima del primo soggetto.
- **Scheda soggetto**: campi e termini dal profilo (non più fissi "cavallo/coperta").
- **Home/Storico/Avvisi/Sensori**: stessi componenti, ma etichette, numero tessere, numero
  ruoli e **funzione di comfort** presi dal profilo.
- **Comfort**: da `comfort(uT,uH,eT)` unico → `profilo.comfort(letture)` per profilo.
- Il resto (BLE, decodifica HolyIoT, identificazione sensori, multi-soggetto) **resta uguale**.

## 6. ⚠️ Bambini: sicurezza e responsabilità (da decidere PRIMA di vendere)
Un prodotto per neonati tocca sicurezza e aspetti legali. Raccomandazioni:
- Posizionarlo come **ausilio indicativo al comfort**, **NON dispositivo medico** e **NON**
  strumento di prevenzione (niente claim tipo "sonno sicuro"/anti-SIDS).
- **Non deve dare falsa sicurezza**: avvertenza chiara che **non sostituisce la sorveglianza**
  dell'adulto.
- Il rischio rilevante è il **surriscaldamento** (non "va tutto bene"): tarare la logica sul
  **troppo caldo**, con soglie conservative.
- **Verifica legale/normativa** prima del lancio (es. regole su prodotti per l'infanzia e su
  ciò che può sembrare un dispositivo medico). Decisione di prodotto/legale, non tecnica.

## 7. Piano di implementazione (a step)
1. **Introdurre i profili nel codice** (oggetto `PROFILI`) e spostarci dentro soglie +
   terminologia + ruoli, con `cavallo-coperta` = comportamento attuale. *(nessun cambiamento
   visibile, base pronta)*
2. **Onboarding "quale prodotto?"** + migrazione cavalli → soggetti.
3. **Rendere l'UI data-driven dal profilo** (etichette, tessere, ruoli).
4. **Comfort per profilo** (Δ per coperta; modello per bambino/cane da definire).
5. (futuro) **QR confezione** per auto-assegnazione, profili scaricabili.

## 8. Decisioni (prese)
- [x] **Profili attivi subito**: tutti e tre — cavallo, cane, bambino.
- [x] **Cane**: **1 sensore** (cappottino, "addosso"), logica **assoluta** sul microclima.
- [x] **Bambino**: lo sviluppiamo ora, ma **solo informazione temperatura** — **NON** dispositivo
      medico, con disclaimer in app. Verifiche legali in corso prima della vendita.
- [x] **Identificazione sensori**: come oggi — **📍 vicinanza** e **🌬️ soffio** (niente QR per ora).
- [x] **Soglie cane/bambino**: valori iniziali da riferimenti online (vedi §9), **da affinare**
      con veterinario / pediatra.

## 9. Soglie implementate (indicative — da tarare)
| Profilo | Modello | Soglie |
|---|---|---|
| **Cavallo — coperta** | Δ interno−esterno | freddo <2° · fresco 2–5° · **ideale 5–10°** · caldo 10–13° · sudore >13° o Δ>10° con umidità ≥80% |
| **Cane — cappottino** | assoluto (microclima sotto il capo) | freddo <18° · fresco 18–24° · **ideale 24–32°** · caldo 32–36° · troppo caldo >36° |
| **Bambino — cameretta** | assoluto (temperatura ambiente) | freddo <16° · fresco 16–18° · **ideale 18–21°** · caldo 21–23° · troppo caldo >23° |

> Riferimenti: cameretta ideale ~18–21 °C (NHS / Lullaby Trust citano 16–20 °C in chiave
> anti-surriscaldamento). Il cane/microclima **non ha uno standard**: le soglie "addosso" sono
> stime prudenziali da validare. Le soglie stanno **dentro il profilo** (`PROFILI` in `tepore.html`),
> quindi si cambiano in un punto solo.

## 10. Da fare ancora
- [ ] Validazione soglie con **veterinario / pediatra**.
- [ ] (futuro) **QR sulla confezione** coi MAC → auto-assegnazione sensori.
- [ ] Profilo **"Altro / generico"** (scegli sensori + modello) se servirà per casi pilota.
- [ ] Terminologia/anagrafica per cane e bambino: oggi la scheda riusa i campi base; si possono
      specializzare ulteriormente.
