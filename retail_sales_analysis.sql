-- Retail Sales & Profitability Analytics
-- Compatible with PostgreSQL-style SQL after importing the Excel data.

-- 1. Overall KPIs
SELECT
    SUM("Sales") AS total_sales,
    SUM("Profit") AS total_profit,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(SUM("Profit") / NULLIF(SUM("Sales"),0) * 100, 2) AS profit_margin_pct
FROM superstore;

-- 2. Sales and profit by category
SELECT
    "Category",
    SUM("Sales") AS sales,
    SUM("Profit") AS profit,
    ROUND(SUM("Profit") / NULLIF(SUM("Sales"),0) * 100, 2) AS margin_pct
FROM superstore
GROUP BY "Category"
ORDER BY sales DESC;

-- 3. Sub-categories destroying profit
SELECT
    "Sub-Category",
    SUM("Sales") AS sales,
    SUM("Profit") AS profit
FROM superstore
GROUP BY "Sub-Category"
HAVING SUM("Profit") < 0
ORDER BY profit ASC;

-- 4. Regional performance
SELECT
    "Region",
    SUM("Sales") AS sales,
    SUM("Profit") AS profit
FROM superstore
GROUP BY "Region"
ORDER BY profit DESC;

-- 5. Discount vs profitability
SELECT
    "Category",
    ROUND(AVG("Discount"), 3) AS avg_discount,
    ROUND(AVG("Profit"), 2) AS avg_profit
FROM superstore
GROUP BY "Category"
ORDER BY avg_discount DESC;

-- 6. Top customers by sales
SELECT
    "Customer ID",
    "Customer Name",
    SUM("Sales") AS sales,
    SUM("Profit") AS profit
FROM superstore
GROUP BY "Customer ID", "Customer Name"
ORDER BY sales DESC
LIMIT 10;

-- 7. Shipping performance
SELECT
    "Ship Mode",
    COUNT(*) AS orders,
    ROUND(AVG("Shipping Days"), 2) AS avg_shipping_days
FROM superstore
GROUP BY "Ship Mode"
ORDER BY avg_shipping_days;
