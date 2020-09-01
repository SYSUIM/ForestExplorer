# -*- coding: utf-8 -*-
# Written by panzy

from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
import requests
import re
import json
import os
import time
import logging

trapInfo = {}
hotKeyWordsPath = 'C:\\Users\\Tommy Pan\\Desktop\\huxiu\\hotKeyword.txt'

'''
    用于实现虎嗅网的相关爬取工作
    To crawl articles on huxiu.com
'''

'''
    断点续爬通过更新配置文件实现
    如果断点续爬使用队列的形式实现
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
    try:
        articleContent = soup.find('div', attrs = "article-content").get_text()
        articleTitle = soup.find('div', attrs = "article-content-title-box").find('div', attrs = "title").get_text()
    except AttributeError as e:
        print(e)
        return {
            'title': None,
            'content': None,
            'time': None
        }
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
        trapInfo = {
            'keyword': formData['s'],
            'page': formData['page']
        }
        return trapInfo
        print('Failed to keyword visit ' + url)
    except Exception as e:
        print(e)
        print('Other Error happened.')

# 写入到指定路径，根据文章相关信息进行写入
def writeToDisk(path, articleInfo):
    if articleInfo['content'] == None:
        return
    with open(path, 'a', encoding='utf-8') as f:
        f.write(str(articleInfo['title']) + '\n' +str(articleInfo['time']) + '\n' + str(articleInfo['content']) + '\n')
        f.close()

# 获取热搜词条
def getHotKeyWords():
    hotURL = 'https://article-api.huxiu.com/tag/hot'
    formData = {
        'platform': 'www',  # 从PC平台检索
    }
    hotResponse = requests.post(hotURL, data=formData)
    hotKeyWordsJson = json.loads(hotResponse.text)
    hotKeyWordsList = hotKeyWordsJson['data']
    return hotKeyWordsList

# 对获得的指令进行基于频道内容的循环爬取
def crawlOnChannel(channelURL, channelFormData, path):
    while (True):
        articleLinkList = getStreamLink(channelURL, channelFormData)
        try:
            channelFormData['last_time'] = articleLinkList['last_time']
            for articleLink in articleLinkList['articleLinks']:
                if os.path.exists(path + str(articleLink)[-11:-5] + '.txt'):
                    print('chongfu')
                    continue
                else: writeToDisk(path + str(articleLink)[-11:-5] + '.txt', processContent(getArticleContent(articleLink)))
        except TypeError as e:
            print('Stream Ended.')
            break

# 对获得的指令进行基于热搜词条的循环爬取
def crawlBySearch(searchURL, searchFormData, path):
    hotKeyWordsList = updateKeywords()
    for hotKeyWord in hotKeyWordsList:
        searchFormData['s'] = hotKeyWord['keyword']
        searchFormData['page'] = hotKeyWord['page']
        while (True):
            articleLinkList = getSearchLink(searchURL, searchFormData)
            print('Search for: ' + hotKeyWord['keyword'] + ' page: ' + str(searchFormData['page']))

            # 做容错处理，如果收到的是429报错或者该检索词检索结束做结束循环处理
            if articleLinkList == []:
                with open(hotKeyWordsPath, 'r') as f:
                    hotKeywordJson = json.loads(f.read())
                    f.close()
                for hotKeyWordInfo in hotKeywordJson['awaiting']:
                    if hotKeyWordInfo['keyword'] == hotKeyWord['keyword']:
                        hotKeywordJson['awaiting'].remove(hotKeyWordInfo)
                        break
                hotKeywordJson['finished'].append(hotKeyWord['keyword'])
                with open(hotKeyWordsPath, 'w+') as f:
                    f.write(json.dumps(hotKeywordJson, ensure_ascii=False))
                    f.close()
                break
            elif type(articleLinkList) == dict:
                print('Trapped in point: keyword = ' + str(articleLinkList['keyword']) + ' ,page = ' + str(articleLinkList['page']))
                with open(hotKeyWordsPath,'r') as f:
                    hotKeywordJson = json.loads(f.read())
                    f.close()
                for hotKeyWordInfo in hotKeywordJson['awaiting']:
                    if hotKeyWordInfo['keyword'] == articleLinkList['keyword']:
                        hotKeyWordInfo['page'] = articleLinkList['page']
                        break
                with open(hotKeyWordsPath, 'w+') as f:
                    f.write(json.dumps(hotKeywordJson, ensure_ascii=False))
                    f.close()
                break

            for articleNum in articleLinkList:
                articleURL = 'https://m.huxiu.com/article/' + str(articleNum) + '.html'
                if os.path.exists(path + hotKeyWord['keyword'] + str(articleNum) + '.txt'):
                    print(path + hotKeyWord['keyword'] + str(articleNum) + '.txt has existed.')
                    continue
                else:
                    writeToDisk(path + hotKeyWord['keyword'] + str(articleNum) + '.txt',processContent(getArticleContent(articleURL)))
            searchFormData['page'] = searchFormData['page'] + 1

# 进行热搜爬取的指令
def crawlJob_search():
    path = 'C:\\Users\\Tommy Pan\\Desktop\\huxiu\\search\\'
    # 用于使用检索词的爬取(包含热门检索词的获取)
    searchURL = 'https://search-api.huxiu.com/api/article'
    searchFormData = {
        'platform': 'www',  # 从PC平台检索
        'page': 1,  # page是翻页指标
        'pagesize': 20  # pagesize不会影响page的翻页，即使超过也能访问
    }
    # if trapInfo != {}:
    #     searchFormData['s'] = trapInfo['keyword']
    #     searchFormData['page'] = trapInfo['page']

    # 关键词检索爬取
    crawlBySearch(searchURL, searchFormData, path)

# 进行频道内容的爬取指令
def crawlJob_Stream():
    path = 'C:\\Users\\Tommy Pan\\Desktop\\huxiu\\stream\\'
    # 用于使用栏目分类的爬取
    channelURL = 'https://article-api.huxiu.com/web/channel/articleList'
    channelFormData = {
        'platform': 'www',
        'last_time': '1597852200',
        'channel_id': '105',
        'pagesize': '22'
    }

    crawlOnChannel(channelURL, channelFormData, path)  # 栏目流爬取

def updateKeywords():
    hotKeywordsList = getHotKeyWords()
    print(hotKeywordsList)
    # 读取热搜数据
    with open(hotKeyWordsPath, 'r') as f:
        hotKeywordJson = json.loads(f.read())
        f.close()

    # 更新热搜爬取数据
    for hotKeyword in hotKeywordsList:
        exit_flag = False
        for hotKeywordInfo in hotKeywordJson['awaiting']:
            if hotKeyword == hotKeywordInfo['keyword']:
                # 已存在等候队列
                exit_flag = True
                break
        if hotKeyword in hotKeywordJson['finished']:
            # 已完成，根据时间追加爬取？后续优化
            continue
        elif exit_flag == True:
            # 已存在于等候队列
            continue
        else:
            hotKeywordInfo = {
                'keyword': hotKeyword,
                'page': 1
            }
            hotKeywordJson['awaiting'].append(hotKeywordInfo)
            with open(hotKeyWordsPath, 'w+') as tmp_f:
                tmp_f.write(json.dumps(hotKeywordJson, ensure_ascii = False))
                tmp_f.close()

    # 读取更新后的数据，返回当前需要爬取的检索词
    with open(hotKeyWordsPath, 'r') as f:
        hotKeywordJson = json.loads(f.read())
        hotKeyWordsList = hotKeywordJson['awaiting']
        f.close()
        return hotKeyWordsList


if __name__ == '__main__':
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔20min
    scheduler.add_job(crawlJob_search, 'interval', minutes = 30, id = 'crawlJob_search')
    # 添加任务,时间间隔20min
    # scheduler.add_job(crawlJob_Stream, 'interval', hours = 1, id = 'crawlJob_stream')
    scheduler.start()