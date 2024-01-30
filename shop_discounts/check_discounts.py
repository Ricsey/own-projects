import asyncio
import functools
from pprint import pprint
import re
import time
import aiohttp
import numpy as np
import requests

from bs4 import BeautifulSoup
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TypeVar

COLUMNS = ['product_name', 
            'link', 
            'original_price', 
            'discount_price', 
            'discount_percentage', 
            'discount_duration']

@dataclass
class ProductInfo:
    product_name: str
    link: str
    original_price: str
    discount_price: str
    discount_percentage: str
    discount_duration: str

def find_element_text(obj: BeautifulSoup, tag: str, attr: dict) -> BeautifulSoup:
    try:
        return obj.find(tag, attr).text
    except:
        return None

def find_first_element_by_css(obj: BeautifulSoup, css_selector: str) -> BeautifulSoup:
    o = obj.select(css_selector)
    if len(o):
        return o[0].text
    else:
        return np.nan

def calc_discount_percentage(orig: str, disc: str) -> str:
    if orig is np.nan:
        return np.nan
    else:
        return f'{int((1 - to_float(disc) / to_float(orig))*100)}%'

def to_float(num_str: str) -> float:
    return float(''.join(c for c in num_str.replace(' ', '') if c.isnumeric())) 

def try_find_sale(datas: dict) -> dict:
    if datas:
        for data in datas:
            if data['type'] == 'sale':
                return data
        else:
            return datas[0]
    else:
        return np.nan

