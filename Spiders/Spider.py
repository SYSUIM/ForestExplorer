# -*- coding: utf-8 -*-
# Written by panzy

import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time

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
    except requests.HTTPError as e:
        print(e)
        print('HTTPError: Request for Article Failed.')

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
    try:
        articleLinkRes = requests.post(url, data = formData)
        articleLinkRes.raise_for_status()
        articleLinkResJson = json.loads(articleLinkRes.text)
        articleLinkList = {
            'articleLinks': []
        }
        articleLinkList['last_time'] = articleLinkResJson['data']['last_time']
        for articleData in articleLinkResJson['data']['datalist']:
            articleLinkList['articleLinks'].append(articleData['share_url'])
        print(articleLinkList['articleLinks'], len(articleLinkList['articleLinks']))
        return articleLinkList
    except requests.HTTPError as e:
        print(e)
        print('Failed to flowing visit ' + url)
    except Exception as e:
        print(e)
        print('Other Error happened.')

# 对网站进行指定关键词检索，获得检索结果中的文章编号
def getSearchLink(url, formData):
    try:
        articleLinkRes = requests.post(url, data = formData)
        articleLinkRes.raise_for_status()
        articleLinkList = []
        articleLinkRes.encoding = 'utf-8'
        articleLinkResJson = json.loads(articleLinkRes.text)
        for articleData in articleLinkResJson['data']['datalist']:
            articleLinkList.append(articleData['aid'])
        print(articleLinkList, len(articleLinkList))
        return articleLinkList
    except Exception as e:
        print(e)
        print('Failed to keyword visit ' + url)
    except Exception as e:
        print(e)
        print('Other Error happened.')

# 写入到指定路径，根据文章相关信息进行写入
def writeToDisk(path, articleInfo):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(str(articleInfo['title']) + '\n' +str(articleInfo['time']) + '\n' + str(articleInfo['content']) + '\n')
        f.close()

def getHotKeyWords():
    hotURL = 'https://article-api.huxiu.com/tag/hot'
    formData = {
        'platform': 'www',  # 从PC平台检索
    }
    hotResponse = requests.post(hotURL, data=formData)
    hotKeyWordsJson = json.loads(hotResponse.text)
    hotKeyWordsList = hotKeyWordsJson['data']
    return hotKeyWordsList

def crawlOnChannel(channelURL, channelFormData, path):
    while (True):
        articleLinkList = getStreamLink(channelURL, channelFormData)
        try:
            channelFormData['last_time'] = articleLinkList['last_time']
            if os.path.exists(path + str(articleLink)[-11:-5] + '.txt'):
                continue
            for articleLink in articleLinkList['articleLinks']:
                writeToDisk(path + str(articleLink)[-11:-5] + '.txt', processContent(getArticleContent(articleLink)))
        except TypeError as e:
            print('Stream Ended.')
            break

def crawlBySearch(searchURL, searchFormData, path):
    hotKeyWordsList = getHotKeyWords()
    for hotKeyWord in hotKeyWordsList:
        searchFormData['s'] = '电商' # s是检索内容
        hotKeyWord = searchFormData['s']
        while (True):
            articleLinkList = getSearchLink(searchURL, searchFormData)
            print('Search for: ' + hotKeyWord + ' page: ' + str(searchFormData['page']))
            if articleLinkList == []:
                break
            elif articleLinkList == None:
                break
            for articleNum in articleLinkList:
                articleURL = 'https://m.huxiu.com/article/' + str(articleNum) + '.html'
                if os.path.exists(path + hotKeyWord + str(articleNum) + '.txt'):
                    continue
                else:
                    writeToDisk(path + hotKeyWord + str(articleNum) + '.txt',
                                processContent(getArticleContent(articleURL)))
            searchFormData['page'] = searchFormData['page'] + 1

if __name__ == '__main__':
    path = 'C:\\Users\\Tommy Pan\\Desktop\\stream\\'

    # 用于使用栏目分类的爬取
    channelURL = 'https://article-api.huxiu.com/web/channel/articleList'
    channelFormData = {
        'platform': 'www',
        'last_time': '1597894020',
        'channel_id': '105',
        'pagesize': '22'
    }

    # 用于使用检索词的爬取(包含热门检索词的获取)
    searchURL = 'https://search-api.huxiu.com/api/article'
    searchFormData = {
        'platform': 'www',  # 从PC平台检索
        'page': 1,  # page是翻页指标
        'pagesize': 20  # pagesize不会影响page的翻页，即使超过也能访问
    }

    crawlOnChannel(channelURL, channelFormData, path) # 栏目流爬取

    crawlBySearch(searchURL, searchFormData, path) # 关键词检索爬取