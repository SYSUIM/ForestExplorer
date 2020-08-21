##-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import os
import time


def get_id(url, topic):
    page_count = 1
    id_list=[]
    fail_time=0
    total_fail_time=0
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
            post_list =  soup.body.find('div',attrs={'id':'page'}).find('div',attrs={'id':'main'}).div.div.div.div.div.find_all('article')
            if(post_list == []):
                print("End！")
                break
            for item in post_list:
                lis=re.findall(r'post-(\d+)',str(item))
                if lis != []:
                    id_list.append(lis[0])
            #获取下一个页面  
            page_count+=1   
        #获取失败
        else:
            time.sleep(5)
            fail_time+=1
            #同一页失败两次，获取下一页 
            if fail_time==2:
                print("Fail to get page!",str(url2))
                page_count+=1
                total_fail_time+=1
                fail_time=0
            #总总共失败三次
            if total_fail_time==3:
                break

    print("获取文章ID",str(len(id_list)),"个！")

    #写入文件
    with open('199/id/'+topic+'_id.txt',"w",encoding="utf-8") as f:
        for item in id_list:
            f.write(item)
            f.write("\n")


def get_articles(topic):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    }
    with open('199/id/'+topic+'_id.txt','r',encoding='utf-8') as f:
        id = f.readline().replace("\n","")
        #读入内容不为空
        while id:
            url = "http://www.199it.com/archives/"+id+".html"
            page = requests.get(url,headers=send_headers)
            #获取成功
            if(page.status_code == 200):
                soup = BeautifulSoup(page.text,'html.parser')
                text = soup.body.find('div',attrs={'id':'page'}).find('div',attrs={'id':'main'}).div.div.div.div.div.article
                #需要删除的标签以及内容
                del_div = text.find('div',attrs={'id':'wp_rp_first'}) 
                del_p = text.find('p',attrs={'style':'text-align: center;'})
                if text.find_all('script') != []:
                    del_script1 = text.find_all('script')[0]
                    del_script2 = text.find_all('script')[1]
                    text = str(text).replace(str(del_script1),'')
                    text = text.replace(str(del_script2),'')
                text = str(text).replace(str(del_div),'')  
                text = text.replace(str(del_p),'')                                                                     
                #去除标签
                reg = re.compile('<[^>]*>')      
                text = reg.sub('',text)
                text = text.replace('(adsbygoogle = window.adsbygoogle || []).push({});','').replace('\n','').replace('\r','')
                with open('199/199_file/'+str(id)+'.txt',"w",encoding="utf-8") as f2:       
                        f2.write(text)
                        #print("Succeed in writing file "+ str(id))
            #获取失败
            else:
                print("Fail to get article  "+str(id))
            #读取下一个id,继续循环
            id = f.readline().replace("\n","") 


if __name__ == "__main__": 

    '''
    get_id("http://www.199it.com/archives/category/emerging/5g","5g")
    get_articles("5g")
    get_id("http://www.199it.com/archives/category/emerging/xinjijian","xinjijian")
    get_articles("xinjijian")
    get_id("http://www.199it.com/archives/category/emerging/smartcar","smartcar")
    get_articles("smartcar")
    get_id("http://www.199it.com/archives/category/emerging/health-tech","health-tech")
    get_articles("health-tech")
    get_id("http://www.199it.com/archives/category/emerging/新能源","新能源")
    get_articles("新能源")
    get_id("http://www.199it.com/archives/category/emerging/heemi","heemi")
    get_articles("heemi")
    get_id("http://www.199it.com/archives/category/emerging/物联网","物联网")
    get_articles("物联网")
    get_id("http://www.199it.com/archives/category/emerging/nmi","nmi")
    get_articles("nmi")
    get_id("http://www.199it.com/archives/category/emerging/nev","nev")
    get_articles("nev")
    get_id("http://www.199it.com/archives/category/emerging/工业4-0","工业4-0")
    get_articles("工业4-0")
    get_id("http://www.199it.com/archives/category/emerging/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD","人工智能")
    get_articles("人工智能")
    get_id('http://www.199it.com/archives/category/emerging/%e4%ba%ba%e5%b7%a5%e6%99%ba%e8%83%bd/%e6%9c%ba%e5%99%a8%e5%ad%a6%e4%b9%a0','机器学习')
    get_articles('机器学习')
    get_id('http://www.199it.com/archives/category/emerging/%e4%ba%ba%e5%b7%a5%e6%99%ba%e8%83%bd/knowledge-domains','knowledge-domains')
    get_articles('knowledge-domains')
    '''
