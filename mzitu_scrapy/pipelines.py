# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


def strip(filename):
    """
    :param filename:
    :return: 去除Windows系统非法文件夹名字的字符串
    """
    return re.sub(r'[？\\*|“<>:/]', '', str(filename))


class MzituScrapyPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return item

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for img_url in item['all_img_urls_of_theme']:
            referer = item['img_theme_url']
            yield Request(img_url, meta={'item': item,
                                         'referer': referer})

    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :return: 每个主题的分类目录
        """
        item = request.meta['item']
        folder = strip(item['img_theme_name'])
        image_guid = request.url.split('/')[-1]
        # 拼接最终的文件名，格式：full/{folder}/{image_guid}.jpg
        filename = u'full/{0}/{1}'.format(folder, image_guid)
        return filename

    def item_completed(self, results, item, info):
        """
        :param results:
        :param item:
        :param info:
        :return:
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

# class MzituScrapyPipeline(object):
#     def process_item(self, item, spider):
#         print(item['img_theme_name'])
#         for img_url in item['all_img_urls_of_theme']:
#             print(img_url)