# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WanfangpatentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()                  # 专利标题
    inventors = scrapy.Field()              # 发明人
    inventors_first = scrapy.Field()        # 第一发明人
    pubnumber = scrapy.Field()              # 公开号
    type = scrapy.Field()                   # 专利类型
    applynumber = scrapy.Field()            # 专利申请号
    apply_date = scrapy.Field()             # 专利申请日期
    success_date = scrapy.Field()           # 专利成功日期
    abstract_text = scrapy.Field()          # 摘要
    IPC = scrapy.Field()                    # 专利分类号
    IPC_main = scrapy.Field()               # 主分类号
    applicants = scrapy.Field()             # 专利申请人
    applicants_first = scrapy.Field()       # 第一专利申请人
    area = scrapy.Field()                   # 地区
    applicants_first_address = scrapy.Field()   # 第一专利申请人地址
    law_status = scrapy.Field()             # 法律状态
    source = scrapy.Field()                 # 数据来源

