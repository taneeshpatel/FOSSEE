# Chemical Equipment Parameter Visualizer

Transform raw equipment measurement data into actionable insights through automated analysis and visual reporting.

## What You Can Do

This system processes CSV files containing equipment performance metrics and delivers comprehensive analytics. Input your data files with equipment identifiers, type classifications, flowrate values, pressure measurements, and temperature readings—the platform handles the rest.

The application automatically calculates aggregate statistics: total equipment inventory, mean flowrate across all units, average pressure and temperature readings, plus distribution breakdowns by equipment category. Visual analytics include four distinct chart formats showing count distributions, percentage allocations, and type-specific temperature and pressure averages.

Your workspace maintains the five most current datasets with instant reload capability. Each analysis can be exported as a formatted PDF document. Access the platform through your web browser or via a dedicated desktop client—both connect to a unified backend API with protected user sessions.

## Technology Foundation

**Server Components:**
The backend runs on Django framework (4.2+) with REST capabilities via Django REST Framework. CSV processing and numerical operations utilize the Pandas library. SQLite handles data persistence with automated cleanup keeping only your latest five uploads. ReportLab library generates PDF reports. Authentication supports both session-based (for browsers) and token-based (for desktop) authorization.

**Web Client:**
Frontend built on React.js (version 18+). Chart.js library powers the visual analytics. HTTP requests flow through Axios with integrated CSRF token management for security.

**Desktop Client:**
GUI constructed with PyQt5 for multi-platform support (Windows/Mac/Linux). Matplotlib generates statistical charts. API communication uses token authentication headers.

## File Organization

```
chemical-equipment-visualizer/
├── backend/                          Server API implementation
│   ├── config/                       Django configuration layer
│   ├── equipment/                    Core application module
│   │   ├── models.py                 Data schemas (UploadedDataset, DataSummary)
│   │   ├── serializers.py            JSON conversion handlers
│   │   ├── views.py                  HTTP endpoint logic
│   │   ├── utils.py                  CSV parser, analytics engine, PDF generator
│   │   └── migrations/               Database version control
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                         Browser-based interface
│   ├── src/
│   │   ├── App.js                    Primary component with auth logic
│   │   ├── api/
│   │   │   └── axios.js              HTTP client configuration
│   │   └── components/
│   │       ├── Login.js              Authentication screen
│   │       ├── Register.js           New account creation
│   │       ├── Upload.js             File upload handler
│   │       ├── DataTable.js          Grid data viewer
│   │       ├── Summary.js            Metrics panel with PDF export
│   │       ├── Charts.js             Visual analytics display
│   │       └── History.js            Previous uploads list
│   ├── package.json
│   └── public/
│
├── desktop/                          Standalone application
│   ├── main.py                       Program entry point
│   ├── api/
│   │   └── client.py                 Backend connector (token auth)
│   └── ui/
│       ├── login_window.py           Login dialog
│       ├── main_window.py            Main interface shell
│       ├── upload_tab.py             Upload and statistics panel
│       ├── chart_tab.py              Visualization workspace
│       └── history_tab.py            Dataset history viewer
│
├── sample_data.csv                   Example dataset
├── .gitignore
└── README.md
```

## Required Software

Your development environment needs:
- Python 3.10 or later
- Node.js 18 or later  
- npm (Node package manager)

## Getting Started

### Backend Setup

```bash
# Navigate into backend folder
cd chemical-equipment-visualizer/backend

# Initialize Python virtual environment
python -m venv venv

# Activate the environment
# For Windows users:
venv\Scripts\activate
# For Mac/Linux users:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize database schema
python manage.py migrate

# Launch development server
python manage.py runserver
```

Server will listen on **http://localhost:8000**

### Web Interface Setup

```bash
# Open a second terminal
cd chemical-equipment-visualizer/frontend

# Install Node.js packages
npm install

# Start React development server
npm start
```

Browser will open **http://localhost:3000** automatically

### Desktop Application Setup

```bash
# Navigate to desktop folder
cd chemical-equipment-visualizer/desktop

# Install PyQt5 and dependencies (use backend's venv)
pip install -r requirements.txt

# Launch the application
python main.py
```

**Critical:** The Django backend must be running before launching either frontend.

