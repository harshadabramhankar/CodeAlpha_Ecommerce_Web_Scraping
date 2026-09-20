import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load data
df = pd.read_csv("books_dataset.csv")

# Set executive styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig = plt.figure(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor("#f8f9fa")

# Create a 2x2 grid with space for a top header
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25, top=0.88, bottom=0.08)

# Title & Subtitle
fig.suptitle(
    "E-COMMERCE CATALOG INTELLIGENCE DASHBOARD",
    fontsize=20,
    fontweight="bold",
    color="#1a202c",
    y=0.96,
)
plt.figtext(
    0.5,
    0.915,
    "Executive Pricing & Portfolio Health Analysis | Derived from Automated Catalog Scraping",
    ha="center",
    fontsize=11,
    color="#718096",
)

# -------------------------------------------------------------
# Chart 1: Price Tier Segmentation (Bar Chart)
# -------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
price_bins = [0, 20, 40, 60]
labels = ["Budget (£0-£20)", "Mid-Tier (£20-£40)", "Premium (£40-£60)"]
df["Price_Category"] = pd.cut(df["Price_GBP"], bins=price_bins, labels=labels)
tier_counts = df["Price_Category"].value_counts().reindex(labels)

bars = ax1.bar(
    tier_counts.index,
    tier_counts.values,
    color=["#3182ce", "#4299e1", "#63b3ed"],
    edgecolor="#2b6cb0",
    width=0.55,
)
ax1.set_title("1. Catalog Inventory by Price Tier", fontsize=12, fontweight="bold", pad=10)
ax1.set_ylabel("Book Count", fontsize=10)
for bar in bars:
    yval = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 1,
        f"{int(yval)}",
        ha="center",
        va="bottom",
        fontweight="bold",
    )

# -------------------------------------------------------------
# Chart 2: Cumulative Rating Share (Donut Chart)
# -------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
rating_counts = df["Rating"].value_counts()[["One", "Two", "Three", "Four", "Five"]]
colors = ["#cbd5e0", "#a0aec0", "#718096", "#4a5568", "#2d3748"]
wedges, texts, autotexts = ax2.pie(
    rating_counts,
    labels=rating_counts.index,
    autopct="%1.0f%%",
    startangle=140,
    colors=colors,
    pctdistance=0.75,
    wedgeprops=dict(width=0.45, edgecolor="w"),
)
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight("bold")
ax2.set_title("2. Customer Rating Tier Share", fontsize=12, fontweight="bold", pad=10)

# -------------------------------------------------------------
# Chart 3: Average Price by Rating Tier (Horizontal Bar)
# -------------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 0])
avg_price_rating = (
    df.groupby("Rating")["Price_GBP"]
    .mean()
    .reindex(["One", "Two", "Three", "Four", "Five"])
)
ax3.barh(avg_price_rating.index, avg_price_rating.values, color="#38a169", height=0.55)
ax3.set_title("3. Average Retail Price (£) per Rating Category", fontsize=12, fontweight="bold", pad=10)
ax3.set_xlabel("Average Price (£)", fontsize=10)
for i, v in enumerate(avg_price_rating.values):
    ax3.text(v + 0.5, i, f"£{v:.2f}", va="center", fontweight="bold")
ax3.set_xlim(0, max(avg_price_rating.values) + 8)

# -------------------------------------------------------------
# Chart 4: Top 5 Highest Priced Items (Storytelling Spotlight)
# -------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 1])
top5 = df.sort_values(by="Price_GBP", ascending=True).tail(5)
# Shorten long titles for clean display
truncated_titles = [t[:28] + "..." if len(t) > 28 else t for t in top5["Book_Title"]]
ax4.barh(truncated_titles, top5["Price_GBP"], color="#dd6b20", height=0.55)
ax4.set_title("4. Top 5 Premium Products (£)", fontsize=12, fontweight="bold", pad=10)
ax4.set_xlabel("Price (£)", fontsize=10)
for i, v in enumerate(top5["Price_GBP"]):
    ax4.text(v + 0.5, i, f"£{v:.2f}", va="center", fontweight="bold")
ax4.set_xlim(0, max(top5["Price_GBP"]) + 8)

# Export dashboard
output_dashboard = "task3_business_dashboard.png"
plt.savefig(output_dashboard, bbox_inches="tight")
print(f"\n[SUCCESS] Executive Dashboard exported to '{output_dashboard}'.")
plt.show()