#!/usr/bin/env python
# -*- coding:utf-8 -*-
import configparser
import pymysql

import pymysql as ps


class MysqlHelper:
    def __init__(self, filePath=None):
        cf = configparser.ConfigParser()
        if filePath is not None:
            cf.read(filePath, encoding='utf-8')
        else:
            cf.read("./dataBase.txt", encoding='utf-8')
        host = cf.get("db", "db_host")
        port = int(cf.get("db", "db_port"))
        user = cf.get("db", "db_user")
        password = cf.get("db", "db_pass")
        database = cf.get("db", "db_pass")
        charset = cf.get("db", "charset")
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None
        self.open()

    # 数据库连接
    def open(self):
        if self.curs is None:
            self.db = ps.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                 database=self.database,
                                 charset=self.charset)
            self.curs = self.db.cursor()

    # 数据库关闭
    def close(self):
        self.curs.close()
        self.db.close()

    # 数据增删改
    def cud(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            self.db.commit()
            print("ok")
        except:
            print('cud出现错误')
            self.db.rollback()
        self.close()

    # 数据查询
    def find(self, sql, params):
        self.open()
        try:
            result = self.curs.execute(sql, params)
            self.close()
            print("ok")
            return result
        except:
            print('find出现错误')


if __name__ == '__main__':
    pass
