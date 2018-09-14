# import re,time
#
# # text = '中国<img src="////">你好><img src="////"> <script src="js.js">iiii'
# #
# # rrr = re.compile(r"(<img.*?>)|(<script.*?>)|(<a.*?</a>)|(<frame.*?>)")
# # new = rrr.sub("",text)
# # # new = rrr.findall(text)
# # print(new)
#
# # print(int(time.time()))
#
# with open("999","r",encoding="utf8") as f:
#     dic = dict()
#     for line in f:
#         line = line.strip()
#         if line:
#
#             key,index = line.split(",")
#             print(key,index)
#             dic[key] = int(index)
#             # print(dic)
#
#     print(dic)


sss = "中国"
print(sss.encode("gbk").decode("gbk"))