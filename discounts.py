from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from bs4 import BeautifulSoup
from pprint import pprint
import time
import re
import requests
import numpy as np
import pandas as pd


#################
# EZT TÖLTSD KI #
#################
# aposztrófok között legyen a szó, ami tartalmazza részben vagy egészben benne van a nevében vesszővel elválasztva
# pl. táska -> Barackos táska, Almás táska, Iskolatáska
# miután lefutott, nyitsd meg ezt a linket a böngészőben: file:///F:/Python%20projects/hello%20world/test.html

looking_for = ('nutella', 'keksz', )
# looking_for = ('glutén', )













@dataclass
class ProductInfo:
    product_name: str
    link: str
    original_price: str
    discount_price: str
    discount_percentage: str
    discount_duration: str

COLUMNS = ['product_name', 
            'link', 
            'original_price', 
            'discount_price', 
            'discount_percentage', 
            'discount_duration']
# CHROME_OPTIONS = options = webdriver.ChromeOptions()
# CHROME_OPTIONS.add_argument('--headless')
# CHROME_OPTIONS.add_argument('--no-sandbox')
# CHROME_OPTIONS.add_argument('--disable-dev-shm-usage')

def is_on_discount(product_name: str) -> bool:
    return any(look_for.lower() in product_name.lower() for look_for in looking_for)

def find_element_text(obj: BeautifulSoup, tag: str, attr: dict) -> BeautifulSoup:
    try:
        return obj.find(tag, attr).text
    except:
        return None

def find_element_href(obj: BeautifulSoup, tag: str, attr: dict) -> BeautifulSoup:
    try:
        return obj.find(tag, attr, href = True)['href']
    except:
        return ''

def pretty_dataframe(dataframe: pd.DataFrame) -> None:
    dataframe = (
        dataframe.assign(
            manufacturer = dataframe.manufacturer
                            .str.lstrip('\n')
                            .str.strip()
                            .fillna(''),
            product_n = dataframe.product_n.str.rstrip(),
            discount_percentage = dataframe.discount_percentage.str.lstrip('-')
            )
    )
    
    dataframe = (
        dataframe
        .assign(product_name = dataframe.manufacturer + ' ' + dataframe.product_n)
        .drop(['manufacturer', 'product_n'], axis = 1)
        .dropna(subset = ['product_name'])
        .fillna('-')
        [COLUMNS]
    )
    return dataframe

def try_find_sale(datas: dict) -> dict:
    if datas:
        for data in datas:
            if data['type'] == 'sale':
                return data
        else:
            return datas[0]
    else:
        return np.nan

def to_float(num_str: str) -> float:
    return float(''.join(c for c in num_str.replace(' ', '') if c.isnumeric())) 

def calc_discount_percentage(orig: str, disc: str) -> str:
    if orig is np.nan:
        return np.nan
    else:
        return f'{int((1 - to_float(disc) / to_float(orig))*100)}%'

def find_first_element_by_css(obj: BeautifulSoup, css_selector: str) -> BeautifulSoup:
    o = obj.select(css_selector)
    if len(o):
        return o[0].text
    else:
        return np.nan

def get_html_content(url: str) -> BeautifulSoup:
        html = requests.get(url)
        return BeautifulSoup(html.content, 'lxml')

class ALDI():

    def get_discounts(self) -> list[ProductInfo]:
        url = 'https://www.aldi.hu/hu/ajanlatok/szuper-ajanlatok-mindennap.html'
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        discounts = list()

        print('Fetching ALDI discounts...')
        for title in (item for item in soup.find_all('div', {'class' : 'E05-basic-text'}) if re.search(r'\d{4}.\d{2}.\d{2}-t.l', item.text)):
            for product in title\
                            .find_next('div', {'class' : 'E12-grid-gallery'})\
                            .find_all('div', {'class' : 'item'}):
                if product.text.replace('\n', ''):
                    discounts.append(
                        ProductInfo(
                            product_name = product.select('figcaption > h3')[0].text,
                            link = url,
                            original_price = find_first_element_by_css(product, 'strike > b'),
                            discount_price = product.select('h2 > b')[0].text,
                            discount_percentage = calc_discount_percentage(orig=find_first_element_by_css(product, 'strike > b'), disc=find_first_element_by_css(product,'h2 > b')),
                            discount_duration = ' - '.join(re.findall(r'\d{4}.\d{2}.\d{2}', title.text))
                        )
                    )
                    print(discounts[-1])
        return pd.DataFrame(discounts, columns = COLUMNS)
        # return discounts


