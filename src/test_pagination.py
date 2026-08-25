import requests
from bs4 import BeautifulSoup

base_url = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

for page_number in range(1, 6):

    if page_number == 1:
        url = base_url
    else:
        url = (
            f"{base_url}catalogue/"
            f"page-{page_number}.html"
        )

    print("\nChecking:", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print(
            "Status:",
            response.status_code
        )

        response.raise_for_status()

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

    except requests.RequestException as error:
        print(
            "Request failed:",
            error
        )