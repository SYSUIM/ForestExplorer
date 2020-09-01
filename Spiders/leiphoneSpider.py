# -*- coding: utf-8 -*-
# Written by panzy

import requests
import json
from bs4 import BeautifulSoup

def getStreamLink(url):
    print('Pull Request to ' + url)
    response = requests.get(url)
    try:
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except requests.HTTPError as e:
        print(e)
        print('HTTPError: Request for Article Web Failed.')

# 返回存有每篇文章字典信息的列表集合
def processStream(streamContent):
    streamContentSoup = BeautifulSoup(streamContent, 'html.parser')
    articleLinkInfoList = []
    for articleDiv in streamContentSoup.find('ul', attrs = "clr").find_all('li'):
        articleDivLink = articleDiv.find('a', attrs = 'headTit').attrs
        articleLinkInfo = {
            'link': articleDivLink['href'], # link键对应文章的URL
            'title': articleDivLink['title'] # title键对应文章的标题
        }
        articleLinkInfoList.append(articleLinkInfo)
    for articleLinkInfo in articleLinkInfoList:
        print(articleLinkInfo['link'] + ' ' + articleLinkInfo['title'])
    return articleLinkInfoList

def getRequestText(articleURL):
    print('Pull Request to ' + articleURL)
    response = requests.get(articleURL)
    try:
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except requests.HTTPError as e:
        print(e)
        print('HTTPError: Request for Article Web Failed.')

def processArticleText(responseText):
    soup = BeautifulSoup(responseText, 'html.parser')
    articleContentInfo = {
        'content': soup.find('div', attrs = "lph-article-comView").get_text(),
        'time': soup.find('td', attrs = "time").get_text()
    }
    return articleContentInfo

def spiderLeiPhone(articleLinkInfoList):
    articleContentList = []
    for articleInfo in articleLinkInfoList:
        articleContentInfo = processArticleText(getRequestText(articleInfo['link']))
        articleTitle = articleInfo['title']
        articleInfoDic = {
            'content' : articleContentInfo['content'],
            'time' : articleContentInfo['time'],
            'title' : articleTitle
        }
        print(articleInfoDic['title'] + ' ' + articleInfoDic['time'])
        articleContentList.append(articleInfoDic)
    return articleContentList

if __name__ == '__main__':
    activeURL = 'https://www.leiphone.com/category/sponsor/page/1'
    articleLinkInfoList = processStream(getStreamLink(activeURL))
    # 带字典的列表
    spiderLeiPhone(articleLinkInfoList)