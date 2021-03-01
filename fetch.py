# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import requests
import lxml.html
from requests import HTTPError


def get_all_website():
    req = requests.get('http://webstack.cc/cn/index.html')
    if req.status_code == 200:
        html = lxml.html.fromstring(req.text)
    else:
        raise HTTPError
    print(html.xpath('/html/body/div/div[2]/h4/text()'))
    all_categorys = html.xpath('/html/body/div/div[2]/h4/text()')


def main():
    get_all_website()


if __name__ == '__main__':
    main()
