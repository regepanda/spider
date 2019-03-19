# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import bs4
from spider.items import LiajiaItem
import re

class LiajiaSpider(RedisSpider):
    # name = 'tencent_wanted'
    # start_urls = ['https://hr.tencent.com/position.php']

    name = "lianjia"
    redis_key = "lianjia:strat_urls"

    def parse(self, response):
        html = response.text
        liajiaBaseUrl = 'https://cd.lianjia.com'
        soup = BeautifulSoup(html, 'html.parser')

        # 获取下一页的url
        nextPages = soup.find('div', class_='page-box fr').find_all('a')
        nextPages = [nextPage.get('href') for nextPage in nextPages if isinstance(nextPage, bs4.element.Tag)]
        nextUrl = liajiaBaseUrl + nextPages[-1]

        lis = soup.findAll('li', class_='clear LOGCLICKDATA')
        detailUrls = []
        for li in lis:
            detailUrls.append(li.find(name='a').get('href'))
        for detailUrl in detailUrls:
            yield scrapy.Request(url=detailUrl, callback=self.detail)

        urlFile = open('/tmp/lianjia.txt', 'a', encoding='utf-8')
        urlFile.write(nextUrl + '\n')
        urlFile.close()
        # 访问下一页信息
        yield scrapy.Request(url=nextUrl, callback=self.parse)

    def detail(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
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
        item = LiajiaItem()
        item['imgs'] = imgs
        item['title'] = title
        item['price'] = price
        item['onePrice'] = onePrice
        item['room'] = room
        item['communityName'] = communityName
        item['area'] = area
        yield item



