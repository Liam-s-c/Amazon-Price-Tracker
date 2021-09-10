import requests
import re
from bs4 import BeautifulSoup
import time

def get_converted_price(price):

    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price)) # Thanks to https://medium.com/@oorjahalt
    return converted_price


def extract_url(url):

    if url.find("www.amazon.co.uk") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.co.uk" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.co.uk" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url


def get_product_details(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url is None:
        details = None
    else:
        page = requests.get(_url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False
        if title is not None and price is not None:
            details["price"] = get_converted_price(price.get_text())
        else:
            details = None
    return details


while True:
    time.sleep(5)
    print(get_product_details("https://www.amazon.co.uk/Corsair-Illuminated-Individually-Addressable-Compatibility/dp/B08SQD14BY/ref=sr_1_3?dchild=1&keywords=128gb+ram&qid=1631258861&sr=8-3"))
