from dbutils import dbCommon
from mail import mail
from app_info import config
db = dbCommon.DbUtils()
text = "取得先は<a href=\"https://ipokabu.net/yotei/\">こちら</a><br><br>"

# 本日上場企業
text = text + "【本日上場】<br>"
for ldt in db.get_listing():
    company = ""
    grade = ""
    pub_price = ""
    try:
        company = "▲" + ldt["company"] + "（" + ldt["securitiesNo"] + "）"
        grade = "　評価　　：" + ldt["grade"]
        pub_price = "　公募価格：" + str(ldt["pubOfferPrice"])
    except:
        continue
    text = text + '<br>'.join([company, grade, pub_price, "<br>"])

# ブックビルディング中
text = text + "【ブックビルディング中】<br>"
for bdt in db.get_bookbillding():
    company = ""
    period = ""
    grade = ""
    td_price = ""
    ex_profit = ""

    st_mon = str(bdt["bookbuilding"]["start"])[4:6]
    st_day = str(bdt["bookbuilding"]["start"])[6:]
    ed_mon = str(bdt["bookbuilding"]["end"])[4:6]
    ed_day = str(bdt["bookbuilding"]["end"])[6:]
    try:
        company = "●" + bdt["company"] + "（" + bdt["securitiesNo"] + "）"
        period = "　期間　　：" + st_mon + "/" + st_day + "　〜　" + ed_mon + "/" + ed_day
        grade = "　評価　　：" + bdt["grade"]
        td_price = "　仮条件　：No data"
        ex_profit = "　予想利益：No data"
        if "expectedProfitAfterTD" in bdt:
            td_price = "　仮条件　：" + str(bdt["expectedProfitAfterTD"]["tdPrice"]["min"]) + "　〜　" + str(bdt["expectedProfitAfterTD"]["tdPrice"]["max"])
            ex_profit = "　予想利益：" + str(bdt["expectedProfitAfterTD"]["exProfit"]["min"]) + "　〜　" + str(bdt["expectedProfitAfterTD"]["exProfit"]["max"])
    except:
        continue
    text = text + '<br>'.join([company, period, grade, td_price, ex_profit, "<br>"])

# 購入期間
text = text + "【購入期間】<br>"
for pdt in db.get_purchase():
    company = ""
    period = ""
    grade = ""
    pub_price = ""

    st_mon = str(pdt["purchasePeriod"]["start"])[4:6]
    st_day = str(pdt["purchasePeriod"]["start"])[6:]
    ed_mon = str(pdt["purchasePeriod"]["end"])[4:6]
    ed_day = str(pdt["purchasePeriod"]["end"])[6:]
    try:
        company = "■" + pdt["company"] + "（" + pdt["securitiesNo"] + "）"
        period = "　期間　　：" + st_mon + "/" + st_day + "　〜　" + ed_mon + "/" + ed_day
        grade = "　評価　　：" + pdt["grade"]
        pub_price = "　公募価格：" + str(pdt["pubOfferPrice"])
    except:
        continue
    text = text + '<br>'.join([company, period, grade, pub_price, "<br>"])

# メール送信
conf = config.Config()
sender = mail.Mail(conf.srcaddr, conf.password)
subject = "ipocc_notify"
for desaddr in conf.desaddr_arry:
    sender.send(desaddr, subject, text)
