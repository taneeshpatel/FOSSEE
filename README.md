# Chemical Equipment Parameter Visualizer

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/chemical-equipment-visualizer)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2-61dafb.svg)](https://reactjs.org/)
[![Django](https://img.shields.io/badge/django-4.2-092e20.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

**Chemical Equipment Parameter Visualizer** is a hybrid web and desktop application for uploading, analyzing, and visualizing chemical equipment data from CSV files. It provides a shared Django REST API backend used by both a React web app and a PyQt5 desktop app, with user authentication and per-user data isolation. Users can view summary statistics, interactive charts (count, average temperature, and pressure per equipment type), and download PDF reports.

---

## Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Screenshots / Demo](#-screenshots--demo)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact / Support](#-contact--support)

---

## Features

- **Upload & parse CSV** — Upload CSV files with required columns: Equipment Name, Type, Flowrate, Pressure, Temperature  
- **Summary statistics** — View total count, average flowrate, pressure, and temperature  
- **Per-type analytics** — Count, average temperature, and average pressure for each equipment type  
- **Interactive charts** — Bar and pie charts (web: Chart.js; desktop: Matplotlib) for type distribution and metrics  
- **Data table** — Browse parsed equipment rows in a clean, sortable table  
- **PDF reports** — Generate and download PDF reports (ReportLab) with summary and type stats  
- **History** — Last 5 uploads per user; load any previous dataset  
- **User authentication** — Register and login; data is isolated per user (web: session + CSRF; desktop: token)  
- **Dual clients** — Same API for React web app (port 3000) and PyQt5 desktop app  
- **Download desktop app** — Web app offers a zip download of the desktop client  
- **Shared SQLite database** — Single database at project root used by the backend for all clients  

---

## Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.10+, Django 4.2, Django REST Framework, django-cors-headers, rest_framework.authtoken |
| **Data & PDF** | Pandas (CSV parsing, analytics), ReportLab (PDF generation), Pillow |
| **Database** | SQLite 3 (single `db.sqlite3` at project root) |
| **Web frontend** | React 18, Chart.js, react-chartjs-2, Axios |
| **Desktop frontend** | PyQt5, Matplotlib (Qt5Agg backend), Requests |
| **Auth** | Django session auth + CSRF (web), DRF Token auth (desktop) |
| **Build / run** | Create React App (react-scripts), Django `manage.py`, venv |

---

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
│   ├── config/                 # Django project settings
│   │   ├── settings.py        # Main config, DB, CORS, DRF
│   │   ├── urls.py            # Root URLconf (includes equipment API)
│   │   └── wsgi.py
│   ├── equipment/              # Main app: models, API, utils
│   │   ├── models.py           # UploadedDataset, DataSummary (with type_stats)
│   │   ├── views.py           # Auth, upload, datasets, summary, PDF, download-app
│   │   ├── serializers.py     # DRF serializers
│   │   ├── urls.py            # API routes under /api/
│   │   ├── utils.py           # parse_csv, compute_summary, generate_pdf
│   │   └── migrations/
│   ├── manage.py
│   ├── requirements.txt
│   └── run_server.bat         # Convenience: run server with venv Python
├── frontend/                   # React web app
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── api/axios.js       # Axios instance, baseURL, CSRF interceptor
│   │   ├── App.js, App.css, index.js
│   │   └── components/       # Login, Register, Upload, DataTable, Summary, Charts, History
│   └── package.json
├── desktop/                    # PyQt5 desktop app
│   ├── api/client.py          # REST client (login, upload, datasets, summary, PDF)
│   ├── ui/                     # Login window, main window, tabs (upload, charts, history)
│   │   ├── login_window.py
│   │   ├── main_window.py
│   │   ├── upload_tab.py
│   │   ├── chart_tab.py
│   │   ├── history_tab.py
│   │   └── theme.py           # Dark theme (QSS + palette)
│   ├── main.py                 # Entry point
│   └── requirements.txt
├── scripts/                    # Helpers
│   ├── init_db.py             # Run migrations from project root
│   ├── run_backend.bat        # Windows: migrate + runserver
│   └── run_backend.sh         # macOS/Linux: migrate + runserver
├── db.sqlite3                  # Created on first migrate (project root)
├── sample_data.csv             # Example CSV for testing
├── .gitignore
└── README.md
```

---

## Prerequisites

- **Python** 3.10 or higher  
- **Node.js** 18+ and **npm** (or yarn)  
- **Git** (for clone)

No API keys or external credentials are required for local development. Optional: set `DJANGO_SECRET_KEY` in production.

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

### 2. Backend (Django API + database)

The backend must run on **port 8000**; both web and desktop clients use it.

**Option A — Using virtual environment (recommended)**

```bash
cd backend
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**Option B — Using venv Python without activating**

```bash
cd backend
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

**Database setup and run**

```bash
# From backend/ with venv activated:
python manage.py migrate

# Start server (with venv activated):
python manage.py runserver
# Or without activating (Windows):
venv\Scripts\python.exe manage.py runserver
```

**Convenience scripts (from project root)**

- **Windows:** `scripts\run_backend.bat` (runs migrate then runserver; uses system `python`)  
- **macOS/Linux:** `./scripts/run_backend.sh`  

Or use the backend helper:

- **Windows:** `backend\run_server.bat` (uses `backend\venv\Scripts\python.exe`)

Database file: `chemical-equipment-visualizer/db.sqlite3` (created at project root on first `migrate`).

### 3. Web app (React)

```bash
cd frontend
npm install
npm start
```

- Dev server: **http://localhost:3000**  
- Build for production: `npm run build` (output in `frontend/build/`)

### 4. Desktop app (PyQt5)

Ensure the **Django backend is running** on `http://127.0.0.1:8000`.

```bash
cd desktop
# Use project venv or a dedicated venv:
pip install -r requirements.txt
python main.py
```

Or with backend venv (from project root):

```bash
backend\venv\Scripts\python.exe desktop\main.py
```

---

## Usage

| Action | Web | Desktop |
|--------|-----|---------|
| **Open app** | http://localhost:3000 | Run `python main.py` from `desktop/` |
| **Register** | Register link on login screen | “Register” button in login window |
| **Login** | Username + password | Username + password (Token stored in client) |
| **Upload CSV** | Choose file → Upload | Select CSV → Upload |
| **View data** | Summary, Data Table, Charts, History | Tabs: Upload & Summary, Charts, History |
| **Download PDF** | “Download PDF Report” (when a dataset is loaded) | “Download PDF Report” in Upload tab |
| **Load from history** | “Load” in History section | “Load” in History tab |

**Sample CSV format** (required columns; exact names, case-sensitive):

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,45.5,12.3,78.9
Valve-B2,Valve,30.2,8.7,55.4
```

See `sample_data.csv` in the project root for a full example.

**Common commands**

```bash
# Backend (from backend/, venv activated)
python manage.py migrate          # Apply migrations
python manage.py runserver        # Dev server @ 8000
python manage.py createsuperuser  # Optional: Django admin

# Frontend (from frontend/)
npm start   # Dev @ 3000
npm run build

# Desktop (from desktop/)
python main.py
```

---

## API Documentation

Base URL: **http://127.0.0.1:8000/api/** (or http://localhost:8000/api/).

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `auth/csrf/` | No | Ensure CSRF cookie (web app) |
| POST | `auth/register/` | No | Register (username, password) |
| POST | `auth/login/` | No | Login; returns session + `token` (for desktop) |
| POST | `auth/logout/` | Yes | Logout |
| POST | `upload/` | Yes | Upload CSV (`file` in `multipart/form-data`) |
| GET | `datasets/` | Yes | List last 5 datasets for current user |
| GET | `datasets/<id>/` | Yes | Get dataset (incl. `raw_data`) |
| GET | `summary/<id>/` | Yes | Get summary (incl. `type_stats`) |
| GET | `pdf/<id>/` | Yes | Download PDF report |
| GET | `download-app/` | No | Download desktop app zip |

**Authentication**

- **Web:** Session + CSRF cookie (`withCredentials`, `X-CSRFToken` header).  
- **Desktop:** `Authorization: Token <token>` (from `auth/login/` response).

**Example: Login (desktop)**

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"youruser","password":"yourpass"}'
```

Response includes `token` for subsequent requests.

**Example: List datasets (authenticated)**

```bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/datasets/
```

**Example: Upload (authenticated)**

```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@sample_data.csv"
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SECRET_KEY` | No (dev) | Django secret key; set in production. |

No `.env` file is required for local development. Optional `.env` in `backend/` can be used to set `DJANGO_SECRET_KEY` if you load it in `settings.py`.

**.env.example (optional)**

```env
# backend/.env.example
DJANGO_SECRET_KEY=your-secret-key-here
```

---

## Deployment

### Web app

- **Backend:** Run Django on a WSGI server (e.g. Gunicorn) behind a reverse proxy (e.g. Nginx). Set `DEBUG=False`, `ALLOWED_HOSTS`, and `DJANGO_SECRET_KEY`. Use a production database (e.g. PostgreSQL) if desired; update `config/settings.py` and run migrations.
- **Frontend:** Run `npm run build`, then serve the `frontend/build/` directory (e.g. Nginx, or same server as API with static files).
- **CORS:** Set `CORS_ALLOWED_ORIGINS` (and `CSRF_TRUSTED_ORIGINS` if needed) to your frontend origin(s).

### Desktop app

- **Distribution:** Package the `desktop/` folder (and optionally a bundled Python + dependencies) into an installer or zip. The “Download App” endpoint serves a zip of the desktop app; users need Python and `pip install -r desktop/requirements.txt` to run it unless you use PyInstaller/cx_Freeze etc.
- **API URL:** For production, change `APIClient.BASE_URL` in `desktop/api/client.py` to the deployed API base URL.

### Suggested hosting

- **Backend:** Railway, Render, Heroku, DigitalOcean, or any VPS with Python/WSGI.  
- **Frontend:** Vercel, Netlify, or same server as API (static files).  

---

## Screenshots / Demo

| View | Description |
|------|-------------|
| **Web — Login** | Login/Register form; “Download App” link. |
| **Web — Dashboard** | Upload CSV, Summary cards, Data Table, Charts (count, avg temp, avg pressure by type), History. |
| **Desktop — Login** | Dark-themed login window with Register. |
| **Desktop — Main** | Tabs: Upload & Summary, Charts (2×2: count, share, avg temp, avg pressure), History. |

*Add screenshots here (e.g. `docs/screenshot-web.png`, `docs/screenshot-desktop.png`) and link them.*

**Live demo:** *Add link if you deploy a public instance.*

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **ModuleNotFoundError: No module named 'django'** | Use the project’s venv: activate it or run `backend\venv\Scripts\python.exe` for manage.py and `backend\run_server.bat` for the server. |
| **Upload failed / 403** | Ensure CSRF is set (web: call `GET /api/auth/csrf/` before first POST). Backend has CSRF_TRUSTED_ORIGINS for localhost. |
| **CORS errors in browser** | Backend must be running; `CORS_ALLOWED_ORIGINS` in `config/settings.py` must include `http://localhost:3000` (and `http://127.0.0.1:3000` if used). |
| **Desktop: connection refused** | Start Django first: `python manage.py runserver` (or `run_server.bat`) so API is at http://127.0.0.1:8000. |
| **CSV parse error / missing columns** | CSV must have exactly: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature` (case-sensitive). |
| **No chart data / empty history** | Upload a valid CSV first; history shows last 5 datasets per user. Old datasets without `type_stats` still show count-only charts. |
| **Database errors** | Run `python manage.py migrate` from `backend/` (with venv). DB file is at project root: `db.sqlite3`. |

---

## Contributing

1. Fork the repository and create a feature branch.  
2. Follow existing code style (e.g. Django/DRF conventions, React functional components).  
3. Ensure backend migrations and frontend build run cleanly.  
4. Submit a pull request with a short description of the change.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Contact / Support

- **Issues:** Open a GitHub issue for bugs or feature requests.  
- **Author:** *Your Name / Your Team*  
- **Repository:** *https://github.com/yourusername/chemical-equipment-visualizer*
