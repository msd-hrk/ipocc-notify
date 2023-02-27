from ast import Raise
from unittest import expectedFailure
from pymongo import MongoClient
import datetime
from app_info import config

class DbUtils():
    def __init__(self):
        # 設定値取得
        conf = config.Config()
        # クライアント取得
        self.client = MongoClient(conf.mongo_url)
        self.db = self.client.ipocc2
        self.code_list = self.db.codelist2
        self.news = self.db.news
        now = datetime.date.today()
        self.today_yyyyMMdd = now.strftime("%Y%m%d")

    def get_listing(self):
        target = self.code_list.find(
            {
                "listingDate":int(self.today_yyyyMMdd),
            },
            {
                "_id": 0,
                "company": 1,
                "pubOfferPrice": 1,
                "securitiesNo": 1,
                "grade": 1,
            }
        )
        return target
    
    def get_bookbillding(self):
        target = self.code_list.find(
            {
                "bookbuilding.start":{'$lte': int(self.today_yyyyMMdd)},
                "bookbuilding.end":{'$gte': int(self.today_yyyyMMdd)},
            },
            {
                "_id": 0,
                "company": 1,
                "securitiesNo": 1,
                "expectedProfitAfterTD": 1,
                "grade": 1,
            }
        )
        return target

    def get_purchase(self):
        target = self.code_list.find(
            {
                "purchasePeriod.start":{'$lte': int(self.today_yyyyMMdd)},
                "purchasePeriod.end":{'$gte': int(self.today_yyyyMMdd)},
            },
            {
                "_id": 0,
                "company": 1,
                "securitiesNo": 1,
                "purchasePeriod": 1,
                "grade": 1,
                "pubOfferPrice": 1,
            }
        )
        return target

    def get_securities_no_list(self):
        target = self.code_list.find(
            {
                "securitiesNo": {"$exists": True}
            },
            {
                "_id": 0,
                "securitiesNo": 1,
            }
        )
        return target

    def is_colection_exist(self, securities_no: str):
        target = self.news.find_one(
            {
                "securitiesNo": str(securities_no)
            },
            {
                "_id": 0
            }
        )
        return target is not None

    def insert_new_data(self, data): 
        self.news.insert_one(data)

    def update(self, sec_no, data): 
        self.news.update_one(
            {
                "securitiesNo": sec_no
            },
            {
                '$set': data
            }
        )

    def get_full_data(self, securities_no: str):
        target = self.news.find_one(
            {
                "securitiesNo": str(securities_no)
            },
            {
                "_id": 0
            }
        )
        return target
