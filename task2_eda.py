# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('books_dataset.csv')
print('\n--- TASK 2: EXPLORATORY DATA ANALYSIS ---')
print(f'Shape: {df.shape}')
print(df.describe())

# Anomaly check
q1 = df['Price_GBP'].quantile(0.25)
q3 = df['Price_GBP'].quantile(0.75)
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df['Price_GBP'] < lower) | (df['Price_GBP'] > upper)]
print(f'Price Outliers Found: {len(outliers)}')

# Hypothesis test
print('\nAverage Price by Rating:')
print(df.groupby('Rating_Numeric')['Price_GBP'].mean())

# Visualizations
sns.set_theme(style='whitegrid')
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.histplot(df['Price_GBP'], kde=True, ax=axes[0, 0], color='#2b5c8f')
axes[0, 0].set_title('Price Distribution (GBP)')

sns.countplot(x='Rating', data=df, ax=axes[0, 1], order=['One', 'Two', 'Three', 'Four', 'Five'], palette='Blues_r')
axes[0, 1].set_title('Book Volume by Rating')

sns.boxplot(x='Rating_Numeric', y='Price_GBP', data=df, ax=axes[1, 0], palette='Blues')
axes[1, 0].set_title('Price Spread by Star Rating')

stock_counts = df['Stock_Status'].value_counts()
axes[1, 1].pie(stock_counts, labels=stock_counts.index, autopct='%1.1f%%', colors=['#52b788'])
axes[1, 1].set_title('Stock Availability')

plt.tight_layout()
plt.savefig('eda_analysis_charts.png', dpi=300)
print('\n[SUCCESS] eda_analysis_charts.png generated successfully.')