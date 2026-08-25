# ============================================================
# CODEALPHA TASK 1
# E-COMMERCE PRODUCT INTELLIGENCE
# EXPLORATORY DATA ANALYSIS
# ============================================================

import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/books_cleaned.csv"

OUTPUT_DIR = "outputs"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("CODEALPHA TASK 1 - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")

print("\nDataset Shape:")
print(df.shape)


# ============================================================
# 3. BASIC DATA PREPARATION
# ============================================================

# Convert date
df["scraped_date"] = pd.to_datetime(
    df["scraped_date"],
    errors="coerce"
)

# Make sure numeric columns are numeric
df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

# Clean text columns
df["product_name"] = (
    df["product_name"]
    .astype(str)
    .str.strip()
)

df["availability"] = (
    df["availability"]
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

df["product_url"] = (
    df["product_url"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 4. DATASET OVERVIEW
# ============================================================

print("\n" + "=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)

print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nColumns:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# 5. STATISTICAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("STATISTICAL SUMMARY")
print("=" * 70)

print(df.describe())


# ============================================================
# 6. BUSINESS QUESTIONS
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS QUESTIONS")
print("=" * 70)

questions = [
    "1. What is the average, minimum and maximum book price?",
    "2. How are book prices distributed?",
    "3. Which rating is most common?",
    "4. What percentage of books receive high ratings?",
    "5. Is there a relationship between price and rating?",
    "6. Which books are the most expensive?",
    "7. Which books are the cheapest?",
    "8. Which rating category has the highest average price?",
    "9. What is the availability distribution?",
    "10. What are the major business insights from the product catalogue?"
]

for question in questions:
    print(question)


# ============================================================
# 7. KEY PERFORMANCE INDICATORS
# ============================================================

total_books = len(df)

average_price = df["price"].mean()
median_price = df["price"].median()
minimum_price = df["price"].min()
maximum_price = df["price"].max()

average_rating = df["rating"].mean()
median_rating = df["rating"].median()

price_std = df["price"].std()

price_rating_correlation = df[
    ["price", "rating"]
].corr().loc["price", "rating"]


print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print("Total Books:", total_books)
print("Average Price:", round(average_price, 2))
print("Median Price:", round(median_price, 2))
print("Minimum Price:", round(minimum_price, 2))
print("Maximum Price:", round(maximum_price, 2))
print("Price Standard Deviation:", round(price_std, 2))
print("Average Rating:", round(average_rating, 2))
print("Median Rating:", round(median_rating, 2))
print(
    "Price-Rating Correlation:",
    round(price_rating_correlation, 3)
)


# ============================================================
# 8. PRICE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PRICE ANALYSIS")
print("=" * 70)

print("\nPrice Statistics:")

print("Mean:", round(df["price"].mean(), 2))
print("Median:", round(df["price"].median(), 2))
print("Minimum:", round(df["price"].min(), 2))
print("Maximum:", round(df["price"].max(), 2))

print("\nMost expensive books:")

most_expensive = (
    df.sort_values(
        by="price",
        ascending=False
    )
    .head(10)
)

print(
    most_expensive[
        [
            "product_name",
            "price",
            "rating"
        ]
    ].to_string(index=False)
)

print("\nCheapest books:")

cheapest = (
    df.sort_values(
        by="price",
        ascending=True
    )
    .head(10)
)

print(
    cheapest[
        [
            "product_name",
            "price",
            "rating"
        ]
    ].to_string(index=False)
)


# ============================================================
# 9. CREATE PRICE CATEGORY
# ============================================================

try:

    df["price_category"] = pd.qcut(
        df["price"],
        q=3,
        labels=[
            "Low Price",
            "Medium Price",
            "High Price"
        ],
        duplicates="drop"
    )

except ValueError:

    df["price_category"] = "Price Category"


print("\nPrice Category Distribution:")

print(
    df["price_category"]
    .value_counts()
)


# ============================================================
# 10. RATING ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RATING ANALYSIS")
print("=" * 70)

rating_counts = (
    df["rating"]
    .value_counts()
    .sort_index()
)

print("\nRating Counts:")
print(rating_counts)

rating_percentages = (
    df["rating"]
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

print("\nRating Percentages:")
print(rating_percentages.round(2))


# High-rated classification

df["rating_category"] = np.where(
    df["rating"] >= 4,
    "High Rated",
    "Standard Rated"
)

print("\nRating Category:")
print(
    df["rating_category"]
    .value_counts()
)

print("\nRating Category Percentage:")
print(
    (
        df["rating_category"]
        .value_counts(normalize=True)
        * 100
    ).round(2)
)


# ============================================================
# 11. AVERAGE PRICE BY RATING
# ============================================================

average_price_by_rating = (
    df.groupby("rating", observed=True)["price"]
    .mean()
    .round(2)
)

print("\n" + "=" * 70)
print("AVERAGE PRICE BY RATING")
print("=" * 70)

print(average_price_by_rating)


# ============================================================
# 12. AVAILABILITY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("AVAILABILITY ANALYSIS")
print("=" * 70)

availability_counts = (
    df["availability"]
    .value_counts()
)

print("\nAvailability Counts:")
print(availability_counts)

availability_percentages = (
    df["availability"]
    .value_counts(normalize=True)
    * 100
)

print("\nAvailability Percentages:")
print(
    availability_percentages.round(2)
)


# ============================================================
# 13. PRICE VS RATING CORRELATION
# ============================================================

print("\n" + "=" * 70)
print("PRICE VS RATING ANALYSIS")
print("=" * 70)

correlation = df["price"].corr(
    df["rating"]
)

print(
    "Pearson correlation:",
    round(correlation, 3)
)

if correlation > 0.7:

    correlation_interpretation = (
        "Strong positive relationship"
    )

elif correlation > 0.3:

    correlation_interpretation = (
        "Moderate positive relationship"
    )

elif correlation > 0:

    correlation_interpretation = (
        "Weak positive relationship"
    )

elif correlation < -0.7:

    correlation_interpretation = (
        "Strong negative relationship"
    )

elif correlation < -0.3:

    correlation_interpretation = (
        "Moderate negative relationship"
    )

elif correlation < 0:

    correlation_interpretation = (
        "Weak negative relationship"
    )

else:

    correlation_interpretation = (
        "No meaningful linear relationship"
    )

print(
    "Interpretation:",
    correlation_interpretation
)


# ============================================================
# 14. CROSS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PRICE CATEGORY VS RATING CATEGORY")
print("=" * 70)

cross_analysis = pd.crosstab(
    df["price_category"],
    df["rating_category"]
)

print(cross_analysis)


# ============================================================
# 15. CREATE SUMMARY TABLE
# ============================================================

summary_table = pd.DataFrame({
    "Metric": [
        "Total Books",
        "Average Price",
        "Median Price",
        "Minimum Price",
        "Maximum Price",
        "Average Rating",
        "Median Rating",
        "Price-Rating Correlation"
    ],

    "Value": [
        total_books,
        round(average_price, 2),
        round(median_price, 2),
        round(minimum_price, 2),
        round(maximum_price, 2),
        round(average_rating, 2),
        round(median_rating, 2),
        round(price_rating_correlation, 3)
    ]
})

print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)

print(summary_table.to_string(index=False))

summary_table.to_csv(
    os.path.join(
        REPORT_DIR,
        "eda_summary.csv"
    ),
    index=False
)


# ============================================================
# 16. VISUALIZATION SETTINGS
# ============================================================

sns.set_theme(
    style="whitegrid"
)


# ============================================================
# 17. PRICE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="price",
    bins=30,
    kde=True
)

plt.title(
    "Distribution of Book Prices",
    fontsize=16
)

plt.xlabel("Price (£)")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "01_price_distribution.png"
    ),
    dpi=300
)



plt.close()


# ============================================================
# 18. PRICE BOX PLOT
# ============================================================

plt.figure(figsize=(10, 5))

sns.boxplot(
    x=df["price"]
)

plt.title(
    "Book Price Distribution and Outliers",
    fontsize=16
)

plt.xlabel("Price (£)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "01_price_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 19. RATING DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="rating"
)

plt.title(
    "Distribution of Book Ratings",
    fontsize=16
)

plt.xlabel("Rating")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "03_rating_distribution.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 20. AVERAGE PRICE BY RATING
# ============================================================

plt.figure(figsize=(8, 5))

sns.barplot(
    x=average_price_by_rating.index,
    y=average_price_by_rating.values
)

plt.title(
    "Average Price by Rating",
    fontsize=16
)

plt.xlabel("Rating")
plt.ylabel("Average Price (£)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "04_average_price_by_rating.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 21. PRICE VS RATING
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="rating",
    y="price"
)

plt.title(
    "Relationship Between Rating and Price",
    fontsize=16
)

plt.xlabel("Rating")
plt.ylabel("Price (£)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "05_price_vs_rating.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 22. TOP 10 MOST EXPENSIVE BOOKS
# ============================================================

plt.figure(figsize=(10, 7))

top_expensive = (
    df.sort_values(
        "price",
        ascending=False
    )
    .head(10)
)

sns.barplot(
    data=top_expensive,
    x="price",
    y="product_name"
)

plt.title(
    "Top 10 Most Expensive Books",
    fontsize=16
)

plt.xlabel("Price (£)")
plt.ylabel("Book")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "06_top_10_expensive_books.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 23. TOP 10 CHEAPEST BOOKS
# ============================================================

plt.figure(figsize=(10, 7))

top_cheap = (
    df.sort_values(
        "price",
        ascending=True
    )
    .head(10)
)

sns.barplot(
    data=top_cheap,
    x="price",
    y="product_name"
)

plt.title(
    "Top 10 Cheapest Books",
    fontsize=16
)

plt.xlabel("Price (£)")
plt.ylabel("Book")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "07_top_10_cheapest_books.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 24. PRICE CATEGORY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="price_category",
    order=[
        "Low Price",
        "Medium Price",
        "High Price"
    ]
)

plt.title(
    "Books by Price Category",
    fontsize=16
)

plt.xlabel("Price Category")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "08_price_category_distribution.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 25. RATING CATEGORY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="rating_category"
)

