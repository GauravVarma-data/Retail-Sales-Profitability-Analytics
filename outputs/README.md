# Retail Sales & Profitability Analytics

## Overview
A business analytics portfolio project using the Superstore retail dataset to evaluate sales performance, profitability, customer value, product performance, regional trends, discounts, and shipping efficiency.

## Business Questions
- What are total sales, profit, orders, and profit margin?
- Which categories and sub-categories drive or destroy profit?
- Which regions and states perform best?
- How does discount affect profitability?
- Which customers generate the most sales and profit?
- How do sales and profit trend over time?
- Which shipping modes have the longest delivery times?

## Tools
Python | Pandas | SQL | Power BI | Excel | Streamlit

## Project Structure
```text
data/        Raw Superstore Excel file
src/         Python analysis
sql/         Business SQL queries
dashboard/   Streamlit dashboard
outputs/     Generated CSVs and charts
POWER_BI_SPEC.md
requirements.txt
```

## How to Run
Place the downloaded Superstore Excel file at:
`data/superstore_sales.xlsx`

Then run:
```bash
pip install -r requirements.txt
python src/01_analysis.py
streamlit run dashboard/app.py
```

The Python script generates the analysis outputs in `outputs/`.