class LIDL():
    def __init__(self):
        self.base_url = 'https://www.lidl.hu'    
        self.discounts = list()    

    def get_discounts(self):
        pprint('Fetching LIDL discounts...')

        html = requests.get(self.base_url)
        base_soup = BeautifulSoup(html.content, 'lxml')

        discount_links = [category.find('a', href=True)['href'] for category in base_soup.find_all('div', {'class' : 'theme__body'})]

        for link in discount_links:
            print(f"Fetcing https://www.lidl.hu + {link}")
            # for product in BeautifulSoup(requests.get('https://www.lidl.hu' + link).content, 'lxml').find_all('div', {'class' : 'nuc-a-flex-item nuc-a-flex-item--width-6 nuc-a-flex-item--width-4@sm'}):
            for product_info in BeautifulSoup(requests.get('https://www.lidl.hu' + link).content, 'lxml').find_all('article', {'class' : 'ret-o-card'}):
                self.discounts.append(
                    ProductInfo(
                        product_name = product_info['data-name'],
                        link = self.base_url + product_info.find('a', href=True)['href'],
                        original_price = find_element_text(product_info, 'span', {'class' : 'lidl-m-pricebox__discount-price'}),
                        discount_price = product_info['data-price'],
                        discount_percentage = find_element_text(product_info, 'div', {'class' : 'lidl-m-pricebox__highlight'}),
                        discount_duration = find_element_text(product_info, 'span', {'class' : 'lidl-m-ribbon-item__text'})
                    )
                )
                # self.discounts.append(
                #     {
                #         'manufacturer' : find_element_text(product, 'p', {'class' : 'ret-o-card__content'}),
                #         'product_n' : find_element_text(product, 'h3', {'class' : 'ret-o-card__headline'}),
                #         'original_price' : find_element_text(product, 'span', {'class' : 'lidl-m-pricebox__discount-price'}),
                #         'discount_price' : find_element_text(product, 'span', {'class' : 'lidl-m-pricebox__price'}) ,
                #         'discount_percentage' : find_element_text(product, 'div', {'class' : 'lidl-m-pricebox__highlight'}),
                #         'link' : self.base_url + find_element_href(product, 'a', {'class' : 'ret-o-card__link nuc-a-anchor'}),
                #         'discount_duration' : find_element_text(product, 'span', {'class' : 'lidl-m-ribbon-item__text'})
                #     }
                # )
        # return pretty_dataframe(pd.DataFrame(self.discounts, columns = ['manufacturer', 'product_n', 'original_price', 'discount_price', 'discount_percentage', 'link', 'discount_duration']))
        return pd.DataFrame(self.discounts, columns=COLUMNS)


class TESCO():
    @staticmethod
    def get_discounts():
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

        print('Fetching TESCO discounts...')

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        discounted_products = list()

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
            print(discounted_products[-1])
        return pd.DataFrame(discounted_products, columns = COLUMNS)


class KIFLI():
    def __init__(self):
        self.base_url = 'https://www.kifli.hu/nagyszeru-arak'

    def get_discounts(self):
        print('Fetching KIFLI discounts...')
        discounts = list()

        html = requests.get(self.base_url)
        base_site_soup = BeautifulSoup(html.content, 'lxml')

        categories = {a.text : a['href'][2:].split('-')[0] for a in base_site_soup.find_all('a', {'class' : 'sortimentLink'}) if 'benu' not in a.text.lower()}

        for category in categories:
            print(f"Fetching '{category}' discounts")
            datas = requests.get(f'https://www.kifli.hu/services/frontend-service/special-category/sale/load-more/category/{categories[category]}?offset=8&limit=100')
            dataframe = pd.json_normalize(datas.json()['data'])
            if  dataframe.empty or \
                'sales' not in dataframe.columns or \
                len(dataframe.sales[0]) == 0:
                    continue
            else:
                discounted_products_by_category = pd.concat(
                                                    [
                                                        dataframe.productName,
                                                        (
                                                        pd.json_normalize(
                                                            dataframe.sales.apply(lambda cell: try_find_sale(cell))
                                                        )
                                                        [['discountPercentage', 'startedAt','endsAt', 'price.full', 'originalPrice.full']]
                                                        ),
                                                        dataframe.baseLink.apply(lambda link: 'http://www.kifli.hu/' + link),
                                                    ],
                                                    axis=1)
                discounts.append(discounted_products_by_category)

        discounts_dataframe = pd.concat(discounts, axis=0)

        discounts_dataframe = (
            discounts_dataframe
            .assign(discount_duration = discounts_dataframe.startedAt + ' - ' +  discounts_dataframe.endsAt)
            .drop(['startedAt', 'endsAt'], axis = 1)
            [['productName', 'baseLink', 'originalPrice.full', 'price.full', 'discountPercentage', 'discount_duration']]
        )

        discounts_dataframe.columns = COLUMNS

        return discounts_dataframe