async def get_html_soup(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    async with session.get(url) as response:
        return BeautifulSoup(await response.text(), 'lxml')

def timeit(func):
    """ decorator that can take either coroutine or normal function """
    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            with wrapping_logic():
                return (await func(*args, **kwargs))
    return wrapper


class LIDL():
    def __init__(self) -> None:
        self.base_url = 'https://www.lidl.hu'

    def parse_discounts_on_page(self, page: BeautifulSoup) -> list[ProductInfo]:
        discounts = []
        for product_infos in page.find_all('article', {'class' : 'ret-o-card'}):
            discounts.append(ProductInfo(
                            product_name = product_infos['data-name'],
                            link = self.base_url + product_infos.find('a', href=True)['href'],
                            original_price = find_element_text(product_infos, 'span', {'class' : 'lidl-m-pricebox__discount-price'}),
                            discount_price = product_infos['data-price'],
                            discount_percentage = find_element_text(product_infos, 'div', {'class' : 'lidl-m-pricebox__highlight'}),
                            discount_duration = find_element_text(product_infos, 'span', {'class' : 'lidl-m-ribbon-item__text'})
                        ))
        return discounts

    async def fetch_datas(self, session: aiohttp.ClientSession, url: str) -> list[ProductInfo]:
        page = await get_html_soup(session, url)
        return self.parse_discounts_on_page(page)

    async def get_discounts(self):
        async with aiohttp.ClientSession() as session:
            response = requests.get(self.base_url)
            base_soup = BeautifulSoup(response.text, 'lxml')
            discount_links = [category.find('a', href=True)['href'] for category in base_soup.find_all('div', {'class' : 'theme__body'})]
            discount_category_pages = list('https://www.lidl.hu' + link for link in discount_links)

            tasks = (self.fetch_datas(session, url) for url in discount_category_pages)
            discounts = await asyncio.gather(*tasks)
            return discounts


class ALDI():
    def __init__(self) -> None:
        self.url = 'https://www.aldi.hu/hu/ajanlatok/szuper-ajanlatok-mindennap.html'

    async def parse_product(self, product: BeautifulSoup, title: BeautifulSoup) -> ProductInfo:
        return ProductInfo(
                product_name = product.select('figcaption > h3')[0].text,
                link = self.url,
                original_price = find_first_element_by_css(product, 'strike > b'),
                discount_price = product.select('h2 > b')[0].text,
                discount_percentage = calc_discount_percentage(orig=find_first_element_by_css(product, 'strike > b'), disc=find_first_element_by_css(product,'h2 > b')),
                discount_duration = ' - '.join(re.findall(r'\d{4}.\d{2}.\d{2}', title.text))
            )

    async def get_discounts(self) -> list[ProductInfo]:
        async with aiohttp.ClientSession() as session:
            soup = await get_html_soup(session=session, url=self.url)

            discounts = list()

            for title in (item for item in soup.find_all('div', {'class' : 'E05-basic-text'}) if re.search(r'\d{4}.\d{2}.\d{2}-t.l', item.text)):
                for product in title\
                                .find_next('div', {'class' : 'E12-grid-gallery'})\
                                .find_all('div', {'class' : 'item'}):
                    if product.text.replace('\n', ''):
                        discounts.append(await self.parse_product(product, title))
            # return pd.DataFrame(discounts, columns = COLUMNS)
            return discounts


class TESCO():
    @staticmethod
    async def get_discounts():
        url = "https://tesco.hu/Ajax"

        querystring = {"apage":"1","limit":"10000","type":"load-more-products","page_url":"/akciok/akcios-termekek","":""}

        payload = ""
        headers = {
            "cookie": "bm_sv=E6CC50FDBEBF01EF7D1E28943ED375ED~YAAQFLUQAoTL4vqCAQAAmeIcDxGu18YFZLmTV46TSb5nAvcG9ciS4cehQH3TkDbqIjV9F%2BcRS7lGwFnT6CJiJtcekqVQdF1WOe60Ap4OELL410ky5N9UCjDRfPoRuNkV6ihYiX%2FojCYJaq8V%2FvBFs7IQPESAq3TzYBQcXd%2BQttdW2K3n1EbziTQL%2BJPOA%2FVaMwP0S6PnkryC%2FdTojwnvS46U5hcLkCwhBKCBPRgXkqEFFzpPLBoHk%2BFDdSnfBBY%3D~1; PHPSESSID=pcn9fp263lu6treckova88js17; ak_bmsc=4098A39153E90A8ECB9A622432890BE0~000000000000000000000000000000~YAAQFLUQArm%2B4vqCAQAASKYZDxHxz2QpeBFGgHQ5ZGGRRlDPpmjK41%2FfdEC6youm2ghRHMljWgwTnKtkfYHO55sN17Yyyd7TkJr503Qx8w8CA5ysfuogtiYXptn5Hz%2FXTsD09kJYgNvss9Dl51uhiBTeyQpESm0VNkVvopgEqAe%2B8EAmFFjRxRpaqJMgGBmQw2Ux83jDDUobK9GQaeGzfBvFxP77OlwtOlD2z3pLdydv4q3JdL1yNcg3ycNd0DK3qvbozgqcURdd8LVTWUMRnNHJVpLDngbQmAiIY7st6AJaq7%2B8eOzBNHdg3Nqc163xycqxKj6uLpNlKCEBu6zfzWF3OK%2FrIIAtwguRMXsKZQ63nzVjb8%2FJMD2kSwnDsI1s2LVocG%2FDdNbouLUhovdd5rjxViC%2Ff576gA%3D%3D",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRF-Token": "OWU1OTA3MDAwOWZjMTc0MjJjN2RmNDk5NTZiMDNmYmU=",
            "Connection": "keep-alive",
            "Referer": "https://tesco.hu/akciok/akcios-termekek/",
            "Cookie": "gdprCookiePreferences=%7B%22experience%22%3Afalse%2C%22advertising%22%3Afalse%7D; PHPSESSID=9mlnkp4cavtb955qgjpeiuebf3; ak_bmsc=193D1FD9932CE89EB8AD962D5F8C58CD~000000000000000000000000000000~YAAQvF4OF9673AaDAQAAYykMDxE1AiLipUDGug3urpb/mNcwyMl0g7j07X6cnq65iUs1sz93YfsFdZ1YTUFu657cd5cS8BjghZ/f3T1FEn8kfHJNWQ6u1C+4w0E/xHtjYUdSawSA3AsnxlcKaoqwUSSAG7vLhF3zTsBISoilx4Nem98o0n5S5nz7K37PeIaZ0AfQc/S00QHTbaFCPAxMqGo/1nEaWSfyqmQRd28stgoKJdhTd7cDJahg0rkgMpBJsbyYLs2EY9zxIpeO7m8Uu2G3xLQjdYsG7yCSlIs3BafvosNdTjw4ge3xxcL7ZveOQEZ11UCk1E4kdwKsVZqq+QzFWAxGhGi+IC60pD/eJbDjd6TBuexZ+NavAlxnKeg4i+F4xmQbrwRJ8LgLgj3NX0yf6v+0FPNDxPqfVCSZreuB59VdtsVo5k+FqWAqgnN4e2dXn7PK6GIOQrRfiwdI0Mw73ao9KpcvQPp2XgFtoC07fYJZihsNbwI=; kcs.index=loaded; bm_sv=E6CC50FDBEBF01EF7D1E28943ED375ED~YAAQvF4OF/W/3AaDAQAAb5sMDxE6zZT90dOjLvKDtFLC68eyi6GJci3ipOAcEjtswBUppsj8Q7HidKvvKCXGdcPWQR4qNJwILH1l9Tbe7z9FNewfALawam4yyB4zTbz6g7IoJ+PnKexyFXMPOXphxGfLLbCuNwaex3AhBni/u89By0xdfHCVlq03Aht5rBXGTN/mI4aCvNify9MVXnS2zppt4wKlaSJg2raIL4ckmKqedJ1GR0a435hcjvZkPsQ=~1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        discounted_products: list[ProductInfo] = list()

        for product_info in response.json()['products']:
            detailed_data = product_info['data']['template']['data']
            discounted_products.append(
                ProductInfo(
                    product_name = product_info['name'],
                    link = 'https://tesco.hu/akciok/akcios-termekek/termek/' + product_info['url'],
                    original_price = detailed_data.get('old-price', np.nan),
                    discount_price = detailed_data.get('clubcard-price', {}).get('price') or detailed_data.get('price'),
                    discount_percentage = detailed_data.get('discount-percentage', np.nan),
                    discount_duration = product_info['offerbegin'] + ' - ' + product_info['offerend']
                )
            )
        # return pd.DataFrame(discounted_products, columns = COLUMNS)
        return discounted_products


class SPAR():
    @staticmethod
    async def get_discounts() -> list[ProductInfo]:
        url = "https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_hu"

        querystring = {"query":"*","q":"*","hitsPerPage":"1000","page":"1","filter":"is-on-promotion:Minden ajánlat"}

        payload = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        discounted_products: list[ProductInfo] = list()

        for hit in response.json()['hits']:
            product = hit['masterValues']
            discounted_products.append(ProductInfo(product_name = product['name'] + '\n' + product['promotion-text'] if 'promotion-text' in product.keys() else product['name'],
                                                    link = 'http://www.spar.hu/onlineshop' + product['url'],
                                                    original_price = product['regular-price'],
                                                    discount_price = product['price'],
                                                    discount_percentage = f"{int((1 - product['price'] / product['regular-price'])*100)}%",
                                                    discount_duration = np.nan
                                                    ))
        # return pd.DataFrame(discounted_products)
        return discounted_products


class KIFLI():
    def __init__(self):
        self.base_url = 'https://www.kifli.hu/nagyszeru-arak'

    async def get_json(self, client, url):
        async with client.get(url) as response:
            return await response.json()


    def try_find_sale(self, datas):
        if not datas:
            return {}
        for data in datas:
            if data['type'] == 'sales':
                return data
        else:
            return datas[0]

    def parse_data(self, data):
        sales = self.try_find_sale(data['sales'])
        return ProductInfo(
            product_name = data['productName'],
            link = 'http://www.kifli.hu/' + data['link'],
            original_price = sales.get('originalPrice', {}).get('full'),
            discount_price = sales.get('price', {}).get('full'),
            discount_percentage = sales.get('discountPercentage'),
            discount_duration = sales.get('startedAt') + ' - ' + sales.get('endsAt')
        )

    async def get_discount_on_page(self, category_code):
        discounted_products_by_category = []
        async with aiohttp.ClientSession() as client:
            datas = await self.get_json(client=client, url=f'https://www.kifli.hu/services/frontend-service/special-category/sale/load-more/category/{category_code}?offset=8&limit=100')

            for product in datas['data']:
                if 'sales' not in product.keys() or\
                    not product['sales']:
                        return
                discounted_products_by_category.append(self.parse_data(product))

            return discounted_products_by_category     

    async def get_discounts(self):
        discounts = list()

        html = requests.get(self.base_url)
        base_site_soup = BeautifulSoup(html.content, 'lxml')

        categories = {a.text : a['href'][2:].split('-')[0] for a in base_site_soup.find_all('a', {'class' : 'sortimentLink'}) if 'benu' not in a.text.lower()}

        tasks = (self.get_discount_on_page(category_code) for category_code in categories.values())
        discounts = await asyncio.gather(*tasks)

        return discounts


def flatten(LIST):
    flattened = []
    for item in LIST:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

def filter_discounts(discounts: list, looking_for) -> list:
    return [product for product in discounts if any(looking.lower() in product.product_name.lower() for looking in looking_for)]

async def run(looking_for):
    start = time.perf_counter()
    tasks = (
        ALDI().get_discounts(),
        LIDL().get_discounts(),
        TESCO().get_discounts(),
        SPAR().get_discounts(),
        KIFLI().get_discounts(),
    )
    res = await asyncio.gather(*tasks)
    discounts = list(flatten(res))
    all_discounts = sum(len(products) for products in res)
    # pprint(f'All discounts are: {discounts}')
    # pprint(f'Len discounts are: {len(discounts)}')
    filtered_discounts = filter_discounts([prod for prod in discounts if prod], looking_for)
    pprint(filtered_discounts)
    print(f'finished in {time.perf_counter() - start} sec')
    return filtered_discounts







