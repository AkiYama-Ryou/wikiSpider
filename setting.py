import pymongo
#--------------------------------------------------------------------------------
# 初始化数据库链接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["test"]
table_Wiki = db["wiki"]
