# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent
from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from scrapy.http import HtmlResponse, Response

import logging

logger = logging.getLogger(__name__)


class SpiderCoreSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    @staticmethod
    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.http import HtmlResponse
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re


class SpiderCoreDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        ua = UserAgent().random
        request.headers.setdefault('User-Agent', ua)
        # pass

        # chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # # 指定谷歌浏览器路径
        # self.driver = webdriver.Chrome(chrome_options=chrome_options,
        #                                executable_path='D://BDCloundDown//chromedriver')
        # print("request.url:", request.url)
        # print("request.method:", request.method)
        # if request.method != 'POST':
        #     self.driver.get(request.url)
        #     time.sleep(1)
        #     html = self.driver.page_source
        #     self.driver.quit()
        #     return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
        #                                     request=request)
        # from_data = {
        #     'UserNameInput': 'LarvwuAX3KTyBFXtXkCcjcFRLzpSb/Ft6P1r29CxZcOlpn9Le8Q+LCQ3iTeXnW2ZdCKJsmA0tOyn4wF4C92vjs1Tg11lGxaroeAgGmSgZvBqyLQha2UNOM/MDHMroF1m9W5j92oe2jg2QPS4rTsCVRsnMcZCCd3y2iY/2/PBtx0=',
        #     'undefined': '0',
        #     'PasswordInput': ' dAaIbU2BmGOtFUVYm/gEM5yaZojqmtjifUJP2N+gkamNFyBqwec5ETXZFcji8orszLywEZPaJ1fQHOvZidQKhWLNtKDqBObcbrXlwgsQuX7ePqYBtP6qAc5JIQ/tfPcPYT6S0s4cCdAWGzyitt/L0jqf27XCael00UjFFLDswAU=',
        #     'IsKeepLoginState': 'true',
        #     'loginType': 'PC',
        # }
        #
        # return scrapy.FormRequest(url='https://passport.ch.com/zh_cn/Login/DoLogin',
        #                           formdata=from_data,
        #                           callback=ChunqiuSpider.islogin)

        if spider.name == 'chunqiu':
            if 'AirFlights/ActivitiesSecondKill' in request.url:
                options = Options()
                options.add_argument('-headless')

                # geckodriver需要手动下载
                driver = Firefox(executable_path='D:\\softpackage\\geckodriver', firefox_options=options)
                # driver.manage().addCookie(new Cookie("Name", "value", "域名", "/", 生效时间, false, false));

                driver.get(request.url)

                time.sleep(3)

                driver.add_cookie(
                    self.ReadTxtName('./cookie.txt')
                )
                # searchText = driver.find_element_by_xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a')[0].text
                #  search_results = WebDriverWait(driver,10).until(
                #      # lambda d: d.find_elements_by_xpath('//h3[@class="t c-title-en"] | //h3[@class="t"]')
                #      lambda e: e.find_elements_by_xpath('//div[contains(@class,"threadlist_title pull_left j_th_tit ")]/a[1]')
                #  )
                #  for item in search_results:
                #      print(item.text)  # 打印搜索内容的标题

                html = driver.page_source
                driver.quit()

                # 构建response, 将它发送给spider引擎
                return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

    def ReadTxtName(self, dir):
        dict_cookies = {}
        with open(dir, 'r') as file_to_read:
            while True:
                line = file_to_read.readline()
                if not line:
                    break

                dict_cookies['Name'] = line.split(';')[0]
                dict_cookies['Value'] = line.split(';')[1]

                expires = re.compile('.*expires=(.*?);', re.DOTALL).findall(line)
                if len(expires) > 0:
                    dict_cookies['Expires'] = expires[0]

                sss = re.search(';path=.*', line, re.IGNORECASE)
                if sss:
                    dict_cookies['Path'] = sss.group().split('=')[1]

                domain = re.compile('.*domain=(.*?);', re.DOTALL).findall(line)
                if len(domain) > 0:
                    dict_cookies['Domain'] = domain[0]

                if len(re.compile('.*httpOnly=(.*?);', re.DOTALL).findall(line)) > 0:
                    dict_cookies['HttpOnly'] = True
                else:
                    dict_cookies['HttpOnly'] = False
                dict_cookies['Secure'] = True

        return dict_cookies

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
