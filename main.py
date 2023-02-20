from dbutils import dbCommon
from mail import mail
from app_info import config
db = dbCommon.DbUtils()
text = ""

# 本日上場企業
text = text + "【本日上場】\n"
for ldt in db.get_listing():
    company = "●" + ldt["company"] + "（" + ldt["securitiesNo"] + "）"
    grade = "　評価　　：" + ldt["grade"]
    pub_price = "　公募価格：" + str(ldt["pubOfferPrice"])
    text = text + '\n'.join([company, grade, pub_price, "\n"])

# ブックビルディング中
text = text + "【ブックビルディング中】\n"
for bdt in db.get_bookbillding():
    company = "●" + bdt["company"] + "（" + bdt["securitiesNo"] + "）"
    grade = "　評価　　：" + bdt["grade"]
    td_price = "　仮条件　：" + str(bdt["expectedProfitAfterTD"]["tdPrice"]["min"]) + "　〜　" + bdt["expectedProfitAfterTD"]["tdPrice"]["max"]
    ex_profit = "　予想利益：" + str(bdt["expectedProfitAfterTD"]["exProfit"]["min"]) + "　〜　" + bdt["expectedProfitAfterTD"]["exProfit"]["max"]
    text = text + '\n'.join([company, grade, td_price, ex_profit, "\n"])

# 購入期間
text = text + "【購入期間】\n"
for pdt in db.get_purchase():
    company = "●" + pdt["company"] + "（" + pdt["securitiesNo"] + "）"
    grade = "　評価　　：" + pdt["grade"]
    pub_price = "　公募価格：" + str(pdt["pubOfferPrice"])
    text = text + '\n'.join([company, grade, pub_price, "\n"])

# メール送信
conf = config.Config()
sender = mail.Mail(conf.srcaddr, conf.password)
subject = "ipocc_notify"
for desaddr in conf.desaddr_arry:
    sender.send(desaddr, subject, text)
