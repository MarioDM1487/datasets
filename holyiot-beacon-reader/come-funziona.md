# MANTO — Come funziona

> **Il comfort termico del cavallo, in un colpo d'occhio.**
> Documento di presentazione del sistema per chi lo mostra e lo vende.

---

## Il problema
D'inverno il cavallo va tenuto **al caldo giusto** con la coperta. Ma "giusto" è difficile da
valutare a mano:
- **Troppo poco** → l'animale ha freddo, spreca energie, si ammala.
- **Troppo** → **suda sotto la coperta**, e il sudore poi lo **raffredda** (effetto peggiore del
  freddo di partenza).

Oggi il proprietario tocca il torace con la mano e "va a sensazione", spesso di notte o quando
non è in scuderia. Nessun dato, nessuno storico, nessun avviso.

## La soluzione: MANTO
Due piccoli sensori Bluetooth e un'app sul telefono:
- un sensore **interno**, sotto la coperta (misura il microclima a contatto con l'animale);
- un sensore **esterno**, che misura l'ambiente.

L'app confronta i due e dice, in parole semplici, **se il cavallo sta al caldo giusto** —
con avvisi quando serve e uno storico dell'andamento.

---

## Come funziona (il cuore: il Δ)
Ciò che conta **non** è la temperatura assoluta, ma **quanto la coperta scalda l'animale
rispetto all'esterno**: la **differenza interno − esterno** (il "Δ").

Una coperta che funziona tiene l'animale **5–10 °C più caldo** dell'ambiente. Sotto, scalda
poco; molto sopra (e con umidità alta), l'animale suda.

| Δ (interno − esterno) | Stato | Cosa significa |
|---|---|---|
| < 2 °C | 🔵 **Troppo freddo** | la coperta non sta scaldando |
| 2 – 5 °C | 🔵 Fresco | isolamento un po' scarso |
| **5 – 10 °C** | 🟢 **Ideale** | al caldo giusto |
| 10 – 13 °C | 🟠 Caldo | si scalda troppo |
| > 13 °C, oppure > 10 °C con umidità ≥ 80% | 🔴 **Sudorazione** | rischio sudore |

> Le soglie sono **indicative** e si tarano facilmente per razza, coperta e clima, insieme al
> veterinario.

---

## Le schermate

### 🏠 Oggi
La schermata principale: **stato in parole** ("Al caldo", "Troppo freddo"…), una **barra**
Freddo → Ideale → Sudore con l'indicatore, e le tessere con **Interno**, **Esterno**,
**Δ isolamento** e **umidità**. Basta uno sguardo.

### 📈 Storico
L'andamento nel tempo di interno ed esterno, la **percentuale di tempo in comfort** e il Δ
medio. Utile per capire se la coperta scelta è adatta a quel cavallo.

### 🔔 Avvisi
L'elenco degli eventi importanti: quando l'animale è andato **troppo freddo** o in
**sudorazione**, con orario e valori. Così non serve guardare di continuo.

### 🐎 Cavalli
Più cavalli, ognuno con la sua **scheda** (razza, peso, coperta, box) e i **suoi sensori**
(Interno/Esterno, identificati dal **MAC**). Si aggiungono, modificano ed eliminano.

### 📡 Sensori
L'abbinamento. Ogni sensore mostra il suo **indirizzo MAC**, la temperatura e il segnale.
Bastano due tap per assegnarlo come **Interno** o **Esterno**, e c'è il tasto **Scollega**.

---

## Identificare i sensori (senza lampeggio)
Con più sensori identici davanti, come si capisce qual è quale? Tre modi, tutti nell'app:
1. **MAC** — ogni sensore mostra il suo indirizzo (come sull'etichetta / app ufficiale).
2. **📍 Vicinanza** — avvicini un sensore al telefono e viene evidenziato come "più vicino".
3. **🌬️ Soffio** — soffi sul sensore 2 secondi: l'umidità sale e appare "**questo!**".

---

## Copione demo (2 minuti)
Per mostrarlo dal vivo a un cliente:
1. Apri l'app → tab **Sensori** → **Avvia monitoraggio**. Compaiono i sensori col loro **MAC**.
2. **Soffia** su un sensore: si evidenzia → assegnalo **Interno**. Assegna l'altro **Esterno**.
3. Vai su **Oggi**: mostra lo stato e il **Δ**.
4. **Scalda un sensore in mano** (o mettilo vicino a una fonte di calore): il Δ sale, la barra
   si sposta verso "Ideale" e poi "Sudore". → *Ecco: l'app reagisce in tempo reale.*
5. Mostra **Cavalli** (più animali) e **Avvisi**.

Messaggio chiave da lasciare: **"Sai sempre se il tuo cavallo sta al caldo giusto — anche
quando non sei in scuderia."**

---

## Punti di forza (per il cliente)
- **Semplice**: nessun numero da interpretare, l'app dice come sta l'animale.
- **Benessere**: previene sia il freddo sia la sudorazione (spesso sottovalutata).
- **Multi-cavallo**: un'app per tutta la scuderia.
- **Concreto**: dati, storico e avvisi al posto del "a sensazione".

## Stato attuale e prossimi passi
- ✅ **Web app** funzionante su **Android** (Chrome).
- ▶️ **App Android** installabile (in arrivo) e **iPhone** (app nativa).
- 🗓️ **Gateway in stalla** per il monitoraggio **24 ore su 24** e storico continuo.
- 🐕 Variante per **cani** (stessa tecnologia).

## In breve, come funziona la tecnologia
I sensori (beacon Bluetooth) **trasmettono** temperatura e umidità in continuo; l'app li
**ascolta** e calcola il comfort. Nessuna connessione da configurare, nessuna password.
Semplice e affidabile.

---

*Documento dimostrativo. Le soglie di comfort sono indicative e vanno tarate con il veterinario.*
