import requests
from bs4 import BeautifulSoup
import sqlite3

def parse_price(value):
    if type(value) != type(""):
        return value
    
    new_value = value.replace("R$", "").strip().replace(",", "").replace(".", "")

    if new_value == "":
        return 0

    return int(new_value)


def data_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []

    for product in soup.find_all('section', class_='items-filters-section'):
        name = product.find('a', class_='poly-component__title').text.strip() if product.find('a', class_='poly-component__title') else 'No Name' #It's using the type of text and his class to find the product, if doesn't have one it returns 'No Name'
        price = product.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').text.strip() if product.find('span', class_='andes-money-amount andes-money-amount--cents-superscript') else 'No Price' # Same kind of thing from above

        products.append((name, parse_price(price)))
        print(name, price, " were scrapped")
    return products
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER
        )
    ''')
    print("Database Confirmed!")
    conn.commit()
    conn.close()

def save_to_database(data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for name, price in data:
        cursor.execute('INSERT INTO product (name, price) VALUES (?, ?)', (name, price)) # The command that makes the information go to the database

    print("Name & Price Saved!")
    conn.commit()
    conn.close() 

if __name__ == "__main__":
    url = "https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1#filter_applied=container_id&filter_position=1&is_recommended_domain=false&origin=scut" # Replace with the target site
    create_database()
    database = data_scrape(url)
    save_to_database(database)
    print("Name and price data scraped and saved with code 1")