\# Sales Data Engineering Pipeline



An end-to-end data pipeline that loads sales data from CSV, cleans and validates it, synchronizes it with PostgreSQL, performs analytics, generates reports, and provides an interactive Streamlit dashboard.



\---



\## Project Overview



This project demonstrates a complete data pipeline workflow:



```text

CSV Data

&#x20; |

&#x20; v

Data Loading

&#x20; |

&#x20; v

Data Cleaning

&#x20; |

&#x20; v

Data Validation

&#x20; |

&#x20; v

PostgreSQL

&#x20; |

&#x20; v

Analytics

&#x20; |

&#x20; v

Reports

&#x20; |

&#x20; v

Streamlit Dashboard

```



The pipeline is designed with separate components for data processing, database operations, analytics, reporting, testing, configuration, and logging.



\---



\## Features



\- CSV data ingestion

\- Required-column validation

\- Duplicate-row removal

\- Data cleaning

\- Automatic `total\_sales` calculation

\- Data quality validation

\- Duplicate order ID detection

\- Date validation

\- Quantity and price validation

\- Total-sales consistency validation

\- PostgreSQL integration

\- Upsert-based database synchronization

\- Database data verification

\- Sales analytics

\- Report generation

\- Interactive Streamlit dashboard

\- City filtering

\- Category filtering

\- Date-range filtering

\- KPI cards

\- Sales charts

\- Filtered-data download

\- Rotating application logs

\- Automated testing with pytest

\- Environment-variable based database configuration



\---



\## Technology Stack



\- Python

\- Pandas

\- PostgreSQL

\- psycopg2

\- Streamlit

\- pytest

\- python-dotenv

\- Git



\---



\## Project Structure



```text

data-pipeline/

|

+-- config/

|   +-- \_\_init\_\_.py

|   +-- settings.py

|

+-- dashboard/

|   +-- app.py

|

+-- data/

|   +-- sales.csv

|

+-- database/

|   +-- load\_to\_db.py

|

+-- src/

|   +-- load\_data.py

|   +-- clean\_data.py

|   +-- validate\_data.py

|   +-- analytics.py

|   +-- generate\_reports.py

|

+-- tests/

|   +-- \_\_init\_\_.py

|   +-- test\_clean\_data.py

|   +-- test\_database.py

|   +-- test\_pipeline.py

|   +-- test\_validate\_data.py

|

+-- utils/

|   +-- logger.py

|

+-- output/

|   +-- reports/

|

+-- logs/

|

+-- .env.example

+-- .gitignore

+-- requirements.txt

+-- README.md

+-- run\_pipeline.py

```



\---



\## Installation



\### 1. Clone the Repository



```bash

git clone <repository-url>

cd data-pipeline

```



\### 2. Create a Virtual Environment



```powershell

python -m venv .venv

```



\### 3. Activate the Virtual Environment



For Windows PowerShell:



```powershell

.venv\\Scripts\\Activate.ps1

```



\### 4. Install Dependencies



```powershell

pip install -r requirements.txt

```



\---



\## PostgreSQL Configuration



The pipeline uses PostgreSQL as the database layer.



Make sure PostgreSQL is installed and running before executing the database stage.



Create a `.env` file in the project root:



```env

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=your\_database\_name

DB\_USER=your\_database\_user

DB\_PASSWORD=your\_database\_password

```



The project provides `.env.example` as a configuration template.



Do not commit `.env` to Git.



\---



\## Run the Complete Pipeline



From the project root:



```powershell

python run\_pipeline.py data/sales.csv

```



The pipeline executes the following stages:



```text

STEP 1 - Load raw data

STEP 2 - Clean data

STEP 3 - Validate data

STEP 4 - Load data into PostgreSQL

STEP 5 - Run analytics

STEP 6 - Generate reports

```



If all stages complete successfully, the pipeline displays the total execution time.



\---



\## Data Cleaning



The cleaning stage:



\- Loads the raw CSV file

\- Removes empty rows

\- Removes duplicate rows

\- Validates required columns

\- Calculates `total\_sales`



The calculation is:



```text

total\_sales = quantity \* price

```



The cleaned dataset is saved to:



```text

output/cleaned\_sales.csv

```



\---



\## Data Validation



The validation stage checks:



\- Required columns

\- Missing values

\- Duplicate order IDs

\- Duplicate rows

\- Invalid order IDs

\- Invalid dates

\- Invalid quantities

\- Invalid prices

\- Invalid total sales

\- Invalid text fields



The pipeline stops if validation fails.



\---



\## PostgreSQL Integration



The database stage:



\- Connects to PostgreSQL

\- Loads the cleaned dataset

\- Synchronizes records using order IDs

\- Inserts new records

\- Updates changed records

\- Detects unchanged records

\- Verifies the final database row count



This allows the pipeline to be run repeatedly without blindly inserting duplicate records.



