# -*- coding: utf-8 -*-\
# Written by panzy

import requests
from bs4 import BeautifulSoup
import re
import json

def getArticleContent(articleURL):
    res = requests.get(articleURL)
    print('Pull request to ' + articleURL)
    try:
        res.raise_for_status()
        res.encoding = 'utf-8'
        return res.text
    except:
        print('HTTPError: request failed.')

def processContent(content):
    soup = BeautifulSoup(content, 'html.parser')
    articleContent = soup.find('div', attrs = "article-content").get_text()
    articleTitle = soup.find('div', attrs = "article-content-title-box").find('div', attrs = "title").get_text()
    if soup.find('div', attrs = "m-article-time") != None:
        articleTime = soup.find('div', attrs = "m-article-time").get_text()
    elif soup.find('div', attrs = "show-time") != None:
        articleTime = soup.find('span', attrs = "show-time").get_text()
    else: articleTime = None
    articleInfo = {'title': articleTitle, 'content': articleContent, 'time': articleTime}
    print(articleInfo['time'], articleInfo['title'])

def getStreamLink(url, formData):
    articleLinkRes = requests.post(url, data = formData)
    articleLinkResJson = json.loads(articleLinkRes.text)
    articleLinkList = []
    for articleData in articleLinkResJson['data']['datalist']:
        articleLinkList.append(articleData['share_url'])
    print(articleLinkList, len(articleLinkList))
    return articleLinkList

def getSearchLink(url, formData):
    articleLinkRes = requests.post(url, data = formData)
    articleLinkList = []
    articleLinkRes.encoding = 'utf-8'
    articleLinkResJson = json.loads(articleLinkRes.text)
    for articleData in articleLinkResJson['data']['datalist']:
        articleLinkList.append(articleData['aid'])
    print(articleLinkList, len(articleLinkList))
        #print('Json Decode Error')
    return articleLinkList

if __name__ == '__main__':
    #url = 'https://article-api.huxiu.com/web/channel/articleList'
    #formData = {
    #    'platform': 'www',
    #    'last_time': '16000647150',
    #    'channel_id': '105',
    #    'pagesize':'22'
    #}

    url = 'https://search-api.huxiu.com/api/article'
    formData = {
        'platform': 'www',
        's': '人工智能',
        'page': 1,
        'pagesize': 20
    }

    while(True):
        articleLinkList = getSearchLink(url, formData)
        if articleLinkList == []:
            break
        for articleURL in articleLinkList:
            processContent(getArticleContent('https://m.huxiu.com/article/'+ str(articleURL) + '.html'))
        formData['page'] = formData['page'] + 1
        print(formData['page'])