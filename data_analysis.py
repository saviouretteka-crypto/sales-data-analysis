"""
Data Analysis Project
=====================
Demonstrates: Pandas, NumPy, Data Cleaning, Data Visualization

Features:
  - Read CSV data
  - Clean missing values
  - Generate summary statistics
  - Create charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Configuration ────────────────────────────────────────────────────────────
CSV_FILE   = "sales_data.csv"
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "figure.autolayout": True})


# ── 1. READ DATA ──────────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    print("\n" + "=" * 55)
    print("  STEP 1 · LOAD DATA")
    print("=" * 55)

    df = pd.read_csv(filepath, parse_dates=["date"])
    print(f"  ✔  Loaded {len(df):,} rows × {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}\n")
    print(df.head(5).to_string(index=False))
    return df


# ── 2. CLEAN DATA ─────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 55)
    print("  STEP 2 · CLEAN DATA")
    print("=" * 55)

    # --- Missing values report
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    print(f"\n  Missing values before cleaning:")
    print(missing.to_string())

    # --- Strategy A: fill numeric 'sales' with median per product
    median_by_product = df.groupby("product")["sales"].transform("median")
    filled_count = df["sales"].isnull().sum()
    df["sales"] = df["sales"].fillna(median_by_product)
    print(f"\n  ✔  Filled {filled_count} missing 'sales' values with per-product median")

    # --- Strategy B: fill numeric 'units' with 1 (sensible floor)
    units_filled = df["units"].isnull().sum()
    df["units"] = df["units"].fillna(1).astype(int)
    print(f"  ✔  Filled {units_filled} missing 'units' values with 1")

    # --- Derive extra columns
    df["revenue"]      = df["sales"] * df["units"] * (1 - df["discount_pct"] / 100)
    df["month"]        = df["date"].dt.to_period("M").astype(str)
    df["is_returned"]  = df["returned"].map({"Yes": True, "No": False})

    print(f"\n  Missing values after cleaning: {df.isnull().sum().sum()}")
    print(f"  ✔  Added derived columns: revenue, month, is_returned")

    # --- Basic dtype summary
    print("\n  DataFrame info:")
    df.info(verbose=False, memory_usage=False)
    return df


# ── 3. SUMMARY STATISTICS ────────────────────────────────────────────────────
def summary_statistics(df: pd.DataFrame) -> None:
    print("\n" + "=" * 55)
    print("  STEP 3 · SUMMARY STATISTICS")
    print("=" * 55)

    # --- Overall numeric summary
    print("\n  [A] Numeric overview:")
    num_cols = ["sales", "units", "discount_pct", "revenue"]
    print(df[num_cols].describe().round(2).to_string())

    # --- Sales by product (NumPy aggregations)
    print("\n  [B] Revenue by product (NumPy):")
    for product, grp in df.groupby("product")["revenue"]:
        arr = grp.values
        print(f"    {product:<12}  "
              f"total={np.sum(arr):>8,.2f}  "
              f"mean={np.mean(arr):>7,.2f}  "
              f"std={np.std(arr):>7,.2f}  "
              f"max={np.max(arr):>8,.2f}")

    # --- Sales by region
    print("\n  [C] Revenue by region:")
    region_rev = (df.groupby("region")["revenue"]
                    .agg(total="sum", mean="mean", orders="count")
                    .sort_values("total", ascending=False))
    print(region_rev.round(2).to_string())

    # --- Return rate
    return_rate = df["is_returned"].mean() * 100
    print(f"\n  [D] Overall return rate: {return_rate:.1f}%")

    # --- Monthly trend
    print("\n  [E] Monthly revenue trend:")
    monthly = df.groupby("month")["revenue"].sum().reset_index()
    for _, row in monthly.iterrows():
        bar = "█" * int(row["revenue"] / 500)
        print(f"    {row['month']}  {bar}  ${row['revenue']:,.2f}")


# ── 4. VISUALIZATIONS ────────────────────────────────────────────────────────
def create_charts(df: pd.DataFrame) -> None:
    print("\n" + "=" * 55)
    print("  STEP 4 · CHARTS")
    print("=" * 55)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Sales Data Analysis Dashboard", fontsize=16, fontweight="bold", y=1.01)

    # ── Chart 1: Revenue by Product (bar) ────────────────────────────────────
    ax1 = axes[0, 0]
    prod_rev = df.groupby("product")["revenue"].sum().sort_values(ascending=False)
    bars = ax1.bar(prod_rev.index, prod_rev.values,
                   color=sns.color_palette("muted", len(prod_rev)))
    ax1.set_title("Total Revenue by Product")
    ax1.set_xlabel("Product")
    ax1.set_ylabel("Revenue ($)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    for bar, val in zip(bars, prod_rev.values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
                 f"${val:,.0f}", ha="center", va="bottom", fontsize=8)

    # ── Chart 2: Monthly Revenue Trend (line) ────────────────────────────────
    ax2 = axes[0, 1]
    monthly = df.groupby("month")["revenue"].sum()
    ax2.plot(monthly.index, monthly.values, marker="o", linewidth=2,
             color=sns.color_palette("muted")[1], markersize=7)
    ax2.fill_between(monthly.index, monthly.values, alpha=0.15,
                     color=sns.color_palette("muted")[1])
    ax2.set_title("Monthly Revenue Trend")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Revenue ($)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax2.tick_params(axis="x", rotation=30)

    # ── Chart 3: Revenue by Region (pie) ─────────────────────────────────────
    ax3 = axes[1, 0]
    region_rev = df.groupby("region")["revenue"].sum()
    ax3.pie(region_rev.values, labels=region_rev.index,
            autopct="%1.1f%%", startangle=140,
            colors=sns.color_palette("pastel", len(region_rev)))
    ax3.set_title("Revenue Share by Region")

    # ── Chart 4: Sales Distribution by Product (box) ─────────────────────────
    ax4 = axes[1, 1]
    order = df.groupby("product")["sales"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="product", y="sales", order=order,
                palette="muted", ax=ax4)
    ax4.set_title("Sales Distribution by Product")
    ax4.set_xlabel("Product")
    ax4.set_ylabel("Unit Sale Price ($)")
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.tight_layout()
    chart_path = os.path.join(OUTPUT_DIR, "dashboard.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()
    print(f"  ✔  Dashboard saved → {chart_path}")

    # ── Bonus: Correlation heatmap ────────────────────────────────────────────
    fig2, ax5 = plt.subplots(figsize=(6, 5))
    corr_cols = ["sales", "units", "discount_pct", "revenue", "customer_age"]
    corr = df[corr_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, linewidths=0.5, ax=ax5)
    ax5.set_title("Correlation Heatmap")
    heatmap_path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    plt.savefig(heatmap_path, bbox_inches="tight")
    plt.close()
    print(f"  ✔  Heatmap saved      → {heatmap_path}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    df = load_data(CSV_FILE)
    df = clean_data(df)
    summary_statistics(df)
    create_charts(df)

    print("\n" + "=" * 55)
    print("  ✅  Analysis complete!  Charts are in ./charts/")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
