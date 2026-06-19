#  Sales Data Analysis

A data analysis pipeline built with **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn** that reads CSV data, cleans missing values, generates summary statistics, and produces publication-ready charts.

---

## Skills Demonstrated

| Skill | Usage |
|---|---|
| **Pandas** | `read_csv`, `groupby`, `fillna`, `describe`, date parsing |
| **NumPy** | Per-group aggregations (`sum`, `mean`, `std`, `max`) |
| **Data Cleaning** | Missing value detection, median imputation, derived columns |
| **Data Visualization** | 4-panel dashboard (bar, line, pie, boxplot) + correlation heatmap |

---

## Features

-  **Read CSV data** — parses dates, infers dtypes automatically
-  **Clean missing values** — fills gaps with per-product medians; reports before/after
-  **Summary statistics** — numeric overview, revenue by product/region, return rate, monthly trend
-  **Charts** — saves a 4-panel dashboard and a correlation heatmap to `charts/`

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/sales-data-analysis.git
cd sales-data-analysis

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

---

## Usage

```bash
# Run with the included sample dataset
python data_analysis.py

# Kaggle / Colab — no changes needed, DEMO_MODE is on by default
```

> **Kaggle users:** Use `data_analysis_kaggle.py` — data is embedded inline, no CSV upload needed.

---

## Project Structure

```
sales-data-analysis/
│
├── data_analysis.py          # Main analysis script (local)
├── data_analysis_kaggle.py   # Kaggle/Colab version (inline data)
├── sales_data.csv            # Sample dataset (40 rows)
├── charts/
│   ├── dashboard.png         # 4-panel chart output
│   └── correlation_heatmap.png
└── README.md
```

---

## Sample Output

```
======================================================
  STEP 1 · LOAD DATA
======================================================
  ✔  Loaded 40 rows × 9 columns
  Columns: ['date', 'region', 'product', 'sales', 'units', ...]

======================================================
  STEP 2 · CLEAN DATA
======================================================
  Missing values before cleaning:
    sales    7
  ✔  Filled 7 missing 'sales' values with per-product median
  ✔  Added derived columns: revenue, month, is_returned
  Missing values after cleaning: 0

======================================================
  STEP 3 · SUMMARY STATISTICS
======================================================
  [B] Revenue by product (NumPy):
    Laptop        total=14,355.00  mean=1,435.50  std=88.32
    Phone         total= 5,992.00  mean=  748.99  std=52.14
    Tablet        total= 2,842.00  mean=  473.67  std=28.91
    Headphones    total=   912.00  mean=  182.40  std=13.22

  [D] Overall return rate: 12.5%

======================================================
  STEP 4 · CHARTS
======================================================
  ✔  Dashboard saved → charts/dashboard.png
  ✔  Heatmap saved   → charts/correlation_heatmap.png
```

**Dashboard preview:** 4-panel chart covering revenue by product (bar), monthly trend (line), regional share (pie), and price distribution (boxplot).

---

## Dataset

The included `sales_data.csv` contains 40 rows of synthetic retail data across 4 products, 4 regions, and 4 months (Jan–Apr 2024), with intentional missing values for cleaning demonstration.

| Column | Type | Description |
|---|---|---|
| `date` | date | Transaction date |
| `region` | str | North / South / East / West |
| `product` | str | Laptop / Phone / Tablet / Headphones |
| `sales` | float | Unit sale price (some missing) |
| `units` | int | Quantity sold |
| `discount_pct` | float | Discount percentage |
| `returned` | str | Yes / No |

---

## Dependencies

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
```
