import requests
import re
import time
import json
from bs4 import BeautifulSoup
from requests.packages import urllib3


def getArticleList(url,fromData,headers):
    #data需要json格式
    articleLinkRes = requests.post(url, data = json.dumps(fromData), headers=headers)
    articleLinkResJson = json.loads(articleLinkRes.text)
    articleLinkList = []
    for articleData in articleLinkResJson['data']['itemList']:
        articleLinkList.append(articleData['itemId'])
    #返回id列表，更新下一次post的pageCallback，是否还有下一页
    print("FINISHED GETTING LIST ......")
    return articleLinkList,articleLinkResJson['data']['pageCallback'],articleLinkResJson['data']['hasNextPage']

def getAritclePage(url):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9"}
    page=requests.get(url,headers=send_headers,verify=False)
    page.encoding = 'utf-8'
    if(page.status_code==200):
        return page.text
    else:
        print("Fail to get ",url)

def articleParser(page):
    soup = BeautifulSoup(page, 'html.parser')
    articleTitle = soup.find('h1',attrs={"class":"article-title margin-bottom-20 common-width"}).get_text()
    articleTime = soup.find('span',attrs={"class":"title-icon-item item-time"}).get_text().replace("·","")
    #article-title margin-bottom-20 common-width
    #article-title margin-bottom-20 common-width
    articleText = soup.find('div',attrs={"class":"common-width content articleDetailContent kr-rich-text-wrapper"}).get_text()
    articleInfo = {'title': articleTitle,'time': articleTime, 'content': articleText}
    return articleInfo

def writeToDisk(path, articleInfo):
    print("WRITING FILE ", path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(articleInfo['title']) + '\n' +str(articleInfo['time']) + '\n' + str(articleInfo['content']) + '\n')
        f.close()
        

if __name__ == "__main__":
    urllib3.disable_warnings()
    postURL='https://gateway.36kr.com/api/mis/nav/search/resultbytype'
    articleURL='https://36kr.com/p/'
    path='C:/Users/hzs/Desktop/数据创新大赛/36kr/36kr_file/'
    keyWords=['宏观经济']
    dic={
        '创新企业':'eyJmaXJzdElkIjo4NDU4MDQzNDQ1Nzk1ODgsImxhc3RJZCI6ODM3NjY0MTQ0ODIwMjMwLCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgwMDczMTExNjMsImxhc3RDcmVhdGVUaW1lIjoxNTk3NDEzNjcyNTMwfQ',
        '高新企业':'eyJmaXJzdElkIjo4NDU3MzY1NjU2NTkxNDIsImxhc3RJZCI6NzU3MjIwNTMzNDYzMDQ0LCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgwNTYzOTIwNDgsImxhc3RDcmVhdGVUaW1lIjoxNTkyNDkwMjYzMzk0fQ',
        '高新技术':'eyJmaXJzdElkIjo4NDkxODkyMjUxNTgxNDQsImxhc3RJZCI6ODQzMzgyNjIzNDczNjY3LCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgxMDI0NDA4MzcsImxhc3RDcmVhdGVUaW1lIjoxNTk3NzQ4MzUwMDM3fQ',
        '宏观经济':'eyJmaXJzdElkIjo4NDc2MjU3NzM2NTk3ODMsImxhc3RJZCI6ODI3NTkyMTkzMDU2ODk4LCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgwMDc0MTg4MTYsImxhc3RDcmVhdGVUaW1lIjoxNTk2Nzg0MzI1NTcxfQ',
        '互联网':'eyJmaXJzdElkIjo4NDc3OTM5NTcwNTgxNzgsImxhc3RJZCI6ODQ3NjAxNDM3MzAwMjMwLCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgwODM2ODQwMDAsImxhc3RDcmVhdGVUaW1lIjoxNTk4MDA3MDgxMDU0fQ',
        '大数据':'eyJmaXJzdElkIjo4NDc3OTM5NTcwNTgxNzgsImxhc3RJZCI6ODQ3MzYzMjExNjYzMTA4LCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgwODM2ODQwMDAsImxhc3RDcmVhdGVUaW1lIjoxNTk3OTkyNzAwMDUzfQ',
        '科技':'eyJmaXJzdElkIjo4NDkxODkyMjUxNTgxNDQsImxhc3RJZCI6ODQ3MTY4MzE1NTc3ODYyLCJmaXJzdENyZWF0ZVRpbWUiOjE1OTgxMDI0NDA4MzcsImxhc3RDcmVhdGVUaW1lIjoxNTk4MDEzNzQ2OTg3fQ',
        '科技服务':'eyJmaXJzdElkIjo4NDQ0MTc3OTA2Nzg3OTMsImxhc3RJZCI6MTcyMjk1NDg5MTI2NSwiZmlyc3RDcmVhdGVUaW1lIjoxNTk3ODExNDA0NDkyLCJsYXN0Q3JlYXRlVGltZSI6MTU0MTU1NzQ0ODAwMH0',
    }
    fromData={
    "partner_id":"web",
    "timestamp":int(round(time.time()*1000)),
    "param":{
        "searchType":"article",
        "searchWord":"",
        "sort":"date",
        "pageSize":20,
        "pageEvent":1,
        "pageCallback":"",
        "siteId":1,
        "platformId":2
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'content-length': str(len(fromData))
        }
    count=0
    '''
    爬取逻辑
    对每个关键字先post获取文章id列表
    爬取id列表中的所有文章
    写入文件
    '''

    for word in keyWords:
        fromData['param']['searchWord']=word
        fromData['param']['pageCallback']=dic[word]
        IdList,pageCallback,hasNextPage=getArticleList(postURL,fromData,headers)
        while(True):
            #处理post获得的文章id
            for Id in IdList:
                page=getAritclePage(articleURL+str(Id))
                count=+1
                if page:
                    writeToDisk(path+str(Id)+'.txt',articleParser(page))
            #如果没有下一页
            if hasNextPage==0:
                break
            if(count==50):
                time.sleep(5)
                count=0
            #更新fromData,继续post
            fromData['param']['pageCallback']=pageCallback
            IdList,pageCallback,hasNextPage=getArticleList(postURL,fromData,headers)
        print("Finished processing keyword ", word)











    


