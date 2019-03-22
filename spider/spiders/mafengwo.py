# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import bs4
import sys
from spider.items import MaFengWoItem
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

sys.setrecursionlimit(100000)


class MaFengWoSpider(RedisSpider):
    name = "mafengwo"
    redis_key = "mafengwo:strat_urls"
    maBaseUrl = 'http://www.mafengwo.cn'

    # 入口， 爬取马蜂窝所有旅游城市的url
    def parse(self, response):
        html = response.text
        fp = open('mafengwo_list.txt', 'w', encoding='utf-8')
        fp.write(html)
        fp.close()
        soup = BeautifulSoup(html, 'html.parser')
        cols = soup.find('div', class_='wrapper').find_all('div', class_='col')
        cities = []
        for col in cols:
            dls = col.find_all('dl')
            for dl in dls:
                hrefs = dl.find_all('a')
                lists = [[href.string, href.get('href')] for href in hrefs if isinstance(href, bs4.element.Tag)]
                cities.append({
                    'sheng': dl.find('dt').string,
                    'shi': lists
                })
        for city in cities:
            sheng = city['sheng']
            i = 0
            for cityShi in city['shi']:
                if i == 1:
                    break
                i = i + 1
                shi = cityShi[0]
                url = self.maBaseUrl + cityShi[1]
                yield self.detail(sheng, shi, url)
            break

    # 请求城市的详情
    def detail(self, sheng, shi, url):
        item = MaFengWoItem()
        item['sheng'] = sheng
        item['shi'] = shi
        item['url'] = url
        item['youji'] = []
        # 获取该地方所有游记的详情页url
        youjiDetailUrls = []
        hotelListUrl = attractionListUrl = foodListUrl = ''
        chrome_options = webdriver.ChromeOptions()
        # headless无界面模式
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/lili/software/chromedriver")
        driver.get(url)
        i = 0
        while True:
            try:
                if i == 5:
                    break
                i = i + 1
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                hotelListUrl = soup.find('div', class_='col col-hotel').find('a').get('href')
                attractionListUrl = soup.find('div', class_='col col-scenic').find('a').get('href')
                foodListUrl = soup.find('div', class_='col col-cate').find('a').get('href')
                images = soup.find_all('div', class_='tn-image')
                detailUrls = [self.maBaseUrl + image.find('a').get('href') for image in images if
                              isinstance(image, bs4.element.Tag)]
                [youjiDetailUrls.append(detailUrl) for detailUrl in detailUrls]
                time.sleep(2)
                ActionChains(driver).click(driver.find_element_by_css_selector("[class='pi pg-next']")).perform()
            except Exception as e:
                self.logging(str(e), 'mafengwo.txt', 'a')
                break
        driver.close()
        # 爬取这些游记的详情信息
        try:
            youjis = self.spiderYouJiDetail(youjiDetailUrls)
            item['youji'] = youjis
            self.logging(json.dumps(youjis), 'mafengwo.txt', 'a')
            # 再找酒店攻略
            self.spiderHotelDetail(hotelListUrl)
            # 再找景点攻略
            self.spiderAttractionDetail(attractionListUrl)
            # 再找美食攻略
            self.spiderFoodDetail(foodListUrl)
        except Exception as e:
            self.logging(str(e), 'mafengwo.txt', 'a')
        return item

    # 爬取该城市所有的游记
    def spiderYouJiDetail(self, youjiDetailUrls):
        data = []
        chrome_options = webdriver.ChromeOptions()
        # headless无界面模式
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/lili/software/chromedriver")
        for youjiDetailUrl in youjiDetailUrls:
            driver.get(youjiDetailUrl)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tmp = soup.find('div', class_='_j_content_box')
            if tmp is None:
                continue
            content = tmp.get_text()
            imgs = tmp.find_all('img')
            imgs = [img.get('data-rt-src') for img in imgs if isinstance(img, bs4.element.Tag) and img.get('data-rt-src') is not None]
            data.append({
                'content': content,
                'imgs': imgs
            })
        return data

    def spiderHotelDetail(self, hotelListUrl):
        return []

    def spiderAttractionDetail(self, attractionListUrl):
        return []

    def spiderFoodDetail(self, foodListUrl):
        return []

    def logging(self, string, file, method):
        file = open(file, method, encoding='utf-8')
        file.write(string)
        file.close()