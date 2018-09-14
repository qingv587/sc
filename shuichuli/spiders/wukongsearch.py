# -*- coding: utf-8 -*-
import scrapy
import time
import json
import copy
from ..items import ShuichuliItem

class WukongsearchSpider(scrapy.Spider):
    name = 'wukongsearch'
    allowed_domains = ['www.wukong.com']
    # https://www.wukong.com/search/?keyword=供水设备
    # ss = "https://www.wukong.com/search/?keyword=供水设备"
    # start_urls = ['https://www.wukong.com/wenda/web/search/brow/?search_text=%E4%BE%9B%E6%B0%B4%E8%AE%BE%E5%A4%87&count=10']
    # zz = "https://www.wukong.com/wenda/web/search/loadmore/?search_text=供水设备&offset=10&count=10"
    headers = {"referer": "https://www.wukong.com/", "Host": "www.wukong.com",
               "user-agent": "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"}

    # keywords = ["阀门"]
    f_base_url = 'https://www.wukong.com/wenda/web/search/brow/?search_text={0}&count=10'
    s_base_url = 'https://www.wukong.com/wenda/web/search/question/brow/?search_text={0}&count=10'
    c_base_url = 'https://www.wukong.com/wenda/web/search/loadmore/?search_text={0}&offset={1}&count=10'
    question_base_url = "https://www.wukong.com/question/{0}/"
    # offset = 10
    # count = 0
    count = {}
    key_index = 0
    key_dict = {'喷泉设备': 1349, '化工泵': 1351, '显示器': 811, '不锈钢管': 1347, '开水器': 1340, '水表': 1353, '中水回用': 1352, '增压泵': 1351, '污水处理': 1352, 'PE管': 1347, '净水机': 1340, '阻垢剂': 1346, '纯化水': 1341, '镀锌管': 1347, '污泥泵': 1351, '泳池': 1349, '污泥处理': 1352, '台式机': 811, '电磁阀': 1350, 'BOD监测仪': 1353, '滤料': 1343, '刮泥机': 1352, '搅拌机': 1352, '水机': 1340, '仪器': 1353, '鼠标': 811, '无负压供水': 1339, '反渗透': 1341, '水箱': 1339, '锅炉': 1354, '加药设备': 1345, '自控系统': 1348, '水质监测仪': 1353, '蝶阀': 1350, '过滤阀': 1350, '不锈钢水箱': 1344, '滤网': 1343, '除氟': 1341, 'PE水箱': 1344, '活性炭': 1343, '杀菌剂': 1346, '消防泵': 1351, '滤芯': 1343, '电动阀': 1350, '膜组件': 1343, '无缝钢管': 1347, '空气净化器': 1345, '去离子水': 1341, '纯净水': 1341, 'COD监测仪': 1353, '气浮': 1352, '止回阀': 1350, '轴流泵': 1351, '脱水剂': 1346, '异型管': 1347, '紫外线消毒': 1345, '焊管': 1347, '管材': 1347, '循环水处理': 1349, '电脑': 811, '除氧器': 1341, '纳滤膜': 1343, '工业锅炉': 1354, '毛发聚集器': 1349, '水处理容器': 1344, '气压给水': 1339, '纯水机': 1340, '离心机': 1352, 'PVC管': 1347, '控制器': 1348, '闸阀': 1350, '多级泵': 1351, '安全阀': 1350, 'PPR管': 1347, '环保': 810, '软水机': 1340, '生活污水': 1352, '消泡剂': 1346, '水处理器': 1341, '过滤材料': 1343, '絮凝剂': 1346, '净水器': 1340, 'UPVC管': 1347, '碳钢罐': 1344, '银盘': 811, '变送器': 1348, '中央净水': 1340, '深井泵': 1351, '液位计': 1353, '滗水器': 1352, '油水分离器': 1352, '过滤器': 1341, '显卡': 811, 'PH值检测仪': 1353, '水处理药剂': 1346, '风淋室': 1345, '曝气器': 1352, '潜水泵': 1351, '控制柜': 1348, '控制阀': 1341, '除氧': 1345, '超滤': 1341, '废液': 810, '臭氧发生器': 1345, '节水': 810, '三通': 1347, '化工废水': 810, '鼓风机': 1352, '变频供水': 1339, '滤袋': 1343, '排污泵': 1351, '键盘': 811, '土壤': 810, '给水': 1339, '吸泥机': 1352, '水位控制阀': 1350, '压力表': 1353, '弯头': 1347, '消毒加药': 1345, '内存': 811, '二氧化氯': 1345, '缓蚀剂': 1346, '水塔': 1339, '生活给水': 1339, '除锰': 1341, '格栅设备': 1352, '热水锅炉': 1354, '仪表': 1353, '无塔供水': 1339, '饮水机': 1340, '玻璃钢罐': 1344, '给水泵': 1351, '传感器': 1348, '超纯水': 1341, '二次供水': 1339, '计量泵': 1351, '纯水': 1340, '恒压供水': 1339, '球阀': 1350, '交换树脂': 1343, '离心泵': 1351, '次氯酸钠发生器': 1345, '继电器': 1348, '消防给水': 1339, '法兰': 1347, '加氯器': 1345, '浊度仪': 1353, '超滤膜': 1343, '景观水处理': 1349, '高压泵': 1351, '蒸汽锅炉': 1354, '电渗析': 1341, '软化水': 1341, '池底吸污': 1349, '脱水机': 1352, '阀门配件': 1350, '高层供水': 1339, '变频器': 1348, '真空泵': 1351, '热水器': 1340, '除铁': 1341, '复合管': 1347, '接头': 1347, '反渗透膜': 1343, '清洗剂': 1346, '螺杆泵': 1351, '除砂器': 1352, '铜管': 1347, '净水': 1340, '管件': 1347, '截止阀': 1350, 'EDI装置': 1341, '矿泉水': 1341, '管道泵': 1351, '隔膜泵': 1351, '流量计': 1353, '主机': 811, '铝塑管': 1347, '记录仪': 1353, '泳池循环泵': 1349}
    # start_urls = ['https://www.wukong.com/wenda/web/nativefeed/brow/?concern_id=6215497900357585410&t=1524291996468']
    def __init__(self,name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.cookies_list = []
        # self.question_url = []
        with open("cookie_id","r",encoding="utf8") as f_r:
            for id in f_r:
                id = int(id.strip())
                if id not in self.cookies_list:
                    self.cookies_list.append(id)
        with open("question_url","r",encoding="utf8") as f_q:
            self.question_url = [line.strip() for line in f_q if line.strip()]

    def start_requests(self):
        with open("ci","r",encoding="utf8") as f:
            self.keywords =  [key.strip() for key in f]
            print(self.keywords)
        # for key in self.keywords:
        self.offset = 10
        key = self.keywords[self.key_index]
        print("--------------------------------",key)
        self.count[key] = 0
        f_url = self.f_base_url.format(key,)
        # s_url = self.s_base_url.format(key,)
        c_url = self.c_base_url.format(key,self.offset)
        headers = copy.deepcopy(self.headers)
        headers["referer"] = "https://www.wukong.com/search/?keyword={0}".format(key,)
        yield scrapy.Request(url = f_url ,meta={'download_timeout': 3, "key":key, "he":headers},headers=headers)
        # yield scrapy.Request(url = s_url ,meta={'download_timeout': 3, "key":key},headers=self.headers)
        yield scrapy.Request(url = c_url ,meta={'download_timeout': 3, "next": True, "key":key, "he":headers},headers=headers,cookies={"tt_webid":self.cookies_list[self.keywords.index(key)]})

    def parse(self, response):
        # print("================",response.request.headers.getlist("cookie"))
        # print("=======response=========",response.headers.getlist("set-cookie"))
        # print("================",response.request.cookies)
        data_dict = json.loads(response.text)
        # print("============",data_dict["data"]["has_more"])
        key = response.meta["key"]
        for question in data_dict["data"]["feed_question"]:
            self.count[key] += 1
            qid = question["question"]["qid"]
            question_url = self.question_base_url.format(qid,)
            print("+++++++++++++++",question_url,"*******",self.count[key])
            if question_url not in self.question_url:
                self.question_url.append(question_url)
                self.item_headers = copy.deepcopy(self.headers)
                self.item_headers["cookie"] = None
                yield scrapy.Request(url=question_url,meta={'download_timeout': 3, "next": True, "key":key},callback=self.get_item,headers=self.item_headers)
        if "next" in response.meta and response.meta["next"]:
            print("================", response.request.headers.getlist("cookie"))
            print("================", response.request.cookies)
            if data_dict["data"]["has_more"]:
                print("-------------进入offset下一层", response.url)
                self.offset += 10
                c_url = self.c_base_url.format(key,self.offset)
                print("采集网址为---------",c_url,response.request.cookies["tt_webid"])
                yield scrapy.Request(c_url,meta={'download_timeout': 3, "next": True, "key":key, "he":response.meta["he"]},headers=response.meta["he"],cookies={"tt_webid":response.request.cookies["tt_webid"]})
            else:
                with open("采集词数据统计","a",encoding="utf8") as f:
                    # f.write(key+":"+ str(self.count[key])+"最后采集url:"+response.url+"\n")
                    f.write("{0}:{1} ------->最后采集url:{2}\n".format(key,str(self.count[key]),response.url))

                print("hasmore 为0，结束采集", key, self.count[key])
                self.key_index += 1
                if self.key_index < len(self.keywords):
                    time.sleep(8)
                    self.offset = 10
                    key = self.keywords[self.key_index]
                    print("--------------------------------", key)
                    self.count[key] = 0
                    f_url = self.f_base_url.format(key, )
                    # s_url = self.s_base_url.format(key,)
                    c_url = self.c_base_url.format(key, self.offset)
                    headers = copy.deepcopy(self.headers)
                    headers["referer"] = "https://www.wukong.com/search/?keyword={0}".format(key, )
                    yield scrapy.Request(url=f_url, meta={'download_timeout': 3, "key": key, "he": headers},
                                         headers=headers)
                    # yield scrapy.Request(url = s_url ,meta={'download_timeout': 3, "key":key},headers=self.headers)
                    yield scrapy.Request(url=c_url,
                                         meta={'download_timeout': 3, "next": True, "key": key, "he": headers},
                                         headers=headers,
                                         cookies={"tt_webid": self.cookies_list[self.keywords.index(key)]})
                else:
                    with open("question_url", "w", encoding="utf8") as f_wq:
                        for question_url in self.question_url:
                            f_wq.write(question_url + "\n")




    def get_item(self,response):
        # print("item request cookie--------------------------",response.headers.getlist("set-cookie"))
        title = response.xpath('//h1/text()').extract_first()
        vote = response.xpath('//div[@class="question-text"]/text()').extract_first()
        answer_list = response.xpath('//div[@class="answer-text-full rich-text"]')
        key = response.meta["key"]
        # print("get_item key========================",key)
        if not title:
            print(response.url, "没有获取到数据！重新放到调度器")
            with open("111", "a", encoding="utf8") as f:
                f.write(response.url + "\n")
            req = response.request
            req.dont_filter = True
            yield req
        else:
            title = title.strip()
            yield ShuichuliItem(title=title, answer_list=answer_list,vote = vote,catid = self.key_dict[key],key=response.meta["key"])

    def get_headers(self,key):
        pass