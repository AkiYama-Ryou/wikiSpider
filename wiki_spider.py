from bs4 import BeautifulSoup as bs
import requests
from setting import table_Wiki
import copy
#--------------------------------------------------------------------------------
# 宏定义
url_base = "https://zh.wikipedia.org/wiki/"
topic = "电子游戏"
data = {
    "class":"game",
    "topic":topic,
    "text":"",
    "links":{
        "wiki":[],
        "reference":[],
    },
    "keywords":[],
}
LINK = {
    "title":"",
    "href":"",
}
#--------------------------------------------------------------------------------
# 抓取
seq = requests.get(url_base + topic).content
#--------------------------------------------------------------------------------
# 解析
soup = bs(seq, "html.parser")
page = soup.find(class_="mw-parser-output").find_all("p")
for tag in page:
    print(tag.text)
    data["text"]+=tag.text
    for a in tag.find_all("a"):
        # --------------------------------------------------------------------------------
        # 提取链接
        link = copy.deepcopy(LINK)
        link["title"], link["href"] = a.text, a.attrs["href"]
        if link["href"].find("wiki")==1:
            data["links"]["wiki"].append(link)
            data["keywords"].append(a.text)
    for b in tag.find_all("b"):
        # --------------------------------------------------------------------------------
        # 提取加粗
        data["keywords"].append(b.text)
# --------------------------------------------------------------------------------
# 提取参考文献
references = soup.find(class_="reflist")
for tag in references.find_all("li"):
    try:
        tag = tag.find(class_="citation")
        link = copy.deepcopy(LINK)
        link["title"] = tag.text
        link["href"] = tag.find("a").attrs["href"]
        data["links"]["reference"].append(link)
        print(link)
    except AttributeError as e:
        pass
#--------------------------------------------------------------------------------
# 入库
table_Wiki.insert_one(data)