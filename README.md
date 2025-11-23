# Aviation Data Automation System

This project automates the processing of aviation data, generates a PDF report, and sends it by email using the Gmail API. It removes manual work and ensures consistent daily reporting for aviation or operations teams.

## Features

### Data Processing

* Reads CSV/Excel flight logs
* Cleans and validates data
* Computes totals and summaries

### PDF Report Generation

* Creates structured aviation reports
* Saves output to the `reports/` directory

### Email Automation

* Uses Gmail API with OAuth
* Sends the generated report as an attachment

### Optional Scheduling

You can schedule the entire workflow (daily, hourly, or custom) through Python’s `schedule` module.

## Project Structure

```
auto_report/
├── config/                # credentials.json for Gmail API
├── data/                  # Input aviation data
├── logs/                  # Application logs
├── reports/               # Generated reports
├── main.py                # Main workflow runner
├── process_data.py        # Data cleaning and analysis
├── generate_report.py     # PDF creation
├── send_email.py          # Email sending
└── requirements.txt
```

## How It Works

1. Place your flight data inside the `data` folder.
2. `process_data.py` reads and processes the dataset.
3. `generate_report.py` creates the PDF report.
4. `send_email.py` emails the report.
5. `main.py` ties all steps together.

## Setup

### 1. Create a virtual environment

```
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Enable Gmail API

1. Open Google Cloud Console
2. Enable Gmail API
3. Create an OAuth Client ID
4. Download `credentials.json`
5. Place it inside `config/`

The first run will generate `token.json` automatically.

## Run the Project

```
python main.py
```

This will read the data, generate a PDF, email it, and log the process.

## Why This Project Matters

* Reduces manual reporting work
* Ensures accuracy and consistency
* Suitable for daily operational use

## Future Improvements

* Deployment on cloud platforms
* Add charts/graphs to the report
* Web dashboard
* Alerts and notifications

If you want a shorter version, a professional LICENSE, or a `requirements.txt`, I can prepare those too.
