import pymysql
import requests
from lxml import etree
import time

if __name__ == '__main__':

    url = 'http://www.gaosan.com/gaokao/150429.html'
    db = pymysql.connect("localhost", "root", "root", "spiderkeeper", charset='utf8')  # 连接MySQL
    cur_sql = db.cursor()
    num = 0
    for i in range(1, 51):
        time.sleep(1)
        url = 'http://c.old.wanfangdata.com.cn/PeriodicalLetter.aspx?NodeId=Z&IsCore=false&PageNo=' + str(i)
        response = requests.get(url=url)
        selector = etree.HTML(response.text)

        periodical_name_list = selector.xpath('//div[@class="list"]/span/a[@class="link"]/text()')
        # print(periodical_name_list)
        for periodical_name in periodical_name_list:
            sql = """insert into periodical_list(name) VALUES ("%s")""" % periodical_name.replace(' ','').replace('\r\n','')
            try:
                cur_sql.execute(sql)
                db.commit()
            except Exception as e:
                pass
        print(i)