## Operating Instructions

### Using the Web Interface

**Initial Access:**
Visit http://localhost:3000 in your browser. Create a new account via the Register button or sign in with existing credentials.

**Data Upload Workflow:**
1. Click the "Select CSV File" button
2. Choose your data file from disk
3. Press "Submit" to process

**Reviewing Results:**
Statistics appear immediately after processing. Scroll through the page to view the equipment data grid, then examine four visualization panels showing equipment counts, distribution percentages, and average metrics by category.

**Exporting Reports:**
Locate the "Download PDF Report" button in the statistics section to save a formatted document.

**Accessing Historical Data:**
The History panel shows your five latest uploads. Click "Load" next to any entry to restore that analysis.

### Using the Desktop Application

**Authentication:**
Launch the program, enter your username and password, then click Login.

**Upload and Analysis (First Tab):**
Select "Select CSV File" to choose your data, then "Upload" to process it. View calculated metrics including Total Count, Average Flowrate, Average Pressure, and Average Temperature. Use "Download PDF" to export the report to your chosen location.

**Visualizations (Second Tab):**
Switch to the Charts tab for four Matplotlib graphs: equipment count by type, distribution pie chart, average temperature by type, and average pressure by type.

**Dataset Archive (Third Tab):**
Browse your five most recent uploads. Double-click any row to load that dataset.

## Data File Format

Your CSV must include these exact column headers:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,2.3,75.2
Valve-B2,Valve,89.3,1.8,68.5
Tank-C3,Tank,0.0,1.2,72.0
Pump-A2,Pump,145.8,2.1,74.5
Valve-B3,Valve,92.1,1.9,69.2
```

**Format Rules:**
- All five columns must exist
- Column names are case-sensitive (exact match required)
- Blank rows get automatically removed
- Numeric columns must contain valid decimal numbers

The project includes `sample_data.csv` in the root directory for testing.

## API Reference

**Base endpoint:** `http://localhost:8000/api`

| Route | HTTP Method | Purpose | Requires Auth |
|-------|-------------|---------|---------------|
| `/auth/register/` | POST | Create new user account | No |
| `/auth/login/` | POST | Authenticate user (returns session + token) | No |
| `/auth/logout/` | POST | End user session | Yes |
| `/upload/` | POST | Process CSV file | Yes |
| `/datasets/` | GET | Retrieve five most recent datasets | Yes |
| `/datasets/<id>/` | GET | Fetch specific dataset with raw records | Yes |
| `/summary/<id>/` | GET | Retrieve calculated statistics | Yes |
| `/pdf/<id>/` | GET | Export PDF report | Yes |

## Capability Summary

🔹 **Data Ingestion** - Process equipment measurement CSV files  
🔹 **Automated Analytics** - Calculate totals, averages, categorical distributions  
🔹 **Category Breakdown** - Per-equipment-type statistical analysis  
🔹 **Visual Intelligence** - Four chart types (web: Chart.js | desktop: Matplotlib)  
🔹 **Document Export** - PDF report generation and download  
🔹 **Session History** - Automatic storage of five latest datasets  
🔹 **Dual Access** - Browser and desktop application interfaces  
🔹 **User Management** - Secure registration and authentication  

## Troubleshooting Guide

| Symptom | Resolution |
|---------|-----------|
| **"Django module not found" error** | Activate Python virtual environment first |
| **CORS policy violation in browser** | Verify Django settings include `http://localhost:3000` in CORS_ALLOWED_ORIGINS |
| **Desktop client connection failure** | Confirm Django server is active on port 8000 |
| **CSV file rejected** | Verify presence of all five required columns with exact names |
| **Missing chart visualizations** | Reload the dataset from History to regenerate statistics |
| **Port conflict** | Terminate existing process or specify alternate port |

## Technology Stack

| Layer | Implementation |
|-------|----------------|
| API Server | Django, Django REST Framework |
| Data Engine | Pandas |
| Storage | SQLite |
| Document Generation | ReportLab |
| Web UI | React.js, Chart.js, Axios |
| Desktop UI | PyQt5, Matplotlib |
| Security | Django Auth, Token Authentication |

## License

This project is released under MIT License terms.

---

**Built with Django • React • PyQt5**
