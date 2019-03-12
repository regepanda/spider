# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from spider.items import LiajiaItem


class LiajiaPipeline(object):
    def open_spider(self, spider):
        """
        爬虫运行时，执行的方法
        :param spider:
        :return:
        """
        self.file = open('lianjia.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):

        content = json.dumps(dict(item), ensure_ascii=False)

        # 判断数据来源于哪里（是哪个类的实例），写入对应的文件
        if isinstance(item, LiajiaItem):
            self.file.write(content + '\n')

        return item

    def close_spider(self, spider):
        """
        爬虫运行结束后执行的方法
        :param spider:
        :return:
        """
        self.file.close()
