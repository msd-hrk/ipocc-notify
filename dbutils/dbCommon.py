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
        now = datetime.date.today()
        self.today_yyyyMMdd = now.strftime("%Y%m%d")

    def search_code_list(self, code_no):
        return self.code_list.find_one({'securitiesNo': code_no})

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
