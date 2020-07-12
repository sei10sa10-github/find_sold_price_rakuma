from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import os
import json
import urllib.parse
import re
import csv

from selenium.webdriver.chrome.webdriver import WebDriver


def main(argv):
    if len(argv) < 2:
        print('Please specify JSON file defines parameters')
        sys.exit(1)

    params = read_param_json(argv[1])

    header, result = search(params)

    save_csv(header, result)


def read_param_json(file_name: str) -> dict:
    abs_file_path = os.path.join(os.getcwd(), file_name)

    if not os.path.exists(abs_file_path):
        print("{} doesn't exist".format(abs_file_path))
        sys.exit(1)

    with open(abs_file_path, 'r') as f:
        return json.load(f)


def search(params: dict) -> list:
    keyword = params['keyword']
    keyword = urllib.parse.quote(keyword)

    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    url = 'https://fril.jp/search/{}'.format(keyword)

    result = []
    page = 0
    while url:
        page += 1
        print('Scrapying page {}'.format(page))

        browser.get(url)
        items = browser.find_elements_by_css_selector('div.content div.item')

        for item in items:
            name = item.find_element_by_css_selector(
                '.item-box__item-name').text
            price = item.find_element_by_css_selector(
                '.item-box__item-price').text
            price = re.sub(r'[^\d]', '', price)
            sold_ribbon = item.find_elements_by_css_selector(
                '.item-box__soldout_ribbon')
            sold = True if len(sold_ribbon) else False
            url = item.find_element_by_css_selector(
                'div.item-box__image-wrapper a').get_attribute('href')
            result.append((name, price, sold, url))

        url = get_next_page_link(browser, page)

    return ('name', 'price', 'sold', 'url'), result


def get_next_page_link(browser: WebDriver, curent_page: int) -> tuple:

    navs = browser.find_elements_by_css_selector('.pagination .page a')

    url = None
    for nav in navs:
        page_num = int(nav.text)
        if page_num == curent_page + 1:
            url = nav.get_attribute('href')
            break

    return url


def save_csv(header: tuple, data: list):
    with open(os.path.join(os.getcwd(), 'data.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == '__main__':
    main(sys.argv)