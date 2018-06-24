import spyder
import requests
from lxml import etree
from requests.exceptions import ConnectionError
from urllib import request
from bs4 import BeautifulSoup
import time


dd = spyder.DdSpider()

temp1 = input("请输入您想阅读的小说：")

a = str(temp1)



for j in dd.get_index_result(a):
    print("书名：",j['title'],"作者：",j['author'],"风格：",j['style'])



while 1:
    temp3 = input('请输入您想阅读的小说名：')
    c = str(temp3)
    m = {}
    for j in dd.get_index_result(a):
        if j['title'] == c:
            m = (j['url'])
            title = j['title']
        else:
        	continue
    if m :
    	print(m)
    	break
    else:
        print("没有找到您想看的书，请重新输入：")
        continue
extra = "https://www.23us.cc"
b = extra + str(m)

url = b
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/535.36(KHTML,like Gecko)Chrome/65.0.3325.162 Safari/537.36'
req = request.Request(url, headers = head)
response = request.urlopen(req)
html = response.read()
soup = BeautifulSoup(html, 'lxml')
soup_texts = soup.find('div', class_= 'inner').find_all('dd')
# 打开文件
   
# 循环解析链接地址
   
for link in soup_texts:
    if link != '\n':
        download_url = link.a.get('href')
        url = b + download_url
        a = dd.get_article(url)
        time.sleep(1)
        with open(title + '.txt', 'a', encoding='gbk', errors='ignore') as f:
            f.write(link.text + '\n\n')
            f.write(a)
            f.write('\n\n')
        print(link.text + '下载完成')

print('已全部下载完')
