import asyncio
import json
import aiohttp
import requests
from bs4 import BeautifulSoup


products = []
count_for_log = 0


async def async_launch(url, headers, product, base_url):
    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers=headers)
        soap = BeautifulSoup(res.text(), 'lxml')
        page_count = int(soap.find_all('a', 'PaginationWidget__page')[-1].get_text())

        tasks = []
        global count_for_log
        count_for_log = page_count
        for count in range(1, page_count + 1):
            current_url = url + f'?p={count}'
            task = asyncio.create_task(get_page_data(session, current_url, headers, product, count, base_url))
            tasks.append(task)
        loop = asyncio.get_event_loop()
        wait_tasks = asyncio.wait(tasks)
        loop.run_until_complete(wait_tasks)
        loop.close()


async def get_page_data(session, url, headers, product, count, base_url):
    global count_for_log
    res = await session.get(url, headers=headers)
    src = res.text()
    with open(f'data/{count}_{product}.html', 'w') as file:
        file.write(src)
    print(f'Save page number: {count}')
    get_data(src, base_url)
    count_for_log -= 1
    print(f'Received data from the page: {count}, {count_for_log} pages left')


def get_data(src, base_url):
    soap = BeautifulSoup(src, 'lxml')
    find_class = 'product_data__gtm-js'
    products_data_list = soap.find_all('div', find_class)

    for div in products_data_list:
        data_params_str = div.get('data-params')
        product_url = 'not found'
        try:
            data_params_dict = json.loads(data_params_str.replace("'", '"'))
            product_url = base_url + div.find('a', 'Link_type_default').get('href')
        except Exception as e:
            print(f'<ERROR> in "json.loads": {e}')
            data_params_dict = {
                'id': 'not found',
                'price': 'not found',
                'oldPrice': 'not found',
                'clubPrice': 'not found',
                'shortName': 'not found',
            }

        products.append(
            {
                'id': data_params_dict['id'],
                'price': data_params_dict['price'],
                'oldPrice': data_params_dict['oldPrice'],
                'clubPrice': data_params_dict['clubPrice'],
                'shortName': data_params_dict['shortName'],
                'brandName': data_params_dict['brandName'],
                'url': product_url
            }
        )

    with open('products/product.json', 'a', encoding='utf-8') as file:
        json.dump(products, file, indent=4, ensure_ascii=False)
