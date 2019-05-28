# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderCoreItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    air_No = scrapy.Field()  # 航班号  a
    f_start_time = scrapy.Field()  # 起飞时间 a
    f_end_time = scrapy.Field()  # 降落时间 a
    del_flag = scrapy.Field()  # 删除标志  0:删除 1:未删除
    f_source_place = scrapy.Field()  # 起飞地点 a
    f_end_place = scrapy.Field()  # 降落地点 a
    position = scrapy.Field()  # 舱位 a
    price = scrapy.Field()  # 价格 a
    ticket_number = scrapy.Field()  # 票张数 默认为0  (已经去掉了没有的票) a
    currency = scrapy.Field()  # 货币 a
    image_url = scrapy.Field()  # 图片地址  a
    discount_start_time = scrapy.Field()  # 打折开始时间 a
    discount_end_time = scrapy.Field()  # 打折结束时间 a
    create_time = scrapy.Field()  # 创建时间 a
    version = scrapy.Field()  # 版本号 初始值为1 a
    area = scrapy.Field()  # 去的范围  a
    mark = scrapy.Field()  # 备用字段
    detail_url = scrapy.Field()  # 详细url
    pass
