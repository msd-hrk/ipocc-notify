from bs4 import BeautifulSoup
import datetime
from scraping import common, ctrl_str

class NewsPage():
    
    def __init__(self, securities_no) -> None:
        self.common = common.Common()
        self.ctrl_str = ctrl_str.CtrlStr()
        self.sec_no = securities_no
        self.base_url = "https://kabuyoho.ifis.co.jp/index.php?action=tp1&sa=report_zim&bcode=" + self.sec_no
        self.page = self.common.get_page(self.base_url)
        self.today = datetime.date.today().strftime("%Y/%m/%d")
        
    def get_new_info_count(self) -> int:
        elem_trs = self.page.select(".tb_new_news tr")
        counter = 0
        for elem_tr in elem_trs:
            elem_date = elem_tr.select(".date")
            if len(elem_date) == 0:
                break
            if elem_date[0].get_text() == self.today:
                counter = counter + 1
        return counter
    
    def get_topics(self):
        elem_trs = self.page.select(".tb_new_news tr")
        today_topics = []
        for elem_tr in elem_trs:
            elem_date = elem_tr.select(".date_new")
            if len(elem_date) == 0:
                break
            if not elem_date[0].get_text() == self.today:
                break
            title = self.ctrl_str.remove(elem_tr.select("a")[0].get_text(), "\r\n", "\t")
            link = "https://kabuyoho.ifis.co.jp/" + elem_tr.select("a")[0].get('href')
            today_topics.append(
                {
                    "date": self.today,
                    "title": title,
                    "link": link
                }
            )
        return today_topics

    def get_company(self):
        return self.page.select("#report .stock_name")[0].getText()