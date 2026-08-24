# ✈️ FlyRent - Smart Working Rental Tracker

**FlyRent** è un'applicazione web moderna concepita per Smart Worker e Nomadi Digitali per tracciare, valutare e confrontare appartamenti in affitto a breve e medio termine in tutta Italia (da annunci Facebook, Subito, Idealista, Immobiliare, ecc.).

---

## 🛠️ Tecnologie Utilizzate

* **Frontend**: Vue 3 (`<script setup lang="ts">`), Vue Router, Vite, Tailwind CSS, Lucide Icons.
* **Backend**: Python 3.11, FastAPI, Pydantic v2, Motor (Async MongoDB Driver), Bcrypt & PyJWT per autenticazione JWT.
* **Database**: MongoDB Atlas Cloud.
* **Orchestrazione**: Docker & Docker Compose (Nginx Web Server + Uvicorn FastAPI Server).

---

## 🚀 Come Far Partire l'Applicazione

### Metodo 1: Avvio Rapido con Docker Compose (Consigliato per qualsiasi PC)

1. **Requisiti**: Assicurati di avere installato [Docker Desktop](https://www.docker.com/products/docker-desktop/) e che sia in esecuzione.
2. **Clona il repository**:
   ```bash
   git clone https://github.com/Lowell130/flyrent.git
   cd flyrent
   ```
3. **Verifica il file `.env`**:
   Crea o imposta il file `.env` nella radice del progetto fornendo la tua stringa di connessione MongoDB:
   ```env
   MONGO_URI=mongodb+srv://<USERNAME>:<PASSWORD>@cluster0.mongodb.net/flyrent
   SECRET_KEY=flyrent-super-secret-jwt-key-2026
   ```
4. **Avvia il progetto**:
   ```bash
   docker compose up --build -d
   ```
5. **Apri nel browser**:
   * 🌐 **Landing Page & App**: [http://localhost:3000](http://localhost:3000)
   * 🔐 **Login & Registrazione**: [http://localhost:3000/login](http://localhost:3000/login)
   * 📚 **Documentazione API Interattiva (Swagger)**: [http://localhost:5000/docs](http://localhost:5000/docs)

---

### Metodo 2: Avvio Manuale Locale (Senza Docker)

#### 1. Backend (FastAPI)
```bash
cd backend
python -m venv venv

# Su Windows:
venv\Scripts\activate

# Su Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

#### 2. Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Accesso & Credenziali Demo

Una volta aperta l'applicazione su `http://localhost:3000/login`, puoi accedere nei seguenti modi:
1. **Accesso a 1-Click**: Clicca sul pulsante **⚡ Accedi come Utente Demo** per accedere subito senza digitare nulla.
2. **Credenziali Demo Predefinite**:
   * **Email**: `stefano@example.com`
   * **Password**: `flyrent2026`
3. **Nuovo Account**: Seleziona la scheda **Registrati** per creare il tuo account personale.

---

## 📌 Funzionalità Principali

* **Landing Page**: Presentazione e panoramica per Smart Worker.
* **Vista Tabella Full-Width & Vista Kanban**: Alterna la visualizzazione e gestisci gli stati delle trattative (`Bozza`, `Contattato`, `In Attesa`, `Visita/Call`, `Opzionato`, `Confermato`, `Scartato`).
* **Smart Work Check & Parcheggio**: Filtra per connessione internet (Fibra FTTH, FTTC, FWA), presenza di scrivania e tipologia di posto auto/box.
* **Calcolo Costi 2 Mesi**: Somma automatica di canone + utenze stimate + condominio.
* **Messaggi WhatsApp Rapidi**: Generazione automatica di messaggi pronti per i proprietari.
* **Gestione Foto & Lightbox**: Caricamento immagini (Base64), URL link e visualizzatore fullscreen.
* **Database Cloud**: Sincronizzazione in tempo reale su MongoDB Atlas per accedere allo stesso archivio da qualsiasi computer.
