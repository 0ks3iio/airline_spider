# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from urllib import parse
import datetime
import uuid
import logging
import os, sys
from fake_useragent import UserAgent
import json

from selenium import webdriver
import http.cookiejar

import re

from scrapy.http.cookies import CookieJar

cookie_jar = CookieJar()

ua = UserAgent()
to_date = datetime.datetime.now()

import pickle


# todo  现在无法获取价格参数
# todo  发生抓取数据异常建议发送邮件 保证数据最新性

class ChunqiuSpider(scrapy.Spider):
    name = 'chunqiu'
    allowed_domains = ['ch.com']
    start_urls = ['https://pages.ch.com/second-kill/']
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36", }


    def start_requests(self):

        """
               重载start_requests方法 待登录成功后，再进入parse进行数据爬取
                   访问登录页面 并调用do_login方法进行登录
               """
        # 春秋通过算法把字符串加密了
        # 17673119082
        # flyfly123
        from_data = {
            'UserNameInput': 'DipmHSQzWRuS4uJuNgip4uoYNobVz/uf4SrS3FVQs0NmezAl6rxw/56oOvDWLmDSS8GvjTd0Or665VuPS4TxH4tR09Ns+BF1U+F3H3SXdhOqSRNLOtLVfDPVXaEwy5WiEpsOpaBh2fLK8ykda3za3IuZQNO/OJcS8NkmVJ3ioW8=',
            'undefined': '0',
            'PasswordInput': 'C3d861CHT2t7QVGr4Nq3FhWBWPp21uBZ8xNkOB8Dprg0DA7fwKBz4ngkwQjlDqoH/YJRK7x+++LqbZ7EIT7LlBHGf2f5WmVb7ETP6vj3/xYCdRIC+BIozvh27WR1Dw7kkbqmjs9TBh7mgxDRbaabEioF+/v8nfRq/Or9OfKbr8U=',
            'IsKeepLoginState': 'true',
            'loginType': 'PC',
        }
        logging.info("进入start_requests方法")
        yield scrapy.FormRequest(url='https://passport.ch.com/zh_cn/Login/DoLogin',
                                 formdata=from_data,
                                 callback=self.islogin,
                                 headers=self.headers,
                                 dont_filter=True,
                                 meta={'cookiejar': 1}
                                 )

    def islogin(self, response):
        logging.info("进入islogin方法")

        # 保存cookie
        self.save_cookie(response.headers.getlist('Set-Cookie'))

        resp = response.body.decode('utf-8')
        logging.info("jsobj:".format(resp))
        try:
            jsobj = json.loads(resp)
            if jsobj is None or '0' is str(jsobj['Code']):
                yield scrapy.Request(url=self.start_urls[0], callback=self.parse,
                                     meta={'cookiejar': True})
            else:
                raise RuntimeError('登陆失败!时间:{}'.format(to_date))

        except Exception as e:
            # todo 登陆失败
            logging.error('Exception :{}登陆失败!时间:{}'.format(e, to_date))

    def parse(self, response):
        # logging.info('进入解析页面1.....response.content:{}'.format(response.body.decode('utf-8')))
        # 地区  东南亚,日韩,港澳台,境内
        area_list = response.xpath('//h2[@class="red f-cb travel-block"]')
        logging.info('method[parse].....:{}'.format(area_list.getall()))

        for idx, item in enumerate(area_list):
            air_item = {}
            try:
                area_html = response.xpath('//div[@class="m-main g-wp pc-only "]/div')[2:5]
                for item in area_html.xpath('//div[@class="m-sk-area f-cb hot-air"]/div[@class="pic"]'):
                    # 图片
                    air_item['image_url'] = item.xpath('./div[@class="pic1"]/img/@data-src').extract_first()
                    # 获取打折结束时间
                    air_item['discount_start_time'] = item.xpath(
                        '//span[@class="time-span"]/@data-start').extract_first()
                    air_item['discount_end_time'] = item.xpath('//span[@class="time-span"]/@data-end').extract_first()

                    # 创建时间
                    air_item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    air_item['version'] = 1
                    air_item['del_flag'] = 1

                    # air_item['id'] = str(uuid.uuid4())
                    btn_form = item.xpath('./div[@class="pic-bottom"]//form[@class="btn-form"]')
                    detail_url = parse.urljoin(response.url, btn_form.xpath('./@action').extract_first())
                    logging.info('解析详细页面前.....air_item:{}'.format(air_item))
                    yield scrapy.FormRequest(
                        url=detail_url,
                        callback=self.parse_detail,
                        meta={
                            "item": deepcopy(air_item),
                            'cookiejar': True
                        },
                        formdata={
                            'OriCityCode': btn_form.xpath('./input[@name="OriCityCode"]/@value').extract_first(),
                            'DestCityCode': btn_form.xpath('./input[@name="DestCityCode"]/@value').extract_first(),
                            'FlightDateBegin': btn_form.xpath(
                                './input[@name="FlightDateBegin"]/@value').extract_first(),
                            'FlightDateEnd': btn_form.xpath('./input[@name="FlightDateEnd"]/@value').extract_first(),
                            'ActivitiesStartTime': btn_form.xpath(
                                './input[@name="ActivitiesStartTime"]/@value').extract_first(),
                            'ActivitiesEndTime': btn_form.xpath(
                                './input[@name="ActivitiesEndTime"]/@value').extract_first(),
                        }
                    )
            except Exception as e:
                print("error:", e)

    # 解析详细数据
    def parse_detail(self, response):
        # 请求Cookie
        Cookie2 = response.request.headers.getlist('Cookie')
        logging.info('method[parse_detail]:登录时携带请求的Cookies：'.format(Cookie2))
        try:
            air_item = response.meta['item']
            logging.info('解析详细页面中.....air_item:{}'.format(air_item))

            currency = response.xpath('//ul[@class="list-ul2 font14"]/li[@class="li10"]/text()').extract_first()
            ul_list = response.xpath('//ul[@class="list-ul3 font14"]')[1:]
            for item in ul_list:
                # 去除已经售罄的
                if item.xpath('./li[@class="li10"]/a/div/@style').extract_first() is None:
                    continue

                air_item['air_No'] = item.xpath('./li/text()').extract()[0]
                date = item.xpath('./li[@class="li2"]/text()').extract_first()
                air_item['f_start_time'] = date + ' ' + item.xpath('./li[@class="li4"]/text()').extract_first()
                air_item['f_end_time'] = date + ' ' + item.xpath('./li[@class="li5"]/text()').extract_first()

                # 开始地点

                city = item.xpath('./li[@class="li6"]/div[@class="start1"]/text()').extract_first()
                site = item.xpath('./li[@class="li6"]/div[@class="start2"]/text()').extract_first()
                air_item['f_source_place'] = city + site

                # 结束地点
                city = item.xpath('./li[@class="li7"]/div[@class="start1"]/text()').extract_first()
                site = item.xpath('./li[@class="li7"]/div[@class="start2"]/text()').extract_first()
                air_item['f_end_place'] = city + site

                air_item['position'] = item.xpath('./li[@class="li9"]/text()').extract_first()
                print("asfasfa:", item.xpath('./li[last()]'))
                price = item.xpath('./li[last()]//span/text()').extract_first()
                print("pring:::", price)
                if price is not None:
                    air_item['price'] = price.replace('¥', '')
                # todo 价格是动态渲染的
                # air_item['price'] = '99'
                air_item['currency'] = currency

                air_item['detail_url'] = response.url
                # logging.info('解析详细页面后.....air_item:{}'.format(air_item))
            yield air_item
        except Exception as e:
            logging.error("解析详细页面错误:", e)
            pass

    def save_cookie(self, cookie_list):
        with open('./cookie.txt', 'w', encoding='utf-8') as f:
            for i, item in enumerate(cookie_list):
                print(item.decode('utf-8'))
                f.writelines(item.decode('utf-8') + '\n')
            f.close()
