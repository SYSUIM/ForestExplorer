# -*- coding: utf-8 -*-\
# Written by panzy

import requests
from bs4 import BeautifulSoup
import re
import json

'''
    用于实现虎嗅网的相关爬取工作
    To crawl articles on huxiu.com
'''

# 得到文章网址后获得网页静态内容
def getArticleContent(articleURL):
    res = requests.get(articleURL)
    print('Pull request to ' + articleURL)
    try:
        res.raise_for_status()
        res.encoding = 'utf-8'
        return res.text
    except:
        print('HTTPError: request failed.')

# 对静态文章网页进行解析，返回含标题，时间和内容的字典
def processContent(content):
    soup = BeautifulSoup(content, 'html.parser')
    articleContent = soup.find('div', attrs = "article-content").get_text()
    articleTitle = soup.find('div', attrs = "article-content-title-box").find('div', attrs = "title").get_text()
    # 静态网页的时间戳位置不确定，容错
    if soup.find('div', attrs = "m-article-time") != None:
        articleTime = soup.find('div', attrs = "m-article-time").get_text()
    elif soup.find('div', attrs = "show-time") != None:
        articleTime = soup.find('span', attrs = "show-time").get_text()
    else: articleTime = None
    articleInfo = {'title': articleTitle, 'content': articleContent, 'time': articleTime}
    print(articleInfo['time'], articleInfo['title'])
    return articleInfo

# 对网站流页面的爬取，存在翻页的问题，暂时弃用
def getStreamLink(url, formData):
    articleLinkRes = requests.post(url, data = formData)
    articleLinkResJson = json.loads(articleLinkRes.text)
    articleLinkList = []
    for articleData in articleLinkResJson['data']['datalist']:
        articleLinkList.append(articleData['share_url'])
    print(articleLinkList, len(articleLinkList))
    return articleLinkList

# 对网站进行指定关键词检索，获得检索结果中的文章编号
def getSearchLink(url, formData):
    articleLinkRes = requests.post(url, data = formData)
    articleLinkList = []
    articleLinkRes.encoding = 'utf-8'
    articleLinkResJson = json.loads(articleLinkRes.text)
    for articleData in articleLinkResJson['data']['datalist']:
        articleLinkList.append(articleData['aid'])
    print(articleLinkList, len(articleLinkList))
    return articleLinkList

# 写入到指定路径，根据文章相关信息进行写入
def writeToDisk(path, articleInfo):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(str(articleInfo['title']) + '\n' +str(articleInfo['time']) + '\n' + str(articleInfo['content']) + '\n')
        f.close()

if __name__ == '__main__':
    path = 'C:\\Users\\Tommy Pan\\Desktop\\test\\'
    url = 'https://search-api.huxiu.com/api/article'
    formData = {
        'platform': 'www', # 从PC平台检索
        's': '人工智能', # s是检索内容
        'page': 1, # page是翻页指标
        'pagesize': 20 # pagesize不会影响page的翻页，即使超过也能访问
    }

    while(True):
        articleLinkList = getSearchLink(url, formData)
        if articleLinkList == []:
            break
        for articleNum in articleLinkList:
            articleURL = 'https://m.huxiu.com/article/'+ str(articleNum) + '.html'
            writeToDisk(path + str(articleNum) + '.txt', processContent(getArticleContent(articleURL)))
        # formData['page'] = formData['page'] + 1
        #print(formData['page'])

    # 用于使用栏目分类的爬取
    #url = 'https://article-api.huxiu.com/web/channel/articleList'
    #formData = {
    #    'platform': 'www',
    #    'last_time': '16000647150',
    #    'channel_id': '105',
    #    'pagesize':'22'
    #}