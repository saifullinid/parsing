import asyncio

from async_parser import async_launch, write_data

config = {
    'product': 'televizory',
    'base_url': 'https://www.citilink.ru',
    'headers': {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
}


def main():
    url = config['base_url'] + '/catalog/' + config['product'] + '/'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_launch(loop, url, config['headers'], config['base_url']))
    write_data(config['product'])


if __name__ == '__main__':
    main()
