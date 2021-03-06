# coding=utf-8
import requests
from lxml import etree
from requests.exceptions import ConnectionError
from urllib import request
from bs4 import BeautifulSoup
import time


"""
爬虫api：
    搜索结果页：get_index_result(search)
    小说章节页：get_chapter(url)
    章节内容：get_article(url)
"""
class DdSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/535.36(KHTML,like Gecko)Chrome/65.0.3325.162 Safari/537.36'
        }

    def parse_url(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                # 处理一下网站打印出来中文乱码的问题
                resp.encoding = 'utf-8'
                return resp.text
            return None
        except ConnectionError:
            print('Error：连接错误')
        return None

    # 搜索结果页数据
    def get_index_result(self, search):
       
        url = 'https://www.23us.cc/SearchBook.php?t=920895234054625192&keyword={search}'.format(search=search)
        print(url)
        
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        titles = html.xpath('//*[@class="details list-type"]/ul/li/span[2]/a/text()')
        urls = html.xpath('//*[@class="details list-type"]/ul/li/span[2]/a/@href')
        authors = html.xpath('//*[@class="details list-type"]/ul/li/span[3]/text()')
        upadtetime = html.xpath('//*[@class="details list-type"]/ul/li/span[4]/text()')
        styles = html.xpath('//*[@class="details list-type"]/ul/li/span[1]/text()')
        state = html.xpath('//*[@class="details list-type"]/ul/li/span[5]/text()')
        #times = html.xpath('//*[@id="results"]/div/div/div/div/p[3]/span[2]/text()')
        for title, url, author, upadtetime, style, state in zip(titles, urls, authors, upadtetime, styles,
                                                                  state):
            data = {
                'title': title.strip(),
                'url': url,
                'author': author.strip(),
                'upadtetime': upadtetime.strip(),
                'style': style.strip(),
                'state': state.strip()
            }
            yield data

    # 小说章节页数据
    def get_chapter(self, url):
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        chapters = html.xpath('//*[@id="main"]/div/dl/dd/a/text()')
        urls = html.xpath('//*[@id="main"]/div/dl/dd/a/@href')
        for chapter_url, chapter in zip(urls, chapters):
            data = {
                'url': str(url) + chapter_url,
                'chapter': chapter
            }
            yield data
            
    # 章节内容页数据
    def get_article(self, url):
        head = {}
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        download_req = request.Request(url, headers = head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read()
        download_soup = BeautifulSoup(download_html, 'lxml')
        download_soup_texts = download_soup.find('div', id = 'content')
        download_soup_texts = download_soup_texts.text
        content = html.xpath('//*[@id="content"]/text()')
        return download_soup_texts
