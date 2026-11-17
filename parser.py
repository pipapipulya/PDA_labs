import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_books(pages=3):
    books_data = []

    for i in range(1, pages + 1):
        url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(url)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for article in articles:
            title = article.h3.a["title"]

            price_str = article.find("p", class_="price_color").text
            price = float(price_str.replace("£", "").replace("Â", ""))

            stock_status = article.find("p", class_="instock availability").text.strip()

            rating_class = article.p["class"][1]

            books_data.append({
                "title": title,
                "price": price,
                "stock_status": stock_status,
                "rating": rating_class
            })

    return pd.DataFrame(books_data)


if __name__ == "__main__":
    print("Начинаем сбор данных...")
    df = scrape_books(pages=5)

    print(f"Собрано {len(df)} записей. Пример данных:")
    print(df.head())

    df.to_csv("parsed_data.csv", index=False)
    print("\nДанные успешно сохранены в файл parsed_data.csv")