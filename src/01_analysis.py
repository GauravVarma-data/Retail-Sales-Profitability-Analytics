import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "superstore_sales.xlsx"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

# Load first sheet from the Superstore workbook
df = pd.read_excel(DATA)
df.columns = [str(c).strip() for c in df.columns]

# Standardize dates
for col in ["Order Date", "Ship Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Shipping days
if {"Order Date", "Ship Date"}.issubset(df.columns):
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Core KPIs
kpis = pd.DataFrame({
    "Metric": ["Total Sales", "Total Profit", "Total Orders", "Profit Margin"],
    "Value": [
        df["Sales"].sum(),
        df["Profit"].sum(),
        df["Order ID"].nunique() if "Order ID" in df else len(df),
        df["Profit"].sum() / df["Sales"].sum()
    ]
})
kpis.to_csv(OUT / "kpis.csv", index=False)

# Category performance
category = df.groupby("Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
category["ProfitMargin"] = category["Profit"] / category["Sales"]
category.sort_values("Profit", ascending=False).to_csv(
    OUT / "category_performance.csv", index=False
)

# Sub-category performance
subcat = df.groupby("Sub-Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
subcat["ProfitMargin"] = subcat["Profit"] / subcat["Sales"]
subcat.sort_values("Profit").to_csv(
    OUT / "subcategory_profitability.csv", index=False
)

# Regional performance
region = df.groupby("Region", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
region.to_csv(OUT / "regional_performance.csv", index=False)

# Customer performance
customer = df.groupby(["Customer ID", "Customer Name"], as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
)
customer.sort_values("Sales", ascending=False).head(20).to_csv(
    OUT / "top_customers.csv", index=False
)

# Discount analysis
discount = df.groupby("Discount", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
discount["ProfitMargin"] = discount["Profit"] / discount["Sales"]
discount.to_csv(OUT / "discount_profitability.csv", index=False)

# Monthly trend
if "Order Date" in df.columns:
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    monthly = df.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    monthly.to_csv(OUT / "monthly_trend.csv", index=False)

# Shipping performance
if "Shipping Days" in df.columns and "Ship Mode" in df.columns:
    shipping = df.groupby("Ship Mode", as_index=False).agg(
        Orders=("Order ID", "nunique"),
        AvgShippingDays=("Shipping Days", "mean")
    )
    shipping.to_csv(OUT / "shipping_performance.csv", index=False)

# Charts
plt.figure(figsize=(8,5))
category.sort_values("Sales").plot.barh(x="Category", y="Sales", legend=False)
plt.title("Sales by Category")
plt.tight_layout()
plt.savefig(OUT / "01_sales_by_category.png")
plt.close()

plt.figure(figsize=(8,5))
subcat.sort_values("Profit").plot.barh(x="Sub-Category", y="Profit", legend=False)
plt.title("Profit by Sub-Category")
plt.tight_layout()
plt.savefig(OUT / "02_profit_by_subcategory.png")
plt.close()

if "monthly" in locals():
    plt.figure(figsize=(10,5))
    plt.plot(monthly["Month"], monthly["Sales"], label="Sales")
    plt.plot(monthly["Month"], monthly["Profit"], label="Profit")
    plt.xticks(rotation=45, ha="right")
    plt.title("Monthly Sales & Profit")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "03_monthly_sales_profit.png")
    plt.close()

print("Analysis complete. Outputs saved to:", OUT)
