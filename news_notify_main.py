from time import sleep
import os
import pathlib
from scraping import news_page, ctrl_str
from dbutils import dbCommon
from app_info import config
from mail import mail

class NewsNotifyMain():
    def __init__(self) -> None:
        self.db = dbCommon.DbUtils()
        self.error_file_path = "error_file"
        pass
    
    def main(self):
        try:
            self.mail_send = False
            mail_text = ""
            # get target security number
            self.db = dbCommon.DbUtils()
            data = self.db.get_securities_no_list()
            target_list = []
            for sec_no in data:
                target_list.append(sec_no["securitiesNo"])
            with open("app_info/target.list") as f:
                for test in f.readlines():
                    target_list.append(ctrl_str.CtrlStr().remove(test, "\r\n", "\n"))
            # for each security number, run code
            for sec_no in target_list:
                sleep(1)
                # get today news
                np = news_page.NewsPage(sec_no)
                topics = np.get_topics()
                company = np.get_company()
                if len(topics) == 0:
                    continue
                if not self.db.is_colection_exist(sec_no):
                    self.db.insert_new_data(
                        {
                            "securitiesNo": sec_no,
                            "company": company,
                            "topics": topics
                        }
                    )
                    mail_text = self.crt_mail_text(sec_no, company, topics, mail_text)
                    self.mail_send = True
                    continue
                add_topics = self.add_new_topics(topics, sec_no)
                if len(add_topics) > 0:
                    mail_text = self.crt_mail_text(sec_no, company, add_topics, mail_text)
                    self.mail_send = True
            if self.mail_send:
                conf = config.Config()
                sender = mail.Mail(conf.srcaddr, conf.password)
                subject = "ipocc_topics"
                for desaddr in conf.desaddr_arry:
                    sender.send(desaddr, subject, mail_text)
            if os.path.exists(self.error_file_path):
                os.remove(self.error_file_path)
                
        except:
            if not os.path.exists(self.error_file_path):
                conf = config.Config()
                sender = mail.Mail(conf.srcaddr, conf.password)
                subject = "ipocc_topics"
                for desaddr in conf.desaddr_arry:
                    sender.send(desaddr, subject, "例外が発生したため、メール配信を停止します")
                err_file = pathlib.Path(self.error_file_path)
                err_file.touch()

    def add_new_topics(self, new_info, sec_no):
        already_info = self.db.get_full_data(sec_no)
        add_target = []
        for new in new_info:
            add_flg = True
            for already in already_info["topics"]:
                if new["title"] == already["title"] \
                    and new["date"] == already["date"] \
                    and new["link"] == already["link"]:
                    add_flg = False
                    break
            if add_flg:
                add_target.append(new)
        
        for add_topic in add_target:
            already_info["topics"].append(add_topic)
        if len(add_target) > 0:
            self.db.update(sec_no, already_info)
        return add_target

    def crt_mail_text(self, sec_no, company, topics, mail_text):
        mail_text = mail_text + "【" + company + "（" + sec_no + "）"+"】<br>"
        for topic in topics:
            link = "●<a href=\""+ topic["link"] + "\">" + topic["title"] + "</a>"
            mail_text = mail_text + '\n'.join([link, "<br>"])
        return mail_text

if __name__ == "__main__":
    NewsNotifyMain().main()