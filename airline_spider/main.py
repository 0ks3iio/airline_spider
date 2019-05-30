#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scrapy.cmdline import execute
import os
import sys

#开发环境下需要删掉日志文件,后续针对环境判断
# def del_file(path):
#     ls = os.listdir(path)
#     for i in ls:
#         c_path = os.path.join(path, i)
#         if os.path.isdir(c_path):
#             del_file(c_path)
#         else:
#             os.remove(c_path)
# del_file(os.getcwd()+'/log')


#添加当前项目的绝对地址
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
execute(['scrapy', 'crawl', 'chunqiu'])