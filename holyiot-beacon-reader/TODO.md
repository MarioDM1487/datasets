# Tepore — Cose da fare (TODO / Roadmap)

Stato: **web app + APK Android funzionanti** (comfort su Δ interno−esterno, multi-cavallo,
abbinamento sensori, storico/avvisi in-app, crea/elimina cavallo con setup iniziale).
Elenco di ciò che manca o si può migliorare.

## 🔜 Prossimo / facile
- [ ] **Logo cavallo** al posto dell'icona provvisoria "T" dorata → serve il **PNG** (quadrato ≥512px, sfondo trasparente o scuro). Poi lo metto come icona app + logo in alto.
- [ ] **Download APK senza login** → pubblicare l'APK come **GitHub Release** (link diretto, comodo da installare/condividere; ora serve l'account GitHub per gli Artifacts).
- [ ] **Allineare i documenti a Tepore**: `brand-brief.md` cita ancora "MANTO come frontrunner"; `come-funziona.md` ok ma si può rifinire.
- [ ] **Conferma branding**: TEPORE = brand per **cani + cavalli**; per l'app cavalli si usa il marchio **cavallo+coperta**.

## 📱 App / piattaforme
- [ ] **iPhone**: stesso progetto Capacitor → build cloud (macOS) + **sideload** con Sideloadly (Apple ID gratuito). Nota: monitoraggio solo con app aperta; background molto limitato su iOS.
- [ ] **Monitoraggio in background su Android** (foreground service) per tenere la lettura attiva ad app chiusa/schermo spento.
- [ ] **Notifiche push** (avviso freddo/sudore anche ad app chiusa) → richiede nativo/gateway/server.
- [ ] **Nome/etichetta app** e rifiniture icona (splash screen, ecc.).

## 🌡️ Funzioni prodotto
- [ ] **Soglie tarate col veterinario** (ora indicative): Δ 2/5/10/13 °C, umidità 80%. Eventualmente **per specie/razza/coperta**.
- [ ] **Storico continuo H24 + conservazione (24h / 7 giorni)** → arriverà col **gateway Raspberry** in stalla (la web/app registra solo mentre è aperta).
- [ ] **Storico**: scelta intervallo (24h/7g), export dati (CSV?).
- [ ] **Avvisi**: cronologia più ricca, soglie personalizzabili, suoni/vibrazione.
- [ ] **Batteria sensore** mostrata in app (ora non nell'advertisement; via GATT o modello sensore).

## 🏗️ Infrastruttura / futuro
- [ ] **Gateway in stalla** (Raspberry) per lettura 24/7 e storico su server.
- [ ] **Variante cani** 🐕 (stessa tecnologia, logica indossata col padrone).
- [ ] Eventuale **backend/cloud** per sincronizzare più dispositivi e conservare lo storico.

## ✅ Fatto (per riferimento)
- Decodifica beacon **HolyIoT-25015** (temp/umidità/pressione + MAC da service 0x180A)
- Web app + **rebrand MANTO → Tepore**
- Comfort su **Δ interno−esterno** con soglie esplicite
- **Multi-cavallo**, scheda, crea/modifica/**elimina** (+ setup iniziale, fix crash zero cavalli)
- Identificazione sensori: **MAC · 📍 vicinanza · 🌬️ soffio**, tasto **Scollega**
- **APK Android** nativo (Capacitor + plugin BLE), **build cloud** (GitHub Actions), **firma fissa**
- Documenti: `README.md`, `come-funziona.md`, `brand-brief.md`
