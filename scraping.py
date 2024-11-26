import requests
from bs4 import BeautifulSoup
import json 



current_page = 1
data = []
book_number = 1

proceed = True

while proceed:
    print(f"Currently scraping page: {current_page}")
    url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    if "404 Not Found" in soup.title.text or current_page == 51:
        proceed = False
    else:
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in all_books:
            item = {"id": book_number }  
            item["title"] = book.find("img").attrs["alt"]  
            item["link"] = f'https://books.toscrape.com/catalogue/{book.find("a").attrs["href" ]}' 
            item["price"] = book.find("p", class_="price_color").text[2:]
            item["stock"] = book.find("p", class_="instock availability").text.strip()
            data.append(item)
            book_number += 1

    current_page += 1 

with open("books.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Scraping completed! Data saved to books.json.")
