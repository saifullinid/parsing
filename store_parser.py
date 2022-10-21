import requests
from bs4 import BeautifulSoup

url = 'https://www.dns-shop.ru/'
# url = 'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

res = requests.get(url, headers=headers)
src = res.text
soap = BeautifulSoup(src, 'html.parser')

# print(src.status_code)
print(src)

products = soap.find_all('div', 'menu-mobile')

print(products)