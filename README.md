# Rental Accounting (on‑prem)

A minimal on‑prem web app to enter and browse rental data, post double‑entry transactions,
and generate Income Statement, Balance Sheet, Expense Report. Includes basic audits
and backup scripts to a NAS mount.

## Stack
- **Backend:** FastAPI (Python), SQLAlchemy, Pydantic
- **DB:** PostgreSQL
- **Frontend:** Vanilla HTML/CSS/JS (served by backend)
- **Optional:** Docker Compose for easy bring‑up

---

## Quick Start (Docker ‑ recommended)

1. Install Docker & Docker Compose.
2. From the project root, run:
   ```bash
   docker compose up -d
   ```
3. Open the app: http://localhost:8000

This will:
- start PostgreSQL with the schema & seed data applied
- start the backend (also serving the simple frontend at `/`)

---

## Manual Setup (Ubuntu or Windows)

### 1) Install PostgreSQL and create DB
- Create a database named `rental_accounting` and a user with permissions.

Apply schema & seed data:
```bash
psql postgresql://postgres:postgres@localhost:5432/rental_accounting -f db/schema.sql
psql postgresql://postgres:postgres@localhost:5432/rental_accounting -f db/seed.sql
```

### 2) Backend
```bash
cd backend
cp .env.example .env   # adjust DATABASE_URL etc.
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open http://localhost:8000

### 3) Frontend
The simple frontend is served by the backend at `/`. Static files are under `frontend/`.

If you prefer to serve the frontend separately (e.g., Nginx/IIS), set CORS via `ALLOWED_ORIGINS`
in `.env` and host `frontend/` as static content, pointing API calls to the backend base URL.

---

## Using the App

- **Data Entry**: Create Companies, Properties, Tenants, Leases, Rents; Add Account Types/Subtypes/Accounts.
- **Transactions**: Post double‑entry transactions (Debit, Credit, Amount, Date, optional Property/Tenant).
- **Reports**: Income Statement (range), Balance Sheet (as‑of date), Expense Report (range).
- **Audits**: Trial Balance, orphan references, positive amounts, lease date consistency.

API docs are at: `http://localhost:8000/docs`

---

## NAS Backups

Mount your NAS path (e.g., `/mnt/nas`). Edit `BACKUP_DIR` in `.env`/scripts.

Run a manual backup:
```bash
BACKUP_DIR=/mnt/nas/rental_accounting_backups \DB_URL=postgresql://postgres:postgres@localhost:5432/rental_accounting \./scripts/backup.sh
```

### Nightly (systemd on Ubuntu)
Copy the service & timer to `/etc/systemd/system/` and adjust the ExecStart path:
```
/opt/rental_accounting/scripts/systemd-backup.service
/opt/rental_accounting/scripts/systemd-backup.timer
```
Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now systemd-backup.timer
```

### Windows
Use Task Scheduler to run `pg_dump` daily, or run Docker and back up the `dbdata` volume.

---

## Notes & Extensions

- This starter creates tables automatically on backend boot (**dev use**). For production, use migrations.
- Add authentication if hosting beyond LAN.
- Add more reports (AR aging, rent roll), exports (CSV/PDF), and role‑based access.
- Tie rents to invoices by posting transactions monthly (Debit AR / Credit Rental Income; then Debit Cash / Credit AR on payment).

---

© 2025
