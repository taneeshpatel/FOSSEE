# Chemical Equipment Parameter Visualizer

A full-stack application for analyzing and visualizing chemical equipment parameters from CSV files. Upload equipment data and get instant statistical summaries, interactive charts, and downloadable PDF reports.

## What This Project Does

- Upload CSV files with chemical equipment data (Equipment Name, Type, Flowrate, Pressure, Temperature)
- Automatically compute statistical summaries (total count, averages per type)
- Generate 4 interactive visualizations (count by type, distribution pie chart, avg temperature/pressure by type)
- Download comprehensive PDF reports
- Store and retrieve last 5 uploaded datasets
- Access via web browser or desktop application
- Secure user authentication and session management

## How It's Built

**Backend:**
- Django 4.2+ with Django REST Framework
- Pandas for CSV parsing and analytics
- SQLite database (stores last 5 datasets)
- ReportLab for PDF generation
- Token + Session authentication

**Web Frontend:**
- React.js 18+
- Chart.js for interactive visualizations
- Axios with CSRF token handling

**Desktop App:**
- PyQt5 for cross-platform GUI
- Matplotlib for charts
- Token-based API authentication

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                          # Django REST API
│   ├── config/                       # Django settings, URLs, WSGI
│   ├── equipment/                    # Main app
│   │   ├── models.py                 # UploadedDataset, DataSummary models
│   │   ├── serializers.py            # DRF serializers
│   │   ├── views.py                  # API endpoints
│   │   ├── utils.py                  # parse_csv, compute_summary, generate_pdf
│   │   └── migrations/               # Database migrations
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                         # React web app
│   ├── src/
│   │   ├── App.js                    # Main component with auth state
│   │   ├── api/
│   │   │   └── axios.js              # Axios instance with CSRF
│   │   └── components/
│   │       ├── Login.js              # Login form
│   │       ├── Register.js           # Registration form
│   │       ├── Upload.js             # CSV upload interface
│   │       ├── DataTable.js          # Equipment data table
│   │       ├── Summary.js            # Stats cards + PDF download
│   │       ├── Charts.js             # Bar and pie charts
│   │       └── History.js            # Last 5 datasets
│   ├── package.json
│   └── public/
│
├── desktop/                          # PyQt5 desktop app
│   ├── main.py                       # Entry point
│   ├── api/
│   │   └── client.py                 # API client with token auth
│   └── ui/
│       ├── login_window.py           # Login window
│       ├── main_window.py            # Main tabbed window
│       ├── upload_tab.py             # Upload & summary tab
│       ├── chart_tab.py              # Charts tab (Matplotlib)
│       └── history_tab.py            # Dataset history tab
│
├── sample_data.csv                   # Sample CSV for testing
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Installation & Setup

### 1. Backend (Django)

```bash
# Navigate to backend directory
cd chemical-equipment-visualizer/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

Backend runs at **http://localhost:8000**

### 2. Web App (React)

```bash
# Open new terminal
cd chemical-equipment-visualizer/frontend

# Install dependencies
npm install

# Start development server
npm start
```

Web app opens at **http://localhost:3000**

### 3. Desktop App (PyQt5)

```bash
# Navigate to desktop directory
cd chemical-equipment-visualizer/desktop

# Install dependencies (use same venv as backend)
pip install -r requirements.txt

# Run application
python main.py
```

**Note:** Ensure Django backend is running before starting web or desktop app.

## How to Use

### Web Application

1. **Register/Login**
   - Navigate to http://localhost:3000
   - Click "Register" to create account or login with existing credentials

2. **Upload CSV**
   - Click "Select CSV File" button
   - Choose your CSV file
   - Click "Submit"

3. **View Results**
   - Summary statistics appear automatically
   - Scroll down to see data table
   - View 4 interactive charts (count by type, share by type, avg temperature/pressure)

4. **Download PDF Report**
   - Click "Download PDF Report" button in Summary section

5. **Load Previous Datasets**
   - Navigate to History section
   - Click "Load" on any of the last 5 datasets

### Desktop Application

1. **Login**
   - Enter username and password
   - Click "Login"

2. **Upload & View Summary** (Tab 1)
   - Click "Select CSV File"
   - Click "Upload"
   - View statistics (Total Count, Avg Flowrate, Avg Pressure, Avg Temperature)
   - Click "Download PDF" to save report

3. **View Charts** (Tab 2)
   - See 4 Matplotlib visualizations
   - Count by type (bar chart)
   - Share by type (pie chart)
   - Avg temperature by type (bar chart)
   - Avg pressure by type (bar chart)

4. **Browse History** (Tab 3)
   - View last 5 uploaded datasets
   - Double-click any dataset to load it

## CSV File Format

Your CSV file must contain these exact columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,2.3,75.2
Valve-B2,Valve,89.3,1.8,68.5
Tank-C3,Tank,0.0,1.2,72.0
Pump-A2,Pump,145.8,2.1,74.5
Valve-B3,Valve,92.1,1.9,69.2
```

**Requirements:**
- All 5 columns must be present
- Column names are case-sensitive
- Empty rows are automatically removed
- Numeric values must be valid floats

A sample CSV file (`sample_data.csv`) is included in the project root for testing.

## API Endpoints

Base URL: `http://localhost:8000/api`

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/auth/register/` | POST | Register new user | No |
| `/auth/login/` | POST | Login (returns session + token) | No |
| `/auth/logout/` | POST | Logout user | Yes |
| `/upload/` | POST | Upload CSV file | Yes |
| `/datasets/` | GET | Get last 5 datasets | Yes |
| `/datasets/<id>/` | GET | Get specific dataset with raw data | Yes |
| `/summary/<id>/` | GET | Get statistical summary | Yes |
| `/pdf/<id>/` | GET | Download PDF report | Yes |

## Features

✅ **CSV Upload** - Upload equipment parameter data  
✅ **Auto Analysis** - Compute total count, averages, type distribution  
✅ **Type-Based Stats** - Per-equipment-type analytics  
✅ **Interactive Charts** - 4 visualizations (web: Chart.js, desktop: Matplotlib)  
✅ **PDF Reports** - Generate and download comprehensive reports  
✅ **History** - Store and retrieve last 5 datasets  
✅ **Dual Interface** - Web browser and desktop application  
✅ **Authentication** - Secure user login/registration  

## Common Issues

| Problem | Solution |
|---------|----------|
| **Django not found** | Activate virtual environment first |
| **CORS errors** | Verify `CORS_ALLOWED_ORIGINS` includes `http://localhost:3000` |
| **Desktop can't connect** | Ensure Django backend is running on port 8000 |
| **CSV validation fails** | Check all 5 columns are present with exact names |
| **Charts not showing** | Reload dataset from History tab to regenerate stats |
| **Port already in use** | Stop existing process or use different port |

## Tech Stack Summary

| Component | Technology |
|-----------|-----------|
| Backend API | Django, Django REST Framework |
| Data Processing | Pandas |
| Database | SQLite |
| PDF Generation | ReportLab |
| Web Frontend | React.js, Chart.js, Axios |
| Desktop Frontend | PyQt5, Matplotlib |
| Authentication | Django Auth + Token Auth |

## License

MIT License

---

**Made with Python, React, and PyQt5**
