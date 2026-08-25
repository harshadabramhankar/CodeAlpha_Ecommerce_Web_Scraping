import os
import re
import pandas as pd


# ============================================================
# CODEALPHA TASK 1
# DATA CLEANING AND PREPROCESSING
# ============================================================

INPUT_FILE = "data/raw/books_raw.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "books_cleaned.csv"
)


# ============================================================
# 1. CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

print("=" * 70)
print("CODEALPHA TASK 1 - DATA CLEANING")
print("=" * 70)

print("\nLoading raw dataset...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8"
)

print("Raw dataset loaded successfully!")

print("\nOriginal shape:")
print(df.shape)


# ============================================================
# 3. DISPLAY ORIGINAL PRICE VALUES
# ============================================================

print("\nOriginal price examples:")

print(
    df["price"].head(10).to_string(index=False)
)


# ============================================================
# 4. REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print(
    "\nDuplicate rows found:",
    duplicate_count
)

if duplicate_count > 0:
    df = df.drop_duplicates()


# ============================================================
# 5. CLEAN PRODUCT NAME
# ============================================================

df["product_name"] = (
    df["product_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# 6. CLEAN PRICE
# ============================================================

# Convert price to string
price_text = (
    df["price"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Extract the first numeric value from each price.
# This works with formats such as:
# £51.77
# Â£51.77
# 51.77
# $51.77
# ₹51.77

df["price"] = (
    price_text
    .str.extract(
        r"([0-9]+(?:\.[0-9]+)?)",
        expand=False
    )
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# ============================================================
# 7. CLEAN RATING
# ============================================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)


# ============================================================
# 8. CLEAN AVAILABILITY
# ============================================================

df["availability"] = (
    df["availability"]
    .fillna("")
    .astype(str)
    .str.replace(
        r"\s+",
        " ",
        regex=True
    )
    .str.strip()
)


# ============================================================
# 9. CLEAN PRODUCT URL
# ============================================================

df["product_url"] = (
    df["product_url"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# 10. CONVERT DATE
# ============================================================

df["scraped_date"] = pd.to_datetime(
    df["scraped_date"],
    errors="coerce"
)


# ============================================================
# 11. SHOW CLEANED PRICE EXAMPLES
# ============================================================

print("\nCleaned price examples:")

print(
    df["price"].head(10).to_string(index=False)
)


# ============================================================
# 12. VALIDATE PRICE
# ============================================================

invalid_price_count = df["price"].isna().sum()

print(
    "\nInvalid price values:",
    invalid_price_count
)


# ============================================================
# 13. VALIDATE RATINGS
# ============================================================

invalid_rating_count = df["rating"].isna().sum()

print(
    "Invalid rating values:",
    invalid_rating_count
)


# ============================================================
# 14. REMOVE INVALID REQUIRED DATA
# ============================================================

before_cleaning = len(df)

df = df.dropna(
    subset=[
        "product_name",
        "price",
        "rating",
        "scraped_date"
    ]
)

df = df[
    (df["product_name"] != "") &
    (df["product_url"] != "")
]

after_cleaning = len(df)

print(
    "\nRows removed during cleaning:",
    before_cleaning - after_cleaning
)


# ============================================================
# 15. VALIDATE RATING RANGE
# ============================================================

invalid_rating_range = ~df["rating"].between(
    1,
    5
)

print(
    "Ratings outside 1-5:",
    invalid_rating_range.sum()
)

df = df[
    ~invalid_rating_range
]


# ============================================================
# 16. VALIDATE PRICE
# ============================================================

invalid_price_range = df["price"] <= 0

print(
    "Prices <= 0:",
    invalid_price_range.sum()
)

df = df[
    ~invalid_price_range
]


# ============================================================
# 17. RESET INDEX
# ============================================================

df = df.reset_index(
    drop=True
)


# ============================================================
# 18. FINAL MISSING VALUE CHECK
# ============================================================

print("\nMissing values after cleaning:")

print(
    df.isnull().sum()
)


# ============================================================
# 19. FINAL DUPLICATE CHECK
# ============================================================

print("\nDuplicate rows after cleaning:")

print(
    df.duplicated().sum()
)


# ============================================================
# 20. DATA TYPES
# ============================================================

print("\nFinal data types:")

print(
    df.dtypes
)


# ============================================================
# 21. FINAL DATASET SHAPE
# ============================================================

print("\nFinal cleaned dataset shape:")

print(
    df.shape
)


# ============================================================
# 22. PREVIEW
# ============================================================

print("\nCleaned dataset preview:")

print(
    df.head(10).to_string(index=False)
)


# ============================================================
# 23. SAVE CLEAN DATASET
# ============================================================

# Make sure the previous file is not blocking the new file.
if os.path.exists(OUTPUT_FILE):
    try:
        os.remove(OUTPUT_FILE)
    except PermissionError:
        print(
            "\nERROR: books_cleaned.csv is open."
        )
        print(
            "Close it in Excel/VS Code and run the script again."
        )
        raise SystemExit


df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 24. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nCleaned dataset saved to:"
)

print(
    OUTPUT_FILE
)

print(
    "\nFinal rows:",
    len(df)
)

print(
    "Final columns:",
    len(df.columns)
)