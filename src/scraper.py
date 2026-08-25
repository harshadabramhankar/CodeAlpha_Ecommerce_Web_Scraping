import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import time


# --------------------------------------------------
# 1. Website Configuration
# --------------------------------------------------

base_url = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}


# --------------------------------------------------
# 2. Rating Conversion
# --------------------------------------------------

rating_mapping = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


# --------------------------------------------------
# 3. Store Scraped Products
# --------------------------------------------------

products = []


# --------------------------------------------------
# 4. Start Pagination
# --------------------------------------------------

current_url = base_url

page_number = 1


while current_url:

    print("\n----------------------------------------")
    print("Scraping Page:", page_number)
    print("URL:", current_url)
    print("----------------------------------------")

    try:

        response = requests.get(
            current_url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        print(
            "Status:",
            response.status_code
        )

    except requests.RequestException as error:

        print(
            "Request failed:",
            error
        )

        break


    # --------------------------------------------------
    # 5. Parse HTML
    # --------------------------------------------------

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    # --------------------------------------------------
    # 6. Find Books
    # --------------------------------------------------

    books = soup.find_all(
        "article",
        class_="product_pod"
    )

    print(
        "Books found:",
        len(books)
    )


    # --------------------------------------------------
    # 7. Extract Product Information
    # --------------------------------------------------

    for book in books:

        # Product Name
        title_element = book.h3.a

        title = title_element.get(
            "title"
        )


        # Price
        price_element = book.find(
            "p",
            class_="price_color"
        )

        price = price_element.get_text(
            strip=True
        )


        # Rating
        rating_element = book.find(
            "p",
            class_="star-rating"
        )

        rating_class = rating_element.get(
            "class"
        )

        rating_word = rating_class[1]

        rating = rating_mapping.get(
            rating_word
        )


        # Availability
        availability_element = book.find(
            "p",
            class_="instock availability"
        )

        availability = availability_element.get_text(
            " ",
            strip=True
        )


        # Product URL
        link_element = book.h3.a

        relative_url = link_element.get(
            "href"
        )

        product_url = urljoin(
            current_url,
            relative_url
        )


        # Scraping Date
        scraped_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


        # Store Product
        products.append({

            "product_name": title,

            "price": price,

            "rating": rating,

            "availability": availability,

            "product_url": product_url,

            "scraped_date": scraped_date

        })


    # --------------------------------------------------
    # 8. Find Next Page
    # --------------------------------------------------

    next_button = soup.select_one(
        "li.next a"
    )


    if next_button:

        next_url = next_button.get(
            "href"
        )

        current_url = urljoin(
            current_url,
            next_url
        )

        page_number += 1

        # Small delay between requests
        time.sleep(1)


    else:

        print("\nNo more pages.")

        current_url = None


# --------------------------------------------------
# 9. Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(products)


# --------------------------------------------------
# 10. Display Results
# --------------------------------------------------

print("\n========================================")
print("SCRAPING COMPLETED")
print("========================================")

print(
    "Total products scraped:",
    len(df)
)

print(
    "Total columns:",
    len(df.columns)
)

print("\nDataset preview:")

print(
    df.head()
)


# --------------------------------------------------
# 11. Save Raw Dataset
# --------------------------------------------------

df.to_csv(
    "data/raw/books_raw.csv",
    index=False
)

print(
    "\nRaw dataset saved successfully!"
)

print(
    "File: data/raw/books_raw.csv"
)