import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup


products = []
count_for_log = 0


async def async_launch(loop, url, headers, base_url):
    async with aiohttp.ClientSession() as session:
        res = await session.get(url, headers=headers)
        soap = BeautifulSoup(await res.text(), 'lxml')
        page_count = int(soap.find_all('a', 'PaginationWidget__page')[-1].get_text())

        tasks = []
        global count_for_log
        count_for_log = page_count

        for count in range(1, page_count + 1):
            current_url = url + f'?p={count}'
            task = loop.create_task(get_page_data(session, current_url, headers, count, base_url))
            tasks.append(task)

        await asyncio.wait(tasks)


async def get_page_data(session, url, headers, count, base_url):
    global count_for_log
    async with session.get(url=url, headers=headers) as res:
        src = await res.text()
        get_data(src, base_url)
        count_for_log -= 1
        print(f'Received data from the page: {count}, {count_for_log} pages left')


def get_data(src, base_url):
    soap = BeautifulSoup(src, 'lxml')
    find_class = 'product_data__gtm-js'
    products_data_list = soap.find_all('div', find_class)

    for div in products_data_list:
        data_params_str = div.get('data-params')
        try:
            data_params_dict = json.loads(data_params_str.replace("'", '"'))
        except Exception as e:
            print(f'<ERROR> in "json.loads": {e}')
            data_params_dict = {
                'id': 'not found',
                'price': 'not found',
                'oldPrice': 'not found',
                'clubPrice': 'not found',
                'shortName': 'not found',
                'brandName': 'not found'
            }
        product_dict = {}
        for key in ['id', 'price', 'oldPrice', 'clubPrice', 'shortName', 'brandName']:
            try:
                product_dict[key] = data_params_dict[key]
            except:
                product_dict[key] = 'not found'
        try:
            product_dict['url'] = base_url + div.find('a', 'Link_type_default')['href']
        except:
            product_dict['url'] = 'not found'

        products.append(product_dict)


def write_data(product):
    with open(f'products/{product}.json', 'a', encoding='utf-8') as file:
        json.dump(products, file, indent=4, ensure_ascii=False)
