from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
import csv
import json

#将json文件写成csv
def JsonToCSV(csvpath,jsonpath,feaList):
    with open(csvpath,"w",encoding='utf-8',newline='') as csvfile:
        writer = csv.writer(csvfile)
        #写入特征名称
        writer.writerow(feaList)
        #将json文件导入
        with open(jsonpath,"r",encoding='utf-8') as f:
            companyList=json.load(f)
        for company in companyList:
            companyFeaList=[]
            for fea in feaList:
                companyFeaList.append(company[fea])
            #csv.writerow只能写入list或者Array
            writer.writerow(companyFeaList)

#将csv文件中的数据变成输入数组
def getArr(csvpath,arrpath):
    np.set_printoptions(suppress=True)
    df=pd.read_csv(csvpath)
    #取出需要编码的文字部分
    strdf=df.iloc[:,0:4]
    df.iloc[:,-1]=df.iloc[:,-1].map(lambda x: x / 1000)
    #数字部分直接变成数组
    intarr=np.array(df.iloc[:,4:])
    #位置编码
    strdf = strdf.astype(str).apply(LabelEncoder().fit_transform)
    #独热编码，返回array对象
    strarr=OneHotEncoder().fit_transform(np.array(strdf)).toarray() 
    arr=np.concatenate((strarr,intarr),axis=1) 
    #保存数字文件
    print("writing file ",arrpath," ......")
    np.savetxt(arrpath,arr)
    #返回拼接的数组
    return arr



if __name__ =='__main__':
    jsonpath='541_BaseInfoList.csv'
    csvpath='541_BaseInfo.csv'
    arrpath='541_BaseInfoArr.txt'    
    feaList=["ent_type","industry","open_status","type","分公司数量","投资企业个数","控股企业个数","专利个数","商标个数","裁判文书个数","失信记录个数","竞品个数","企业项目个数","新闻个数","是否上市","是否有网站备案","是否有违法记录","是否经营异常","是否有知识产权出质","是否有行政许可","软著信息个数","高层数量","reg_capital"]
    JsonToCSV(csvpath,jsonpath,feaList)
    getArr(csvpath,arrpath)