\---



\## Analytics



The analytics stage calculates:



\- Sales by city

\- Sales by category

\- Sales by product

\- Total quantity sold



Example outputs include:



```text

Sales by City

Sales by Category

Sales by Product

Total Quantity Sold

```



\---



\## Report Generation



The reporting stage generates:



\- Sales by city report

\- Sales by category report

\- Sales by product report

\- Quantity by product report

\- Pipeline summary report



Generated reports are stored in:



```text

output/reports/

```



\---



\## Streamlit Dashboard



The project includes an interactive dashboard located at:



```text

dashboard/app.py

```



Start the dashboard with:



```powershell

streamlit run dashboard/app.py

```



The dashboard provides:



\### Filters



\- City

\- Category

\- Date range



\### Key Performance Indicators



\- Total Sales

\- Total Orders

\- Total Quantity

\- Average Order Value

\- Top Product

\- Top City



\### Visualizations



\- Sales by City

\- Sales by Category

\- Sales by Product

\- Daily Sales Trend

\- Quantity Sold by Product



The dashboard also provides filtered sales-data download functionality.



\---



\## Logging



Application logs are stored in:



```text

logs/pipeline.log

```



The project uses a rotating file handler to prevent the log file from growing indefinitely.



The logger records:



\- Pipeline execution

\- Pipeline steps

\- Errors

\- Execution times

\- Child-process output

\- Pipeline completion



\---



\## Testing



The project uses `pytest` for automated testing.



Run the complete test suite:



```powershell

python -m pytest -v

```



The current test suite contains:



```text

25 tests

```



Current status:



```text

25 passed

```



Tests cover:



\### Data Cleaning



\- Valid CSV input

\- Duplicate-row removal

\- Invalid-value handling

\- Missing required columns



\### Database



\- Database connection

\- Sales table existence

\- Sales table data

\- Table columns

\- Unique order IDs

\- Total-sales calculation

\- Positive quantities

\- Valid prices

\- Total-sales values

\- Total quantity



\### Pipeline



\- Complete pipeline execution

\- Cleaned file creation

\- Report generation

\- Required report existence



\### Data Validation



\- Valid data

\- Duplicate order IDs

\- Invalid quantities

\- Invalid prices

\- Invalid total sales

\- Invalid dates

\- Missing columns



\---



\## Output



Generated files are stored under:



```text

output/

```



Cleaned data:



```text

output/cleaned\_sales.csv

```



Reports:



```text

output/reports/

```



\---



\## Environment and Security



Sensitive database credentials are stored in `.env`.



The `.gitignore` file prevents sensitive and generated files from being committed, including:



```text

.env

.venv/

\_\_pycache\_\_/

.pytest\_cache/

logs/

output/

```



A safe configuration template is provided through:



```text

.env.example

```



\---



\## Data Flow



```text

&#x20;                   sales.csv

&#x20;                       |

&#x20;                       v

&#x20;               +---------------+

&#x20;               | Load Data     |

&#x20;               +-------+-------+

&#x20;                       |

&#x20;                       v

&#x20;               +---------------+

&#x20;               | Clean Data    |

&#x20;               +-------+-------+

&#x20;                       |

&#x20;                       v

&#x20;               +---------------+

&#x20;               | Validate Data |

&#x20;               +-------+-------+

&#x20;                       |

&#x20;                       v

&#x20;               +---------------+

&#x20;               | PostgreSQL    |

&#x20;               +-------+-------+

&#x20;                       |

&#x20;             +---------+---------+

&#x20;             |                   |

&#x20;             v                   v

&#x20;      +-------------+     +-------------+

&#x20;      | Analytics   |     | Dashboard   |

&#x20;      +------+------+     +-------------+

&#x20;             |

&#x20;             v

&#x20;      +-------------+

&#x20;      | Reports     |

&#x20;      +-------------+

```



\---



\## Current Project Status



```text

Data ingestion          \[DONE]

Data cleaning           \[DONE]

Data validation         \[DONE]

PostgreSQL integration  \[DONE]

Data synchronization    \[DONE]

Analytics               \[DONE]

Report generation       \[DONE]

Logging                 \[DONE]

Streamlit dashboard     \[DONE]

Dashboard filters       \[DONE]

Automated testing       \[25/25 PASSED]

Git version control     \[DONE]

```



\---



\## Future Improvements



Potential future improvements include:



\- Incremental data processing

\- Larger dataset support

\- Pipeline scheduling

\- GitHub Actions CI/CD

\- Dashboard-specific automated tests

\- Database schema migrations

\- Data quality monitoring

\- Pipeline performance monitoring

\- Docker containerization

\- Cloud deployment

\- Advanced analytics



\---



\## Author



\*\*Abhijeet Kumar\*\*



B.Tech - Computer Science and Engineering (AI)



\---



\## License



This project is intended for educational, portfolio, and development purposes.

