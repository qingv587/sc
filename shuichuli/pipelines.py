# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import time
import re
from scrapy.selector import Selector

class ShuichuliPipeline(object):
    count = 0

    def process_item(self, item, spider):

        # file_name = 'download/%s.txt' % (item['title'],)
        # print(file_name)

        # with open(file_name, 'w') as f:
        #     a_ls = item['answer_list'].xpath("node()").extract()
        #     for i in a_ls:
        #         print(i)
        #         f.write(i+"\n")
        #         # sxh = Selector(text=i)
        #         # content_list = sxh.xpath('./node()').extract()
        #         # for j in content_list:
        #         #     f.write(j+"\n")
        self.key = item["key"]
        if len(item["answer_list"]) >1:
            itemid = self.latest_itemid +1
            title = item["title"].encode("gbk",'ignore').decode("gbk",'ignore')
            catid = item["catid"]
            dtime = int(time.time())
            process = 1
            status = 2
            a_status = 3
            keyword = title
            linkurl = "show-%s.html" % (itemid,)
            qid = itemid
            content = item["vote"].encode("gbk",'ignore').decode("gbk",'ignore') if item["vote"] else title
            areaid = 0
            answer = len(item["answer_list"])
            addition = ""
            comment = ""
            pptword = ""
            passport = ""
            ask = ""
            expert = ""
            ip = ""
            url = ""
            null = ""
            try:
                self.cursor.execute(self.know_sql,[itemid, catid, title, process, keyword, dtime, dtime, dtime, status, linkurl, areaid,addition,comment, pptword, passport,ask,expert,ip,answer])
                self.cursor.execute(self.know_data_sql,[itemid, content])
                for sel in item["answer_list"]:
                    a_list = sel.xpath('./node()').extract()
                    a_text = "\n".join(a_list)
                    rc = re.compile(r"(<img.*?>)|(<script.*?>)|(<a.*?</a>)|(<frame.*?>)")
                    text = rc.sub("",a_text)
                    if len(text) >10:
                        # print("content数量:",len(text))
                        try:
                            self.cursor.execute(self.answer_sql,[qid,text.encode("gbk",'ignore').decode("gbk",'ignore'),dtime,a_status,null,null,null])
                        except Exception as ex:
                            print("编码有误！")
                self.count += 1
            except Exception as e:
                print("写入数据库出错了",e)
                with open("dberror","a",encoding="utf8") as f_db:
                    f_db.write(title.encode("utf8",'ignore').decode("utf8",'ignore')+"----------"+str(e)+"\n")
        print("计数：", self.count)
        return item

    def open_spider(self, spider):
        self.conn = pymysql.connect(host="114.112.103.228", port=3306, db="dy88", user="root", password="dayu88@#mysql",charset="gbk")
        # self.conn = pymysql.connect(host="localhost",port=3306,db = "destoon",user="root",password="root",charset= "utf8")

        self.cursor =self.conn.cursor()
        self.know_sql = "INSERT INTO destoon_know_10(itemid, catid, title, process, keyword, addtime, totime, edittime, status, linkurl, areaid, addition, comment, pptword, passport,ask,expert,ip,answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        self.know_data_sql = "INSERT INTO destoon_know_data_10(itemid, content) VALUES (%s, %s)"
        self.answer_sql = "INSERT INTO destoon_know_answer_10(qid, content, addtime, status, url, passport, ip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.sel_sql = "select itemid from destoon_know_10"

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        with open("记录","a",encoding="utf8") as f:
            f.write(self.key+":"+str(self.count)+"\n")

    @property
    def latest_itemid(self):
        self.cursor.execute(self.sel_sql,[])
        itemid = self.cursor.fetchall()[-1][0]
        return itemid