import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Load the scraped dataset
df = pd.read_csv("books_dataset.csv")

print("=" * 60)
print("TASK 2: EXPLORATORY DATA ANALYSIS (EDA) REPORT")
print("=" * 60)

# --- 2. Explore Data Structure ---
print("\n[1] DATASET OVERVIEW & SHAPE:")
print(f"Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
print("\n[2] DATA TYPES & NULL VALUES:")
print(df.info())

print("\n[3] SUMMARY STATISTICS (Price & Ratings):")
print(df.describe())

# --- 3. Identify Outliers & Anomalies ---
q1 = df["Price_GBP"].quantile(0.25)
q3 = df["Price_GBP"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df[
    (df["Price_GBP"] < lower_bound) | (df["Price_GBP"] > upper_bound)
]
print(
    f"\n[4] ANOMALY DETECTION: Found {len(outliers)} price outliers outside [{lower_bound:.2f}, {upper_bound:.2f}]."
)

# --- 4. Hypothesis Testing ---
# Hypothesis: Higher-rated books command higher average prices.
mean_price_by_rating = (
    df.groupby("Rating_Numeric")["Price_GBP"]
    .agg(["mean", "median", "count"])
    .reset_index()
)
print("\n[5] HYPOTHESIS TEST: Price Distribution by Rating:")
print(mean_price_by_rating)

# Top 5 most expensive books
print("\n[6] TOP 5 MOST EXPENSIVE BOOKS:")
print(df.sort_values(by="Price_GBP", ascending=False)[["Book_Title", "Price_GBP", "Rating"]].head())

# --- 5. High-Impact Visualizations ---
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Visual 1: Price Distribution (Histogram + KDE)
sns.histplot(df["Price_GBP"], kde=True, ax=axes[0, 0], color="#2b5c8f", bins=15)
axes[0, 0].set_title("Price Distribution (£)", fontsize=12, fontweight="bold")
axes[0, 0].set_xlabel("Price in GBP")

# Visual 2: Rating Frequency Breakdown (Bar Chart)
sns.countplot(
    x="Rating",
    data=df,
    ax=axes[0, 1],
    order=["One", "Two", "Three", "Four", "Five"],
    palette="Blues_r",
)
axes[0, 1].set_title("Book Count by Star Rating", fontsize=12, fontweight="bold")
axes[0, 1].set_xlabel("Rating Tier")

# Visual 3: Price vs Rating Relationship (Boxplot)
sns.boxplot(
    x="Rating_Numeric",
    y="Price_GBP",
    data=df,
    ax=axes[1, 0],
    palette="Blues",
)
axes[1, 0].set_title("Price Spread across Star Ratings", fontsize=12, fontweight="bold")
axes[1, 0].set_xlabel("Numeric Rating (1-5)")
axes[1, 0].set_ylabel("Price (£)")

# Visual 4: Stock Availability Distribution
stock_counts = df["Stock_Status"].value_counts()
axes[1, 1].pie(
    stock_counts,
    labels=stock_counts.index,
    autopct="%1.1f%%",
    colors=["#52b788"],
    startangle=90,
)
axes[1, 1].set_title("Inventory Stock Health", fontsize=12, fontweight="bold")

plt.tight_layout()
chart_filename = "eda_analysis_charts.png"
plt.savefig(chart_filename, dpi=300)
print(f"\n[7] All 4 analysis charts exported to '{chart_filename}'!")
plt.show()