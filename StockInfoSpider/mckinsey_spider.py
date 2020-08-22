import requests
import time
from bs4 import BeautifulSoup
from requests.packages import urllib3

def get_article(topic,path):
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
        page=requests.get(page_url,headers=send_headers,verify = False)       
        if(page.status_code==200):
            print("Getting URL ", page_url," ......")
            soup = BeautifulSoup(page.text,'html.parser')
            articles_list=soup.find_all('article')
            for article in articles_list:
                article_url=article.h2.a['href']
                article_page=requests.get(article_url,headers=send_headers,verify = False)
                if(article_page.status_code==200):
                    soup2 = BeautifulSoup(article_page.text,'html.parser')
                    if soup2.find('article') == None:
                        continue
                    articleId=soup2.find('article')['id']
                    articleTitle=soup2.find('h2',attrs={'class':'fusion-post-title'}).get_text()
                    articleContent=soup2.find('div',attrs={'class':'post-content'}).get_text()
                    articleTime=soup2.find('div',attrs={'class':'fusion-meta-info-wrapper'}).find_all('span')[2].get_text() 
                    print("WRITING FILE ",articleId," ......")
                    with open(path+str(articleId)+'.txt','w',encoding='utf-8') as f:
                        f.write(articleTitle+'\n')
                        f.write(articleTime+'\n')
                        f.write(articleContent)
            page_count+=1
            if(page_count%3==0):
                print("SLEEP FOR 5 SECONDS ......")
                time.sleep(5)
        else:
            print(page_url, "404")
            break

if __name__=='__main__':
    urllib3.disable_warnings()
    path='C:/Users/hzs/Desktop/数据创新大赛/mckinsey/mckinsey_file/'
    #'宏观经济','创新','高新科技','科技+企业','创新+科技','企业+创新','高科技','互联网','物联网','数字化','大数据','5g','人工智能'
    keys=['人工智能']
    for key in keys:
        get_article(key,path)





    
    
    



        
