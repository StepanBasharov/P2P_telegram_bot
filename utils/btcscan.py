import requests
from bs4 import BeautifulSoup


def btc_hash_scaner(hash, wallet):
    resp = requests.get(f"https://blockchair.com/bitcoin/transaction/{hash}")
    soup = BeautifulSoup(resp.text, 'lxml')
    for i in soup.findAll('div', class_="transaction-io__card"):
        id = i.find('a', class_='hash')
        try:
            if id.text.strip() == wallet:
                return float(i.findAll('span')[6].text)
        except:
            return False
