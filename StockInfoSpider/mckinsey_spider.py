import requests
import re
import time
import os
from bs4 import BeautifulSoup
from requests.packages import urllib3

def get_article(topic):
    page_count=1
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9"}

    while(True):
        if(page_count==1):
            page_url='https://www.mckinsey.com.cn/?s='+topic
        else:
            page_url='https://www.mckinsey.com.cn/page/'+str(page_count)+'/?s='+topic
        #关闭警告信息
        urllib3.disable_warnings()
        page=requests.get(page_url,headers=send_headers,verify = False)       
        if(page.status_code==200):
            soup = BeautifulSoup(page.text,'html.parser')
            articles_list=soup.body.find('div',attrs={'id':'wrapper'}).main.div.section.find('div',attrs={'id':'posts-container'}).div.find_all('article')
            for article in articles_list:
                #文章链接
                article_url=re.findall(r'href="(.+)"',str(article.find('h2')))[0]
                #文章标题
                article_title = str(article.find('h2').a.text).replace('|','').replace('"','').replace('/','').replace('?','')
                #print(article_title)
                article_page=requests.get(article_url,headers=send_headers,verify = False)
                if(article_page.status_code==200):
                    soup2 = BeautifulSoup(article_page.text,'html.parser')
                    section=soup2.body.find('div',attrs={'id':'wrapper'}).main.div.section
                    #如果存在article标签
                    if(section.article):
                        article_text=section.article.find('div',attrs={'class':'post-content'})
                    #不存在article标签
                    else:
                        article_text=section.div.div.div.div.div.div.div
                    #去除标签
                    reg = re.compile('<[^>]*>')      
                    text = reg.sub('',str(article_text))    
                    with open('mckinsey/mckinsey_file/'+article_title+'.txt','w',encoding='utf-8') as f:
                        f.write(text.replace('\n','').replace('\r',''))
            page_count+=1
        elif(page.status_code==404):
            print(page_url, "404")
            break
        else:
            time.sleep(5)

if __name__=='__main__':
    lis=[]
    for word in lis:
        get_article(word)
    #'宏观经济','创新','高新科技','科技+企业','创新+科技','企业+创新','高科技','互联网','物联网','数字化','大数据','5g','人工智能'

    
    
    



        
