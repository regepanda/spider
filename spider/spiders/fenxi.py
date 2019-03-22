# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
import time

if __name__ == '__main__':
    url = 'http://www.mafengwo.cn/i/11815590.html'
    chrome_options = webdriver.ChromeOptions()
    # headless无界面模式
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/lili/software/chromedriver")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find('div', class_='_j_content_box').get_text()
    imgs = soup.find('div', class_='_j_content_box').find_all('img')
    imgs = [img.get('data-rt-src') for img in imgs if isinstance(img, bs4.element.Tag)]



