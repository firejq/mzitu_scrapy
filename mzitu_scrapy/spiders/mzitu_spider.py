# -*- coding: utf-8 -*-
# Author： firejq
# Created on 2017/9/6
import scrapy
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from mzitu_scrapy.items import MzituScrapyItem


class MzituSpider(CrawlSpider):
    """mzitu spider"""
    name = 'mzitu_spider'

    allow_domains = ['mzitu.com']

    start_urls = ['http://www.mzitu.com/']

    # 定义rules：抓取所有主题的URL
    rules = [
        Rule(link_extractor=LinkExtractor(
            allow='http://www.mzitu.com/\d{1,6}',
            deny='http://www.mzitu.com/\d{1,6}/\d{1,6}'),
            callback='parse_item',
            follow=True
        )
    ]

    # 用于存储每个主题的全部图片的URL
    all_img_urls_of_theme = []

    def parse_item(self, response):
        """获取当前主题所有页面的所有图片的URL，以构造并返回该主题的MzituScrapyItem对象

        :param response:
        :return: MzituScrapyItem
        """
        print(response.url)
        mzitu_scrapy_item = MzituScrapyItem()
        mzitu_scrapy_item['img_theme_name'] = response.xpath(
            '/html/body/div[2]/div[1]/h2/text()').extract_first(default="N/A")
        mzitu_scrapy_item['img_theme_url'] = response.url

        max_page_num = response.xpath(
            "descendant::div[@class='main']"
            "/div[@class='content']/div[@class='pagenavi']"
            "/a[last()-1]/span/text()").extract_first(default="N/A")
        for num in range(1, int(max_page_num)):
            # img_page_url 为图片所在的页面地址
            img_page_url = response.url + '/' + str(num)
            # 遍历该主题的所有页面，将该主题下的所有图片URL添加到all_img_urls_of_theme
            yield Request(img_page_url, callback=self.get_all_img_urls_of_page)

        mzitu_scrapy_item['all_img_urls_of_theme'] = self.all_img_urls_of_theme
        yield mzitu_scrapy_item

    def get_all_img_urls_of_page(self, response):
        """获取当前页面每张图片的URL，添加到 self.all_img_urls_of_theme 列表中

        :param response:
        :return:
        """
        # 当前页面的所有图片的URL(List)
        all_img_urls_of_page = response.xpath("descendant::div[@class="
                                              "'main-image']/descendant"
                                              "::img/@src").extract()
        for img_url in all_img_urls_of_page:
            self.all_img_urls_of_theme.append(img_url)

















