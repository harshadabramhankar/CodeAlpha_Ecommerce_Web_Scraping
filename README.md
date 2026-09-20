# Data Analytics Internship - Three-Stage Analytics Pipeline

## Project Overview
This repository contains an end-to-end data analytics pipeline demonstrating automated data extraction, statistical exploratory data analysis (EDA), and executive visual reporting.

---

### Task 1: Web Scraping Pipeline (`task1_web_scraping.py`)
* **Objective:** Extract structured multi-page catalog records from public e-commerce listings.
* **Tech Stack:** Python 3.11, BeautifulSoup4, Requests, Pandas.
* **Deliverable:** `books_dataset.csv` (contains book titles, numeric ratings, prices, and stock statuses).

---

### Task 2: Exploratory Data Analysis (`task2_eda.py`)
* **Objective:** Data profiling, distribution analysis, outlier detection, and hypothesis validation.
* **Hypothesis Tested:** "Higher customer ratings correspond to higher average prices."
  * **Result:** Disproved. Average pricing remains steady across star tiers (~£35.00), demonstrating catalog-independent pricing.
* **Deliverable:** `eda_analysis_charts.png` (4-panel statistical chart suite).

---

### Task 3: Data Visualization Dashboard (`task3_visualization.py`)
* **Objective:** Present actionable merchandise intelligence for retail category managers.
* **Deliverable:** `task3_business_dashboard.png` (executive dashboard covering price tier segmentation, rating distribution, and product spotlights).