plt.title(
    "Books by Rating Category",
    fontsize=16
)

plt.xlabel("Rating Category")
plt.ylabel("Number of Books")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "09_rating_category_distribution.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 26. AVAILABILITY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="availability"
)

plt.title(
    "Book Availability Distribution",
    fontsize=16
)

plt.xlabel("Availability")
plt.ylabel("Number of Books")

plt.xticks(
    rotation=20
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "10_availability_distribution.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 27. CORRELATION HEATMAP
# ============================================================

numeric_columns = [
    "price",
    "rating"
]

correlation_matrix = df[
    numeric_columns
].corr()

plt.figure(figsize=(6, 5))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="Blues"
)

plt.title(
    "Price and Rating Correlation",
    fontsize=16
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "11_correlation_heatmap.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 28. RATING × PRICE CATEGORY HEATMAP
# ============================================================

rating_price_table = pd.crosstab(
    df["price_category"],
    df["rating"]
)

plt.figure(figsize=(8, 5))

sns.heatmap(
    rating_price_table,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title(
    "Price Category vs Rating",
    fontsize=16
)

plt.xlabel("Rating")
plt.ylabel("Price Category")

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "12_price_category_vs_rating.png"
    ),
    dpi=300
)

plt.show()

plt.close()


# ============================================================
# 29. BUSINESS INSIGHTS GENERATION
# ============================================================

