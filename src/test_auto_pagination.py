import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

current_url = base_url

page_number = 1

while current_url:

    print("\nScraping Page:", page_number)
    print("URL:", current_url)

    try:
        response = requests.get(
            current_url,
            headers=headers,
            timeout=20
        )

        print("Status:", response.status_code)

        response.raise_for_status()

    except requests.RequestException as error:
        print("Request failed:", error)
        break

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    books = soup.find_all(
        "article",
        class_="product_pod"
    )

    print(
        "Books found:",
        len(books)
    )

    # Find Next button
    next_button = soup.select_one(
        "li.next a"
    )

    if next_button:

        next_url = next_button.get("href")

        current_url = urljoin(
            current_url,
            next_url
        )

        page_number += 1

    else:

        print("\nNo more pages.")
        current_url = None

print("\nPagination completed.")
print("Total pages scraped:", page_number)