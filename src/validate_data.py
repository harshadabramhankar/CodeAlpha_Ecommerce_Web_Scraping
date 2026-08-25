import pandas as pd


file_path = "data/processed/books_cleaned.csv"

df = pd.read_csv(file_path)


print("===================================")
print("DATA VALIDATION REPORT")
print("===================================")


# Dataset size

print("\nDataset shape:")
print(df.shape)


# Missing values

print("\nMissing values:")
print(df.isnull().sum())


# Duplicate rows

print("\nDuplicate rows:")
print(df.duplicated().sum())


# Price validation

print("\nPrice validation:")

print(
    "Minimum price:",
    df["price"].min()
)

print(
    "Maximum price:",
    df["price"].max()
)

print(
    "Average price:",
    round(df["price"].mean(), 2)
)


# Rating validation

print("\nRating validation:")

print(
    "Minimum rating:",
    df["rating"].min()
)

print(
    "Maximum rating:",
    df["rating"].max()
)

print(
    "\nRating distribution:"
)

print(
    df["rating"].value_counts().sort_index()
)


# Availability

print("\nAvailability:")

print(
    df["availability"].value_counts()
)


# Data types

print("\nData types:")

print(df.dtypes)


print("\n===================================")
print("VALIDATION COMPLETED")
print("===================================")