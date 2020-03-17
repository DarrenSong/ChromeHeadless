from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup, Comment
import collections


class WebHelp:

    __path = ''
    __url = ''
    driver = ''

    def __init__(self, path, url):
        self.__path = path
        self.__url = url

    def configWeb(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        self.driver = webdriver.Chrome(executable_path=self.__path, chrome_options=chrome_options)
        self.driver.set_page_load_timeout(100)
        self.driver.set_script_timeout(100)

    def getPage(self):
        self.driver.get(self.__url)
        # 模拟滚动
        for i in range(1, 11):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight/10*%s);" % i
            )
            time.sleep(2)
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # 删除注释
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        return soup

    def getIndex(self, soup):
        xml = soup.find_all('span', class_='caa inlb')
        indexNum = []
        for i in range(len(xml)):
            msg = xml[i].string.strip().replace(" ", "")
            if msg.isdigit():
                indexNum.append(msg)
        return indexNum

    def split_list(self, l, n, new=[]):
        '''
        将一个LIST拆分成一个子LIST元素个数为n的二维数组,
        :param l:  原LIST
        :param n:  每个子LIST的个数
        :param new: 新的LIST, 不需要传
        :return: [[1..], [2..], [3..]]
        '''
        if len(l) <= n:
            new.append(l)
            return new
        else:
            new.append(l[:n])
            return self.split_list(l[n:], n)

    def getNum(self, soup):
        xml = soup.find_all('span', class_='caba')
        indexNum = []
        for i in range(len(xml)):
            msg = xml[i].string.strip().replace(" ", "")
            if msg.isdigit():
                indexNum.append(msg)
        finlist = self.split_list(indexNum, 5)
        return finlist

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    # chrome driver路径
    path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
    # 抓取的网页url
    url = "https://ds.dsproxy.net/ds_jxf01/#/game/1-3-5"

    while True:
        tm_start = time.time()
        wh = WebHelp(path, url)
        wh.configWeb()  # 配置driver
        soup = wh.getPage()  # 请求数据
        inlist = wh.getIndex(soup)  # 从请求的数据里解析期号
        nulist = wh.getNum(soup)  # 从请求的数据里解析中奖号码
        d = collections.OrderedDict()
        for i in range(len(inlist)):
            d[inlist[i]] = nulist[i]
        print(inlist)
        print(nulist)
        print(d)
        tm_end = time.time()
        tm_c = tm_end - tm_start
        print('time cost', tm_c, 's')
        time.sleep(30)
