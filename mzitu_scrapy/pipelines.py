# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


class MzituScrapyPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return item

    def get_media_requests(self, item, info):
        return super().get_media_requests(item, info)

    def file_path(self, request, response=None, info=None):
        """

        :param request:
        :param response:
        :param info:
        :return:
        """
        item = request.meta['item']
        folder = item['name']
        folder_strip = strip(folder)
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def item_completed(self, results, item, info):
        return super().item_completed(results, item, info)




















