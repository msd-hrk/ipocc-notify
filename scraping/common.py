import requests
from bs4 import BeautifulSoup

class Common():
    def __init__(self) -> None:
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        pass
    
    def get_page(self, url: str) -> BeautifulSoup:
        html = requests.get(url, headers={"User-Agent": self.user_agent})
        return BeautifulSoup(html.content, 'html.parser')
