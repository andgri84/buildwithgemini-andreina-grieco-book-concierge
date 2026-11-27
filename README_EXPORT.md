# Andreina Grieco - Book Concierge & Store (Pacchetto Completo)

Questo pacchetto contiene tutto il codice sorgente, i database, le immagini ad alta risoluzione e la documentazione del progetto pronto per essere eseguito o deployato su qualsiasi piattaforma.

---

## 📦 Contenuto del Pacchetto

1. **`frontend/`**
   - `static/index.html`: La Web App completa (Showcase Libri, Box Autografate, Modulo d'Ordine con calcolo spese di spedizione automatico, Chat Concierge integrata).
   - `main.py`: Backend proxy FastAPI con endpoint `/api/catalog`, `/api/order` e `/chat` (A2A).
   - `requirements.txt`: Dipendenze Python necessarie.

2. **`book-concierge/`**
   - `app/agent.py`: Definizione dell'agente ADK (Google Agent Development Kit).
   - `app/tools.py`: I function tools per l'agente (lettura libri, box, calcolo spedizioni e scrittura ordini).
   - `app/catalog.py`: Fallback statico del catalogo.
   - `seed_firestore.py`: Script originale di inizializzazione database.
   - `covers/`: Copertine originali ad alta risoluzione.
   - `thumbnails/`: Miniature ottimizzate a 300px per il web.

3. **Database Firestore (`firestore_export.json` & `import_firestore.py`)**
   - `firestore_export.json`: Dump completo in formato JSON di tutte le collezioni:
     - `catalog_books`: I romanzi con sinossi, generi, ambientazioni e URL immagini.
     - `catalog_boxes`: Le 6 tipologie di box autografate con le card incluse e le formule prezzi.
     - `book_orders`: Gli ordini registrati.
   - `import_firestore.py`: Script automatico per re-importare l'intero database in un altro progetto Google Cloud.

4. **`project_brief.md`**
   - Documento di specifica e requisiti del progetto (prezzi, formule Vinted, regole di dedica e logistica).

---

## 🚀 Come Eseguire Localmente

### 1. Avviare il Frontend Web
```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
Apri il browser su: `http://localhost:8080`

---

## ☁️ Come Importare il Database su un Altro Account GCP
Assicurati di aver configurato il nuovo progetto con `gcloud config set project <NUOVO_PROJECT_ID>` e abilitato Firestore:
```bash
pip install google-cloud-firestore
export GOOGLE_CLOUD_PROJECT="<NUOVO_PROJECT_ID>"
python import_firestore.py
```