class SPAR():
    @staticmethod
    def get_discounts() -> list[ProductInfo]:
        print('Fetching SPAR discounts...')
        url = "https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_hu"

        querystring = {"query":"*","q":"*","hitsPerPage":"1000","page":"1","filter":"is-on-promotion:Minden ajánlat"}

        payload = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        discounted_products = list()

        for hit in response.json()['hits']:
            product = hit['masterValues']
            discounted_products.append(ProductInfo(product_name = product['name'] + '\n' + product['promotion-text'] if 'promotion-text' in product.keys() else product['name'],
                                                    link = 'http://www.spar.hu/onlineshop' + product['url'],
                                                    original_price = product['regular-price'],
                                                    discount_price = product['price'],
                                                    discount_percentage = f"{int((1 - product['price'] / product['regular-price'])*100)}%",
                                                    discount_duration = np.nan
                                                    ))
            print(discounted_products[-1])
        return pd.DataFrame(discounted_products)
    

def main():
    start = time.perf_counter()
    shop_discounts = [shop().get_discounts() for shop in (KIFLI, TESCO, ALDI, LIDL, SPAR)]
    print(f'finished in {time.perf_counter() - start} sec')
    return

    # shop_discounts = [shop().get_discounts() for shop in (ALDI, SPAR)]
    discounts = pd.concat(shop_discounts)
    filtered_discounts = (
        discounts
        .loc[discounts.product_name.apply(is_on_discount)]
        .astype(str)
        .assign(original_price = lambda d: d['original_price'].str.replace(' ', ''))
        .assign(original_price = lambda d: d['original_price'].str.extract('(\d+)'))
        .assign(discount_price = lambda d: d['discount_price'].str.extract('(\d+)'))
        .assign(discount_percentage = lambda d: d['discount_percentage'].str.extract('(\d+)'))
        .drop_duplicates(subset=[COLUMNS[0]])
        .reset_index(drop=True)
        .fillna('-')
        .set_axis("Termék|Link|Eredeti ár|Akciós ár|Akció [%]|Akció időtartama".split('|'), axis=1)
    )


    style = """
    table {
        border: 1px solid #ccc;
        border-collapse: collapse;
        margin: 0;
        padding: 0;
        width: 100%;
        table-layout: fixed;
    }
    
    table caption {
        font-size: 1.5em;
        margin: .5em 0 .75em;
    }
    
    table tr {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        padding: .35em;
    }
    
    table th,
    table td {
        padding: .625em;
        text-align: center;
    }
    
    table th {
        font-size: .85em;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    
    @media screen and (max-width: 600px) {
        table {
        border: 0;
        }
    
        table caption {
        font-size: 1.3em;
        }
        
        table thead {
        border: none;
        clip: rect(0 0 0 0);
        height: 1px;
        margin: -1px;
        overflow: hidden;
        padding: 0;
        position: absolute;
        width: 1px;
        }
        
        table tr {
        border-bottom: 3px solid #ddd;
        display: block;
        margin-bottom: .625em;
        }
        
        table td {
        border-bottom: 1px solid #ddd;
        display: block;
        font-size: .8em;
        text-align: right;
        }
        
        table td::before {
        /*
        * aria-label has no advantage, it won't be read inside a table
        content: attr(aria-label);
        */
        content: attr(data-label);
        float: left;
        font-weight: bold;
        text-transform: uppercase;
        }
        
        table td:last-child {
        border-bottom: 0;
        }
    }
    
    
    /* general styling */
    body {
        font-family: "Open Sans", sans-serif;
        line-height: 1.25;
    }"""
    with open('test.html', 'w') as html:
        html.writelines('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />')
        html.writelines('<link rel="stylesheet" href="mystyle.css">')
        html.write(filtered_discounts.to_html(render_links=True, escape=False))

    with open('mystyle.css', 'w') as css:
        css.write(style)

    print('\n'*5)
    print(f'All discounts: {discounts.shape[0]}, filtered discounts: {filtered_discounts.shape[0]}')

    print('\n'*5)
    print('*'*100)
    print('DONE')
    print('*'*100)

if __name__ == "__main__":
    main()