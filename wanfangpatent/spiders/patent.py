# -*- coding: utf-8 -*-
import json
import random

import pymysql
import scrapy
import time
from scrapy import Request
from scrapy.conf import settings
from scrapy.utils import spider

from wanfangpatent.items import WanfangpatentItem


class PatentSpider(scrapy.Spider):
    name = 'patent'

    def __init__(self, *args, **kwargs):
        super(PatentSpider, self).__init__(*args, **kwargs)

        self.db = pymysql.connect("localhost", "root", "root", "spiderkeeper", charset='utf8')  # 连接MySQL
        self.cur_sql = self.db.cursor()

        self.allowed_domains = ['www.wanfangdata.com.cn', 'g.wanfangdata.com.cn', 'common.wanfangdata.com.cn']
        random_num = round(random.random(), 15)  # 随机数精度要求
        url1 = 'http://www.wanfangdata.com.cn/searchResult/getCoreSearch.do?d=' + str(random_num)
        # self.start_urls = ["http://www.wanfangdata.com.cn/searchResult/getAdvancedSearch.do?searchType=all"]
        self.start_urls = [url1]

        # self.paramStrs = paramstrs
        self.startDate = 2008
        self.endDate = 2018
        self.updateDate = ''
        self.classType = 'patent-patent_element'
        # self.pageNum = 0
        self.pageSize = 1000
        self.sortFiled = ""
        self.isSearchSecond = 'false'
        self.pageTotal = 10

    headers = {
        'Accept': 'json',
        'Accept-Language': 'zh - CN, zh;q = 0.9',
        'Connection': 'keep-alive',  # 保持链接状态
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.wanfangdata.com.cn',
        'Origin': 'http://www.wanfangdata.com.cn',
        'Referer': 'http://www.wanfangdata.com.cn/searchResult/getAdvancedSearch.do?searchType=all',
        'DNT': 1,
        'X-Requested-With': 'XMLHttpRequest',
    }

    def start_requests(self):  # 用来确定一共多少页
        # sql1 = """select orgnization_name from orgnizations where num=1 limit 0,100 """
        sql1 = """select name from ipc where num=0 """
        self.cur_sql.execute(sql1)
        results = self.cur_sql.fetchall()
        # results = ['山西铝厂',  '华电水务工程有限公司', '中国电子科技集团公司', ]
        for row in results:
            random_num = round(random.random(), 15)  # 随机数精度要求
            url1 = 'http://www.wanfangdata.com.cn/searchResult/getCoreSearch.do?d=' + str(random_num)
            name = row[0]
            paramStrs = '专利—主分类号:(%s)' % row[0]
            pageNum = 0
            form_data = {'paramStrs': paramStrs,
                         'startDate': str(self.startDate),
                         'endDate': str(self.endDate),
                         'updateDate': str(self.updateDate),
                         'classType': self.classType,
                         'pageNum': str(pageNum),
                         'pageSize': str(self.pageSize),
                         'sortFiled': self.sortFiled,
                         'isSearchSecond': self.isSearchSecond,
                         }  # 表单数据，字典格式，注意数字也要用引号引起来，否则报错。
            yield scrapy.FormRequest(url=url1, method='POST', headers=self.headers, formdata=form_data,
                                     callback=self.parse, dont_filter=True,
                                     meta={'paramStrs': paramStrs, 'pageNum': pageNum, 'name': name})  # 还可以通过callback修改回调函数等

    def parse(self, response):
        paramStrs = response.meta['paramStrs']
        pageNum = response.meta['pageNum']
        name = response.meta['name']
        obj = json.loads(response.text)
        pageTotal = obj.get('pageTotal', 1)
        totalRow = obj.get('totalRow', 0)
        spider.logger.info(msg="%s专利共%d页，总数为：%d" % (paramStrs, pageTotal, totalRow))
        while pageNum <= pageTotal != 0:
            time.sleep(1)

            random_num = round(random.random(), 15)  # 随机数精度要求
            url1 = 'http://www.wanfangdata.com.cn/searchResult/getCoreSearch.do?d=' + str(random_num)
            url2 = 'http://g.wanfangdata.com.cn/searchResult/getCoreSearch.do?d=' + str(random_num)
            form_data = {'paramStrs': paramStrs,
                         'startDate': str(self.startDate),
                         'endDate': str(self.endDate),
                         'updateDate': str(self.updateDate),
                         'classType': self.classType,
                         'pageNum': str(pageNum),
                         'pageSize': str(self.pageSize),
                         'sortFiled': self.sortFiled,
                         'isSearchSecond': self.isSearchSecond,
                         }  # 表单数据，字典格式，注意数字也要用引号引起来，否则报错。

            pageNum = 1 if pageNum == 0 else pageNum
            spider.logger.info(msg="正在爬去%s专利的第%d页" % (paramStrs, pageNum))
            url = random.choice([url2, url1])
            if pageNum == 0:
                pageNum = 2
            else:
                pageNum += 1
            yield scrapy.FormRequest(url=url, method='POST', headers=self.headers, formdata=form_data,
                                     callback=self.parse_info, dont_filter=True)  # 还可以通过callback修改回调函数等
        self.cur_sql.execute("UPDATE ipc SET num =%d WHERE name='%s'" % (1, name))
        self.db.commit()
        spider.logger.info(msg="%s专利已爬取完毕" % paramStrs)

    def parse_info(self, response):
        """
        处理返回的信息
        :param response:
        :return:
        """
        obj = json.loads(response.text)
        item = WanfangpatentItem()
        pageRow = obj.get('pageRow')
        if pageRow is not None:
            for patent in pageRow:
                item['title'] = patent.get('title').replace("<em>", "").replace("</em>", "") if patent.get('title') is not None else None # 专利标题
                item['inventors'] = '|'.join(patent.get('inv_name')) if isinstance(patent.get('inv_name'), list) else patent.get('inv_name')  # 发明人
                item['inventors_first'] = patent.get('inv_name')[0] if isinstance(patent.get('inv_name'), list) else patent.get('inv_name')  # 第一发明人
                item['pubnumber'] = patent.get('pub_num')  # 公开号
                item['type'] = patent.get('patent_type')  # 专利类型
                item['applynumber'] = patent.get('app_num')  # 专利申请号
                item['apply_date'] = patent.get('app_date02')  # 专利申请日期
                item['success_date'] = patent.get('pub_date')  # 专利成功日期
                item['abstract_text'] = self.translation(patent.get('summary')).strip()  # 摘要
                item['IPC'] = ','.join(patent.get('class_code')) if isinstance(patent.get('class_code'), list) else patent.get('class_code') # 专利分类号
                item['IPC_main'] = ','.join(patent.get('main_classcode')) if isinstance(patent.get('main_classcode'), list) else patent.get('main_classcode')  # 主分类号
                item['applicants'] = '|'.join(patent.get('applicant_name')) if isinstance(patent.get('applicant_name'), list) else patent.get('applicant_name')  # 专利申请人
                item['applicants_first'] = patent.get('applicant_name')[0] if isinstance(patent.get('applicant_name'), list) else patent.get('applicant_name')  # 第一专利申请人
                item['area'] = patent.get('app_area_code') if patent.get('app_area_code') is None else patent.get('app_area_code')[:-3]  # 地区
                item['applicants_first_address'] = patent.get('app_address')  # 第一专利申请人地址
                item['law_status'] = patent.get('legal_status')  # 法律状态
                item['source'] = '万方数据'  # 数据来源
                yield item

    def translation(self, instring):
        """
        去掉数据中的空格换行等字符
        :param instring:
        :return:
        """
        move = dict.fromkeys((ord(c) for c in u"\xa0\n\t|│’‘\'“”\"&#39&quot"))
        outstring = instring.translate(move)
        # outstring=Converter('zh-hans').convert(outstring)
        return outstring