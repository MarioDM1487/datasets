# Tepore — App multi-prodotto (architettura & ragionamento)

Obiettivo: **una sola app** in cui l'utente sceglie il **prodotto acquistato** e l'app si
configura da sola — numero di sensori, ruoli, logica di comfort, soglie, termini e icona.
Il "cavallo" di oggi diventa **un caso particolare** di un modello più generale.

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

## 8. Decisioni aperte (mi servono per procedere bene)
- [ ] Quali **profili** attiviamo subito? (cavallo è fatto; cane sì/no ora; bambino sì/no/dopo)
- [ ] Per il **cane**: 1 o 2 sensori? indossato con cappottino (Δ) o solo microclima?
- [ ] Per il **bambino**: lo affrontiamo ora (con cautele e verifica legale) o lo teniamo come
      profilo "in valutazione"?
- [ ] I prodotti venduti avranno un **QR coi MAC** sulla confezione? (abilita l'auto-assegnazione)
- [ ] Soglie **cane/bambino**: chi le valida (veterinario / pediatra)?

> Quando rispondi a queste, parto con lo **step 1** (profili nel codice) che non cambia nulla
> di visibile ma prepara tutto il resto.
