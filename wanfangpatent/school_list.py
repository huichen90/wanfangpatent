import pymysql
import requests
from lxml import etree


if __name__ == '__main__':

    url = 'http://www.gaosan.com/gaokao/150429.html'
    db = pymysql.connect("localhost", "root", "root", "spiderkeeper", charset='utf8')  # 连接MySQL
    cur_sql = db.cursor()
    response = requests.get(url=url)

    selector = etree.HTML(response.text)

    school_name_list = selector.xpath('//tbody/tr/td[2]/text()')
    for school_name in school_name_list:
        sql = """insert into school(name) VALUES ("%s")""" % school_name
        cur_sql.execute(sql)

    db.commit()
