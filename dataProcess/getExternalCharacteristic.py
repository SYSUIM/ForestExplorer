# -*- coding: utf-8 -*-
# Written by linxw

import csv
import json
import os

#获取当前拥有的行业的名称集合
IndustryList = []
csvfilePath = 'c:\\Users\\Lin\\Desktop\\ForestExplorer\\外部特征\\行业外部特征\\'
for i, j, k in os.walk(csvfilePath):
    for item in k:
        string = str(item)[:-4]
        IndustryList.append(string)

#读取基本信息，获得code，根据相应的情况匹配industry
def getBaseInfo():
    BaseInfoList = []
    industry = ''
    json_base = 'c:\\Users\\Lin\\Desktop\\ForestExplorer\\data\\json\\BaseInfoList.json'
    with open(json_base, 'r', encoding="utf-8") as f:
        json_basedata = json.load(f)
        for i in json_basedata:
            try:
                code = i['code']
                if (i.__contains__('所属行业') == False):
                    industry = '综合'
                elif ((i['所属行业']) in IndustryList):
                    industry = i['所属行业']
                else:
                    industry = '综合'
            except:
                print(i)
                industry = '综合'
                continue

            BaseInfo = {
                'code': code,
                'industry': industry
            }
            BaseInfoList.append(BaseInfo)
    return BaseInfoList

def getAccelerate(industry):
    # 打开外部特征的csv
    with open('c:\\Users\\Lin\\Desktop\\ForestExplorer\\外部特征\\行业外部特征\\' + industry + '.csv', 'r') as f:
        reader = csv.reader(f)
        result = list(reader)

    #进行特征运算，计算该年利润与上一年利润的比值
    Characteristic = {
        '2012': (float(result[1][1])/float(result[1][2])+float(result[1][1])/float(result[1][2])+float(result[1][2])/float(result[1][3])+float(result[1][3])/float(result[1][4])+float(result[1][4])/float(result[1][5])+float(result[1][5])/float(result[1][6])+float(result[1][6])/float(result[1][7]))/6,
        '2013': float(result[1][6])/float(result[1][7]),
        '2014': float(result[1][5])/float(result[1][6]),
        '2015': float(result[1][4])/float(result[1][5]),
        '2016': float(result[1][3])/float(result[1][4]),
        '2017': float(result[1][2])/float(result[1][3]),
        '2018': float(result[1][1])/float(result[1][2]),
        '2019': (float(result[1][1])/float(result[1][2])+float(result[1][1])/float(result[1][2])+float(result[1][2])/float(result[1][3])+float(result[1][3])/float(result[1][4])+float(result[1][4])/float(result[1][5])+float(result[1][5])/float(result[1][6])+float(result[1][6])/float(result[1][7]))/6,
        '2020': (float(result[1][1]) / float(result[1][2]) + float(result[1][1]) / float(result[1][2]) + float(
            result[1][2]) / float(result[1][3]) + float(result[1][3]) / float(result[1][4]) + float(
            result[1][4]) / float(result[1][5]) + float(result[1][5]) / float(result[1][6]) + float(
            result[1][6]) / float(result[1][7])) / 6

    }
    return Characteristic

#生成CSV文件
def getCSV(AccelerateInfo):
    # 创建文件对象
    f = open('c:\\Users\\Lin\\Desktop\\ForestExplorer\\data\\WaiBuTeZheng.csv', 'w', encoding='utf-8', newline='')
    # 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    #表头为每一年的年份
    csv_writer.writerow(['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'])
    #写入每一个行业的特征
    for item in AccelerateInfo:
        AccelerateList = []
        year = 2012
        for i in range(9):
            AccelerateList.append(item['accelerate'][str(year)])
            year += 1
        # 写入csv文件内容
        csv_writer.writerow(AccelerateList)

if __name__ == '__main__':
    BaseInfoList = getBaseInfo()
    ExternalCharacteristicList = []
    for i in BaseInfoList:
        try:
            ExternalCharacteristicDic = {
                'code': i['code'],
                'accelerate': getAccelerate(i['industry']),
            }
            ExternalCharacteristicList.append(ExternalCharacteristicDic)
        except:
            continue
    # 写入json文件
    with open('c:\\Users\\Lin\\Desktop\\ForestExplorer\\data\\json\\WaiBuTeZheng.json', 'w', encoding='utf-8') as f:
        json.dump(ExternalCharacteristicList, f)
    #写入csv文件
    with open('c:\\Users\\Lin\\Desktop\\ForestExplorer\\data\\json\\WaiBuTeZheng.json') as f:
        AccelerateInfo = json.load(f)
    getCSV(AccelerateInfo)