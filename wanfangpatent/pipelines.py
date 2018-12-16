# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymysql
from scrapy.utils.project import get_project_settings
import pymssql


class WanfangpatentPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        self.host = settings["DB_HOST"]
        self.port = settings["DB_PORT"]
        self.user = settings["DB_USER"]
        self.pwd = settings["DB_PWD"]
        self.name = settings["DB_NAME"]
        self.charset = settings["DB_CHARSET"]

        self.connect()

    def connect(self):
        # self.conn = pymssql.connect(host=self.host,
        #                             port=self.port,
        #                             user=self.user,
        #                             password=self.pwd,
        #                             database=self.name,
        #                             charset=self.charset)
        # self.cursor = self.conn.cursor()
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.user,
                                    password=self.pwd,
                                    database=self.name,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def colose_spider(self, spider):
        self.conn.close()
        self.cursor.close()

    def process_item(self, item, spider):
        # 查重处理
        self.cursor.execute(
            """select * from sd_patent where applynumber = '%s'""" % item['applynumber'])
        # 是否有重复数据
        repetition = self.cursor.fetchone()

        # 重复
        # if repetition:
        #     spider.logger.info(msg='此条重复抓取，没有存入数据库')
        # else:
        #     sql = """insert into sd_patent(title,inventors,inventors_first,pubnumber,type,applynumber,apply_date,success_date, abstract_text,IPC,IPC_main,applicants,applicants_first,area,applicants_first_address,law_status,source)
        #           VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" \
        #           % (
        #               item['title'], item['inventors'], item['inventors_first'], item['pubnumber'], item['type'],
        #               item['applynumber'],item['apply_date'], item['success_date'], item['abstract_text'], item['IPC'],
        #               item['IPC_main'],item['applicants'], item['applicants_first'], item['area'],
        #               item['applicants_first_address'], item['law_status'],item['source']
        #           )
        #     try:
        #         self.cursor.execute(sql)
        #         self.conn.commit()
        #         # print('添加一条新数据')
        #     except Exception as e:
        #         print(sql)
        #         spider.logger.error(msg='存入数据库失败 %s' %e)
        # return item
        if repetition:
            spider.logger.info(msg='此条重复抓取，没有存入数据库')
        else:
            sql = """insert into sd_patent(title,inventors,inventors_first,pubnumber,type,applynumber,apply_date,success_date, abstract_text,IPC,IPC_main,applicants,applicants_first,area,applicants_first_address,law_status,source)
                  VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" \
                  % (
                      pymysql.escape_string(item["title"]) if item["title"] is not None else None,
                      pymysql.escape_string(item["inventors"]) if item["inventors"] is not None else None,
                      pymysql.escape_string(item["inventors_first"]) if item["inventors_first"] is not None else None,
                      item["pubnumber"], item["type"],
                      item['applynumber'], item['apply_date'], item['success_date'],
                      pymysql.escape_string(item["abstract_text"]) if item["abstract_text"] is not None else None,
                      item['IPC'],
                      item['IPC_main'],
                      pymysql.escape_string(item["applicants"]) if item["applicants"] is not None else None,
                      pymysql.escape_string(item["applicants_first"]) if item["applicants_first"] is not None else None,
                      pymysql.escape_string(item["area"]) if item["area"] is not None else None,
                      pymysql.escape_string(item["applicants_first_address"]) if item["applicants_first_address"] is not None else None,
                      item['law_status'], item['source']

                  )
            try:
                self.cursor.execute(sql.replace("'None'", pymysql.NULL))
                self.conn.commit()
                # print('添加一条新数据')
            except Exception as e:
                print(sql)
                spider.logger.error(msg='存入数据库失败 %s' % e)
        return item
