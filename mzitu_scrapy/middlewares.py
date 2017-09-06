# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import requests
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


# class MzituScrapySpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            request.meta['proxy'] = get_proxy_ip()
        except Exception as error:
            print(error)


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', get_random_useragent())


def get_proxy_ip():
    """爬取http://www.xicidaili.com/nn/首页的高匿代理ip

    :return: 可用的代理ip
    """
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/53.0.2785.143 Safari/537.36')
    }
    url = 'http://www.xicidaili.com/nn/'
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    # ip_list为可用的代理ip列表
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)

    # 随机选择一个可用的代理ip
    proxy_ip = ''.join(str(random.choice(ip_list)).strip())
    return proxy_ip


def get_random_useragent():
    """返回一个随机user-agent
    :return:
    """
    user_agents = [
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/60.0.3072.0 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 '
         'Firefox/46.0'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,'
         ' like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 '
         '(KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
         '(KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'),
        ('Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) '
         'like Gecko'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36'),
        ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 '
         'QQBrowser/9.4.7658.400'),
        ('Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) '
         'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
         'Chrome/37.0.0.0 Mobile Safari/537.36 '
         'MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI'),
        ('Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) '
         'AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 '
         'QQ/5.2.1.302 NetType/WIFI Mem/28')
    ]
    return random.choice(user_agents)