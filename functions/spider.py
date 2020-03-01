import requests
import re
import pymysql


class NewsSpider(object):
    def __init__(self):
        self.url = 'http://www.soft6.com/'
        self.db = pymysql.connect('localhost', 'root', '123456', 'outsource', charset='utf8')
        self.cursor = self.db.cursor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0;'
                          ' Windows NT 6.1; Win64; x64; Trident/5.0;'
                          ' .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729;'
                          ' .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3;'
                          ' .NET4.0C; Tablet PC 2.0; .NET4.0E)'}

    def get_info(self):
        html = requests.get(url=self.url, headers=self.headers).content.decode()
        regex = '<div class="bd main-left-list">(.*?)</ul>'
        regex2 = '<li>.*?src="(.*?)".*?>.*?href="(.*?)">(.*?)</a></h2>.*?>(.*?)</small>.*?<p><span>(.*?)</span>.*?</li>'
        pattern = re.compile(regex, re.S)
        print("*" * 50, pattern)
        result = pattern.findall(html)[0]
        print("-" * 50, pattern.findall(html)[0])
        pattern2 = re.compile(regex2, re.S)
        info_list = pattern2.findall(result)
        for info in info_list:
            print(info)
            self.save_info(info)

    def save_info(self, info):
        news_title = info[2]
        news_tip = info[-2]
        image_url = info[0]
        created_at = info[-1]
        news_detail_url = info[1]
        # ins = 'insert into outsource_news(news_title,news_tip,image_url,created_at,index,news_detail_url) values(%s,%s,%s,%s,%s,%s)'
        ins = 'insert into news(news_title, news_tip, image_url, created_at, news_detail_url) values(%s,%s,%s,%s,%s)'
        print([news_title, news_tip, image_url, created_at, news_detail_url])
        self.cursor.execute(ins, [news_title, news_tip, image_url, created_at, news_detail_url])
        self.db.commit()
        print('存入数据库成功')

    def run(self):
        self.get_info()
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    spider = NewsSpider()
    spider.run()
