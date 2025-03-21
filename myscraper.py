import requests
import random
import time
from bs4 import BeautifulSoup as bs
import csv
import nltk
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import os

# ✅ Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

pd.options.mode.chained_assignment = None

# ✅ ScraperAPI Key
API_KEY = "4b6bb26639a28c93d1b27a35e1020594"

# ✅ Dynamic User-Agent rotation (for Flipkart scraping)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate"
    }

# ✅ Utility functions
def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.lower() not in stopwords.words("english")]
    return sorted(set(tokens))

def get_amazon_url(search):
    return f"http://api.scraperapi.com/?api_key={API_KEY}&url=https://www.amazon.com/s?k={search.replace(' ', '+')}"

def get_flipkart_url(search):
    return f"https://www.flipkart.com/search?q={search.replace(' ', '%20')}"

# ✅ Amazon Scraper (with ScraperAPI)
def search_in_amazon(search, writer):
    url = get_amazon_url(search)
    print(f"🔄 Fetching Amazon results for '{search}' using ScraperAPI...")

    try:
        response = requests.get(url)  # ScraperAPI handles headers & proxies
        print(f"📡 Amazon Response Code: {response.status_code}")

        if response.status_code != 200:
            print("⚠️ Amazon request failed. Retrying...")
            return

        soup = bs(response.content, "html.parser")
        items = soup.find_all('div', {'data-component-type': 's-search-result'})

        if not items:
            print("⚠️ No items found on Amazon.")
            return

        links = []
        for item in items:
            try:
                image = item.find('img', class_="s-image")['src']
                name = item.find('span', class_="a-text-normal").text.strip()
                link = "https://amazon.com" + item.find('a', class_="a-link-normal")['href']
                price = item.find('span', class_="a-offscreen").text.strip() if item.find('span', class_="a-offscreen") else "N/A"
                rating = item.find('span', class_="a-icon-alt").text.strip() if item.find('span', class_="a-icon-alt") else "N/A"

                if link in links:
                    continue
                links.append(link)

                writer.writerow([image, "Amazon", name, price, rating, link])
            except AttributeError:
                continue

        print(f"✅ Amazon results fetched: {len(links)}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Amazon: {e}")

# ✅ Flipkart Scraper (Standard Scraping)
def search_in_flipkart(search, writer):
    url = get_flipkart_url(search)

    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("⚠️ Flipkart scraping failed. Skipping...")
        return

    soup = bs(response.content, "lxml")
    items = soup.find_all('div', class_='_1AtVbE')

    if not items:
        print("⚠️ No items found on Flipkart.")
        return

    links = []
    for item in items:
        try:
            image = item.find('img', class_="_396cs4")['src']
            name = item.find('a', class_="IRpwTa").text.strip()
            link = "https://www.flipkart.com" + item.find('a', class_="IRpwTa")['href']
            price = item.find('div', class_="_30jeq3").text.strip()
            rating = item.find('div', class_="_3LWZlK").text.strip()

            if link in links:
                continue
            links.append(link)

            writer.writerow([image, "Flipkart", name, price, rating, link])
        except:
            continue

    print(f"✅ Flipkart results fetched: {len(links)}")

# ✅ Main controller function
def result(search):
    BASE_DIR = os.getcwd()
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['image', 'company', 'name', 'price', 'rating', 'link'])

        search_in_amazon(search, writer)
        search_in_flipkart(search, writer)

    print("✅ Scraping complete. Results saved to results.csv")
    if __name__ == "__main__":
        search_query = input("🔍 Enter a product to search: ").strip()
        if search_query:
            result(search_query)
        else:
            print("⚠️ Error: Search query cannot be empty!")


