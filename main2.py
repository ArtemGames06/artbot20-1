from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://artbot:aFMm37mkxn8kZcd4@cluster0.yusxf.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = ["testdb"]