# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MzituScrapyItem(scrapy.Item):
    # define the fields for your item here like:

    # 当前图片主题名称
    img_theme_name = scrapy.Field()

    # 图片主题 URL
    img_theme_url = scrapy.Field()

    # 当前主题的所有图片的URL
    all_img_urls_of_theme = scrapy.Field()