most_common_rating = (
    rating_counts.idxmax()
)

most_common_rating_count = (
    rating_counts.max()
)

highest_average_rating_price = (
    average_price_by_rating.idxmax()
)

highest_average_rating_price_value = (
    average_price_by_rating.max()
)

most_common_availability = (
    availability_counts.idxmax()
)

most_common_availability_percent = (
    availability_percentages.max()
)

high_rated_percentage = (
    (
        df["rating_category"]
        == "High Rated"
    ).mean()
    * 100
)


# ============================================================
# 30. GENERATE BUSINESS REPORT
# ============================================================

report_file = os.path.join(
    REPORT_DIR,
    "business_insights.txt"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "CODEALPHA TASK 1 - "
        "E-COMMERCE PRODUCT INTELLIGENCE\n"
    )

    file.write(
        "=" * 65 + "\n\n"
    )

    file.write("DATASET OVERVIEW\n")
    file.write("-" * 65 + "\n")

    file.write(
        f"Total products analyzed: {total_books}\n"
    )

    file.write(
        f"Average price: £{average_price:.2f}\n"
    )

    file.write(
        f"Median price: £{median_price:.2f}\n"
    )

    file.write(
        f"Minimum price: £{minimum_price:.2f}\n"
    )

    file.write(
        f"Maximum price: £{maximum_price:.2f}\n"
    )

    file.write(
        f"Average rating: {average_rating:.2f}\n"
    )

    file.write(
        f"Most common rating: "
        f"{most_common_rating} "
        f"({most_common_rating_count} books)\n"
    )

    file.write(
        f"High-rated products: "
        f"{high_rated_percentage:.2f}%\n"
    )

    file.write(
        f"Most common availability status: "
        f"{most_common_availability} "
        f"({most_common_availability_percent:.2f}%)\n"
    )

    file.write(
        f"Price-rating correlation: "
        f"{correlation:.3f}\n\n"
    )

    file.write("KEY BUSINESS INSIGHTS\n")
    file.write("-" * 65 + "\n")

    file.write(
        "1. Pricing:\n"
        f"The average product price is "
        f"£{average_price:.2f}, while the median "
        f"price is £{median_price:.2f}. "
        "This provides a benchmark for the overall "
        "catalogue pricing level.\n\n"
    )

    file.write(
        "2. Customer Rating:\n"
        f"The most common customer rating is "
        f"{most_common_rating} stars. "
        f"{high_rated_percentage:.2f}% of products "
        "are classified as high-rated products "
        "(4 or 5 stars).\n\n"
    )

    file.write(
        "3. Price and Rating:\n"
        f"The price-rating correlation is "
        f"{correlation:.3f}. "
        f"The observed relationship is classified "
        f"as {correlation_interpretation.lower()}. "
        "Correlation should not be interpreted as "
        "proof of causation.\n\n"
    )

    file.write(
        "4. Availability:\n"
        f"The most common availability status is "
        f"'{most_common_availability}', representing "
        f"{most_common_availability_percent:.2f}% "
        "of the catalogue.\n\n"
    )

    file.write(
        "5. Pricing Segmentation:\n"
        "The catalogue was divided into Low, Medium "
        "and High Price groups using quantile-based "
        "segmentation. This allows comparison of "
        "products across different pricing levels.\n\n"
    )

    file.write(
        "BUSINESS RECOMMENDATIONS\n"
    )

    file.write("-" * 65 + "\n")

    file.write(
        "1. Use the median and average price as "
        "benchmarks when evaluating competitive "
        "pricing strategies.\n"
    )

    file.write(
        "2. Monitor highly rated products closely "
        "because they may represent strong customer "
        "acceptance and potential promotional opportunities.\n"
    )

    file.write(
        "3. Compare price and rating together rather "
        "than using price alone when evaluating "
        "product positioning.\n"
    )

    file.write(
        "4. Track availability continuously because "
        "product availability can affect customer "
        "experience and potential revenue.\n"
    )

    file.write(
        "5. Repeat the scraping and analysis periodically "
        "to monitor pricing and catalogue changes over time.\n"
    )


# ============================================================
# 31. SAVE ENRICHED DATASET
# ============================================================

enriched_file = (
    "data/processed/books_analysis_ready.csv"
)

df.to_csv(
    enriched_file,
    index=False
)


# ============================================================
# 32. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFiles generated:")

print(
    "1. Analysis-ready dataset:",
    enriched_file
)

print(
    "2. Summary report:",
    os.path.join(
        REPORT_DIR,
        "eda_summary.csv"
    )
)

print(
    "3. Business insights:",
    report_file
)

print(
    "4. Charts folder:",
    CHART_DIR
)

print("\nTotal charts generated: 12")

print("\nFinal dataset shape:")
print(df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nKey Results:")
print(
    f"Average Price: £{average_price:.2f}"
)

print(
    f"Average Rating: {average_rating:.2f}"
)

print(
    f"Price-Rating Correlation: {correlation:.3f}"
)

print(
    f"High-Rated Products: "
    f"{high_rated_percentage:.2f}%"
)

print(
    "\nEDA and business analysis completed!"
)