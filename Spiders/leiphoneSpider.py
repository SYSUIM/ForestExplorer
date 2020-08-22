# -*- coding: utf-8 -*-
# Written by panzy

import requests
import json
from bs4 import BeautifulSoup

def getStreamLink(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except:
        print('HTTPError: Request Failed.')

# 返回存有每篇文章字典信息的列表集合
def processStream(streamContent):
    streamContentJson = json.loads(streamContent)
    streamContentSoup = BeautifulSoup(streamContentJson['html'], 'html.parser')
    articleLinkInfoList = []
    for articleDiv in streamContentSoup.find_all('li'):
        #print(articleDiv.find('a', attrs = 'headTit').attrs)
        articleDivLink = articleDiv.find('a', attrs = 'headTit').attrs
        articleLinkInfo = {
            'link': articleDivLink['href'], # link键对应文章的URL
            'title': articleDivLink['title'] # title键对应文章的标题
        }
        articleLinkInfoList.append(articleLinkInfo)
    print(articleLinkInfoList)
    return articleLinkInfoList

if __name__ == '__main__':
    activeURL = 'https://www.leiphone.com/site/AjaxLoad/page/1'
    processStream(getStreamLink(activeURL))