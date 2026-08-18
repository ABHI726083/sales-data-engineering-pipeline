# Sales Data Engineering Pipeline

An end-to-end data engineering project that ingests sales data from CSV, cleans and validates it, loads it into PostgreSQL, performs analytics, generates reports, and provides API and dashboard access.

## Project Overview

The pipeline follows this workflow:

\`\`\`text
CSV Data
    |
    v
Load Data
    |
    v
Clean Data
    |
    v
Validate Data
    |
    v
PostgreSQL
    |
    v
Analytics
    |
    v
Reports
    |
    +----> FastAPI
    |
    +----> Streamlit Dashboard
\`\`\`

## Features

- CSV data ingestion
- Data cleaning
- Duplicate removal
- Invalid record detection
- Data validation
- Missing-value validation
- Date validation
- Quantity and price validation
- Total sales calculation
- PostgreSQL database loading
- Insert, update, and unchanged-record handling
- Transaction and rollback handling
- Sales analytics
- Automated CSV reports
- FastAPI REST API
- API filtering and pagination
- Streamlit dashboard
- Automated application startup
- Application logging
- Automated testing with pytest
- Bandit security scanning
- pip-audit dependency scanning
- GitHub Actions CI

## Data Cleaning and Validation

The pipeline is designed for structured sales transaction data.

### Expected Input Columns

\`\`\`text
order_id
order_date
product
category
quantity
price
city
\`\`\`

### Cleaning Checks

The pipeline checks for:

- Empty rows
- Duplicate rows
- Duplicate order IDs
- Invalid order IDs
- Invalid dates
- Invalid quantities
- Invalid prices
- Missing values
- Missing required columns
- Invalid text fields

The number of rows does not need to remain fixed. Invalid or duplicate records can be removed during cleaning.

### Total Sales Calculation

\`\`\`text
total_sales = quantity * price
\`\`\`

## PostgreSQL

Validated sales data is loaded into PostgreSQL.

The database layer supports:

- Table creation
- New record insertion
- Existing record updates
- Unchanged record detection
- Transaction handling
- Rollback handling
- Database verification
- Database connection cleanup

## Analytics

The pipeline calculates:

- Sales by city
- Sales by category
- Sales by product
- Quantity by product
- Total quantity sold
- Total sales
- Total orders
- Average order value

## Generated Reports

Reports are generated in:

\`\`\`text
output/reports/
\`\`\`

Available reports:

- \`pipeline_summary.csv\`
- \`sales_by_city.csv\`
- \`sales_by_category.csv\`
- \`sales_by_product.csv\`
- \`quantity_by_product.csv\`

Cleaned data is generated at:

\`\`\`text
output/cleaned_sales.csv
\`\`\`

## FastAPI

The project includes a FastAPI backend for accessing sales data and analytics.

### Main Endpoints

\`\`\`text
/
/health
/sales
/analytics/summary
/analytics/city
/analytics/category
/analytics/product
\`\`\`

The \`/sales\` endpoint supports filtering and pagination.

### Examples

\`\`\`text
/sales?city=Delhi
/sales?category=Electronics
/sales?product=Laptop
/sales?limit=10&offset=0
\`\`\`

### API Documentation

\`\`\`text
http://127.0.0.1:8000/docs
\`\`\`

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard for viewing sales data and analytics.

### Run the Dashboard

\`\`\`powershell
streamlit run dashboard\app.py
\`\`\`

## Automated Application Startup

The project includes an automated launcher that starts the FastAPI backend and Streamlit dashboard together.

### Start the Application

\`\`\`powershell
python start_app.py
\`\`\`

The launcher automatically starts both services and opens:

\`\`\`text
FastAPI Documentation
http://127.0.0.1:8000/docs

Streamlit Dashboard
http://127.0.0.1:8501
\`\`\`

Press \`Ctrl+C\` to stop the application.

## Logging

Pipeline execution logs are stored in:

\`\`\`text
logs/pipeline.log
\`\`\`

Logs include:

- Pipeline steps
- Execution times
- Database operations
- Analytics
- Report generation
- Errors
- Exceptions
- Cleanup failures

## Testing

The project includes automated tests covering:

- API functionality
- API filtering
- API pagination
- API edge cases
- Data cleaning
- Data validation
- Database connectivity
- Database structure
- Database integrity
- Pipeline execution
- Report generation

### Test Result

47 tests passed.

Run the tests with:

\`\`\`powershell
pytest -v
\`\`\`

Or:

\`\`\`powershell
pytest -q
\`\`\`

## Security and Quality Checks

### Dependency Check

\`\`\`powershell
python -m pip check
\`\`\`

Expected result:

\`\`\`text
No broken requirements found.
\`\`\`

### Dependency Vulnerability Scan

\`\`\`powershell
pip-audit
\`\`\`

\`\`\`powershell
pip-audit -r requirements.txt
\`\`\`

Expected result:

\`\`\`text
No known vulnerabilities found
\`\`\`

### Python Security Scan

\`\`\`powershell
bandit -r api src utils database config run_pipeline.py start_app.py -ll
\`\`\`

Expected result:

\`\`\`text
No issues identified.
\`\`\`

## Running the Complete Pipeline

### Activate the Virtual Environment

\`\`\`powershell
.\.venv\Scripts\Activate.ps1
\`\`\`

### Install Dependencies

\`\`\`powershell
pip install -r requirements.txt
\`\`\`

### Configure Environment Variables

Create a \`.env\` file using \`.env.example\` as a template.

Do not commit \`.env\` to Git.

### Run the Complete Pipeline

\`\`\`powershell
python run_pipeline.py data\sales.csv
\`\`\`

### Pipeline Stages

\`\`\`text
1. Load raw data
2. Clean data
3. Validate data
4. Load into PostgreSQL
5. Run analytics
6. Generate reports
\`\`\`

## Project Structure

\`\`\`text
sales-data-engineering-pipeline/
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- api/
|   +-- app.py
|
+-- config/
|   +-- __init__.py
|   +-- settings.py
|
+-- dashboard/
|   +-- app.py
|
+-- data/
|   +-- sales.csv
|
+-- database/
|   +-- load_to_db.py
|
+-- logs/
|   +-- pipeline.log
|
+-- output/
|   +-- cleaned_sales.csv
|   +-- reports/
|
+-- src/
|   +-- analytics.py
|   +-- clean_data.py
|   +-- generate_reports.py
|   +-- load_data.py
|   +-- validate_data.py
|
+-- tests/
|   +-- __init__.py
|   +-- test_api.py
|   +-- test_clean_data.py
|   +-- test_database.py
|   +-- test_pipeline.py
|   +-- test_validate_data.py
|
+-- utils/
|   +-- logger.py
|
+-- .env.example
+-- .gitignore
+-- README.md
+-- requirements.txt
+-- run_pipeline.py
+-- start_app.py
\`\`\`

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core pipeline development |
| Pandas | Data processing |
| PostgreSQL | Database |
| Psycopg2 | PostgreSQL connectivity |
| FastAPI | REST API |
| Streamlit | Interactive dashboard |
| Pytest | Automated testing |
| Bandit | Python security scanning |
| pip-audit | Dependency vulnerability scanning |
| Git | Version control |
| GitHub Actions | Continuous integration |

## Continuous Integration

GitHub Actions automatically runs the test suite when changes are pushed to \`main\` or submitted through a pull request.

The workflow performs:

1. Checkout repository
2. Set up Python 3.14
3. Install dependencies
4. Run pytest

Workflow file:

\`\`\`text
.github/workflows/ci.yml
\`\`\`

## Final Verification

The completed project was verified with:

- 47 automated tests passed
- Pipeline execution successful
- PostgreSQL verification successful
- API verification successful
- Reports generated successfully
- \`pip check\` passed
- \`pip-audit\` passed
- Bandit security scan passed
- Git working tree clean

The pipeline was also tested with intentionally invalid sales records, including:

- Duplicate records
- Invalid dates
- Negative quantities
- Negative prices

The cleaning stage successfully removed those invalid records before validation and database loading.

## Project Objective

The objective of this project is to demonstrate a complete data engineering workflow that transforms raw sales data into validated, database-ready information and makes the resulting analytics available through reports, APIs, and an interactive dashboard.

## License
This project is intended for educational, portfolio, and demonstration purposes.