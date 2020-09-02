import re
import requests
from bs4 import BeautifulSoup
titles=[]
urls=[]
keyword=input("输入想要在维科网搜索的关键字：")
pagenum=input("输入想要查找的前几页（如果输入2，即找前2页的）：")
txt_name="关键词："+keyword+"前"+pagenum+"页具体内容.txt"
with open(txt_name,'w',encoding='utf-8') as f:
    f.write(txt_name+'\r')
    f.close()
for i in range(1,int(pagenum)+1):
    html="http://www.ofweek.com/newquery.action?keywords="+keyword+"&type=1&pagenum="+str(i)#科技新闻
    resp=requests.get(html)
    resp.encoding='GBK'
    content=resp.text
    bs=BeautifulSoup(content,'html.parser')
    for news in bs.select('div.zx-tl'):#每个标题都是存在类名为no-pic的li标签里面
        url=news.select('a')[0]['href']
        urls.append(url)
        title=news.select('a')[0].text
        titles.append(title)
    for i in range(len(urls)):
        resp=requests.get(urls[i])
        resp.encoding='GBK'
        content=resp.text
        bs=BeautifulSoup(content,'html.parser')
        page_content=bs.select('div.artical-content')[0].text
        with open(txt_name,'a',encoding='utf-8') as f:
            f.write("\n"+titles[i]+page_content)
            f.close()
print("txt文件已经成功记录！")