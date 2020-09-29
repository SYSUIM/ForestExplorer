#-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import os
import time


def get_id(url, topic, idPath):
    page_count = 1
    id_list=[]
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9"}
    #循环获取所有相关文章id
    while(True):
        if(page_count>1):
            url2 = url +"/page/"+ str(page_count)
            page = requests.get(url2,headers=send_headers)
        else:    
            page = requests.get(url,headers=send_headers)
        #获取成功
        if(page.status_code == 200):
            soup = BeautifulSoup(page.text,'html.parser')
            post_list =  soup.find_all('article',attrs={'itemtype':'http://schema.org/BlogPosting'})
            if(post_list == []):
                print("FINISHED GETTING ID ......" )
                break
            for item in post_list:
                lis=re.findall(r'post-(\d+)',str(item))
                if lis != []:
                    id_list.append(lis[0])
            #获取下一个页面  
            page_count+=1
            if(page_count%3==0):
                time.sleep(5)   
        #获取失败
        else:
            break
    print("获取文章ID",str(len(id_list)),"个！")

    #写入文件
    with open(idPath+topic+'_id.txt',"w",encoding="utf-8") as f:
        for item in id_list:
            f.write(item+'\n')


def get_articles(topic,idPath,filePath):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9"}
    with open(idPath+topic+'_id.txt','r',encoding='utf-8') as f:
        id = f.readline().replace("\n","")
        #读入内容不为空
        while id:
            url = "http://www.199it.com/archives/"+id+".html"
            page = requests.get(url,headers=send_headers)
            #获取成功
            if(page.status_code == 200):
                soup = BeautifulSoup(page.text,'html.parser')
                articleTitle=soup.find('h1',attrs={'itemprop':'headline mainEntityOfPage'}).get_text()
                delContent=soup.find('div',attrs={'class':'wp_rp_content'}).get_text()
                articleContent=soup.find('div',attrs={'class':'entry-content articlebody'}).get_text().replace(delContent,"")
                articleTime=soup.find('time',attrs={'itemprop':'datePublished'}).get_text()
                with open(filePath+str(id)+'.txt',"w",encoding="utf-8") as f2:       
                        f2.write(articleTitle+'\n')
                        f2.write(articleTime+'\n')
                        f2.write(articleContent)
            #获取失败
            else:
                print("Fail to get article  "+str(id))
            #读取下一个id,继续循环
            id = f.readline().replace("\n","") 


if __name__ == "__main__": 
    url='http://www.199it.com/archives/category/emerging/'
    idPath='C:/Users/hzs/Desktop/数据创新大赛/199/id/'
    filePath='C:/Users/hzs/Desktop/数据创新大赛/199/199_file/'
    keys=['5g','xinjijian',"smartcar","health-tech","新能源","heemi","物联网","nmi","nev","工业4-0","人工智能",'机器学习','knowledge-domains']
    for key in keys:
        get_id(url+key,key,idPath)
    for key in keys:
        get_articles(key,idPath,filePath)
        print('FINISHEDE WRITTING TOPIC ',key)




