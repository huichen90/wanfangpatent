class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        """
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        """


        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = 'zh_choose=n; firstvisit_backurl=http%3A//www.wanfangdata.com.cn; Hm_lvt_838fbc4154ad87515435bf1e10023fab=1534485973,1534497384,1534726402; SEARCHHISTORY_0=UEsDBBQACAgIAAtYFE0AAAAAAAAAAAAAAAABAAAAMO3YfUvbQBgA8O%2BSP8YG6czbJRdBhi9Th646%0AV3zZGCVtzi4S03q51pchOJhaBJkydWPKNoRNBtMNZNCxyT7MmqrfYk%2FaqS00bg7RDfJP8twlF%2B5%2B%0AuST35P4jjhkJm0SNUcI1Olnb5jnL5Bq5aDRrSdgcUhWJ47msS%2Bgt8%2BgElxg0%2BTA2mYEmIhykNjRo%0AqNT2ETdrs4YUYc1mznCSxLxbrr9upm8waNGUMRhxWKSyixObjML%2BissoVKQmm4p7Gwczs97ianFv%0AsfFqsbDtre%2Ftr3z2tpf2t5ZLCzOH63Pe%2BqY3%2B8F7WrgGPSMTGUpc10o70IezNmblIXDFwjMv%2Fx7K%0ATna0PZ11YKCiImCF55KUQLdilo8jIlnRZEFUFTCZ5oPghpOZlr5Ef48sqRcLV%2Fh6uPni7GR%2F3OwU%0ArDpQkqYjCQyCoWTU2sV6B1wV6eEMO4ZTdKxiDCbBcEZKn1J6jU4di%2BcLl0w7w4QSOBLxw7hBmZU0%0A7Eum%2B%2FbyYGenhk7BglxHDutIw4ASLDfUerOvA4aoKEo45argNE1TwSQYTm1OtJmUTmIxhKuGU7Eo%0AgkkwXGeMojQxYxpCIVw1nAZfCISC4e5J%2Ff0u7pNlHK4%2FauAEwTc5ZcblEu3dt3OjCJ3z1%2BF%2FhxMF%0AFUyC4ZrN8W7U0tmBVCGEq3nHCQKYBMPR3kR0YujWoK7jEK4GTkZgEgyndI6Lua5sTpTCd1zNOk7G%0AGEyC4RJOFA%2FI1ELhk1qdOWhI0AV0ypPan4xhp8tuUc99NUKolY6Ut0dZA2%2BSFCUkUtkd1wbkGHxd%0Aet5lhmMa1HQjxxHPyFGHIn4Yp%2BWYt0nKcm2DgbYbqS6UGxydmklTxqeMKcIYITTukPHIccn1iyd3%0AG9Jib2mxlF%2FzZncPV3YOPp79nv%2FdJX7d%2BdLGay%2B%2F8GPmsbf9DuYMBJVUyA%2FKkwKC0pt5b34OgsqV%0ASvml0qsNv3539WDryUn9wltvuXypjU%2BltS%2Fe9%2Bc1E0oT9HoZvKqomnraGi06NkKmBsUxLF7wr45%2F%0A%2Bjn0f32oEpgEw1kT4h23py0HWdclwiWINWI5qd8IVZ0VTKEJGNf7W6YIkgSDnH7wE1BLBwjIyd4Z%0AMAMAAGgUAAA%3D%0A; WFKS.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%5d%2c%22Data%22%3a%5b%5d%2c%22SessionId%22%3a%22dc7b6609-f272-475a-b5a6-522569c6e519%22%2c%22Sign%22%3a%22hi+authserv%22%7d%2c%22LastUpdate%22%3a%222018-08-20T03%3a31%3a11Z%22%2c%22TicketSign%22%3a%220SzvhdB3c5qD1yWQOan7qA%3d%3d%22%7d; CASTGC=TGT-4874220-a7ZI0n1i4TGSMG6d3haOEPXwfGyHmQbVUpljZOqccYLDN1Zw9V-my.wanfangdata.com.cn; JSESSIONID=AF7143225CDD32E21F94109B730D7C49; Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1534739466'
    trans = transCookie(cookie)
    print(trans.stringToDict())