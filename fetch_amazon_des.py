import requests
from bs4 import BeautifulSoup as bs

headers = {
    'authority': 'www.amazon.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def find_des(url):
    description = ""
    html_text = requests.get(url, headers=headers)
    soup = bs(html_text.content, "lxml")
    soup = bs(soup.prettify(), "lxml")

    try:
        des_list = soup.find('div', class_="a-section a-spacing-medium a-spacing-top-small").find('ul').find_all('li')
        for item in des_list:
            description += " " + item.text.strip()
    except:
        print("No description found.")

    return description

