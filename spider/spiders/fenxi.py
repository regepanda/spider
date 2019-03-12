# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bs4
import re

fp = open('/Users/lili/Desktop/spider/spider/spiders/detail.txt', encoding='utf-8')
html = fp.read()
# baseUrl = 'https://cd.lianjia.com'
soup = BeautifulSoup(html, 'html.parser')
# lis = soup.findAll('li', class_='clear LOGCLICKDATA')
# detailUrls = []
# for li in lis:
#     detailUrls.append(li.find(name='a').get('href'))
#
#
# # 再获取下一页的url
# nextPages = soup.find('div', class_='page-box fr').find_all('a')
# nextPages = [nextPage.get('href') for nextPage in nextPages if isinstance(nextPage, bs4.element.Tag)]
# nextUrl = baseUrl + nextPages[-1]
# print(nextUrl)
imgs = soup.find('ul', class_='smallpic').findAll('li')
imgs = [img.get('data-src') for img in imgs if isinstance(img, bs4.element.Tag)]
title = soup.find('h1', class_='main').string
price = soup.find('span', class_='total').string + soup.find('span', class_='unit').string
onePrice = soup.find('span', class_='unitPriceValue')
onePrice = re.compile(r'<[^>]+>', re.S).sub('', str(onePrice))
room = soup.find('div', class_='mainInfo').string
communityNames = soup.find('div', class_='communityName').findAll('a')
communityName = [name.string for name in communityNames if isinstance(name, bs4.element.Tag)][0]
areas = soup.find('span', class_='info').findAll('a')
area = [areaName.string for areaName in areas if isinstance(areaName, bs4.element.Tag)][0]