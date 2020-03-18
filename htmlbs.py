from bs4 import BeautifulSoup, Comment
import collections


class HtmlBs:

    def __init__(self):
        return

    def getSoup(self, shtml):
        soup = BeautifulSoup(shtml, 'html.parser')
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

    def getNum(self, soup):
        xml = soup.find_all('span', class_='caba')
        indexNum = []
        for i in range(len(xml)):
            msg = xml[i].string.strip().replace(" ", "")
            if msg.isdigit():
                indexNum.append(msg)
        # print(indexNum)
        finlist = self.splitlist(indexNum, 5)
        return finlist

    def splitlist(self, word, sublen):
        subLucky = [word[i:i+sublen] for i in range(0, len(word), sublen)]
        return subLucky

    # 多次调用会出现问题，pass
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

    def del_com(self, soup):
        # 删除注释
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
