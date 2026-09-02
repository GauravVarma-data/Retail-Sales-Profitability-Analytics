import streamlit as st
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "superstore_sales.xlsx"

st.set_page_config(page_title="Retail Sales Analytics", layout="wide")

df = pd.read_excel(DATA)
df.columns = [str(c).strip() for c in df.columns]

for col in ["Order Date", "Ship Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

if {"Order Date", "Ship Date"}.issubset(df.columns):
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

st.title("Retail Sales & Profitability Analytics")
st.caption("Portfolio project | Superstore retail dataset")

# Filters
years = sorted(df["Order Date"].dt.year.dropna().unique()) if "Order Date" in df else []
year = st.selectbox("Year", ["All"] + [int(y) for y in years])

view = df.copy()
if year != "All":
    view = view[view["Order Date"].dt.year == year]

sales = view["Sales"].sum()
profit = view["Profit"].sum()
orders = view["Order ID"].nunique()
margin = profit / sales if sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sales", f"${sales:,.0f}")
c2.metric("Profit", f"${profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Profit Margin", f"{margin:.1%}")

st.subheader("Category Performance")
cat = view.groupby("Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
st.bar_chart(cat.set_index("Category")[["Sales", "Profit"]])

st.subheader("Regional Performance")
reg = view.groupby("Region", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
st.dataframe(reg.sort_values("Profit", ascending=False), use_container_width=True)

st.subheader("Most & Least Profitable Sub-Categories")
sub = view.groupby("Sub-Category", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
st.dataframe(sub.sort_values("Profit"), use_container_width=True)

st.subheader("Customer Explorer")
if "Customer Name" in view.columns:
    customer = view.groupby(["Customer ID", "Customer Name"], as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=False)
    st.dataframe(customer.head(50), use_container_width=True)

st.subheader("Discount & Profitability")
disc = view.groupby("Discount", as_index=False).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)
st.dataframe(disc, use_container_width=True)
