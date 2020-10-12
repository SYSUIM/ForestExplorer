import numpy as np
import csv
import pandas as pd
import json
from sklearn import preprocessing

#将每一个json文件处理成csv
def getCsv(jsonpath,csvpath,feaList):
    titleList=[]
    year=2012
    for i in range(9):
        for fea in feaList:
            titleList.append(str(year)+fea)
        year+=1
    with open(jsonpath,'r',encoding='utf-8') as f :
        InfoList=json.load(f)
    print(" finish reading file .....")
    with open(csvpath,'w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(titleList)
        print(" finish writing title .....")
        for company in InfoList:
            timeSeq=[]
            year=2012
            for i in range(9):
                for fea in feaList:
                    if fea in company.keys() and company[fea][str(year)] != '':
                       timeSeq.append(company[fea][str(year)])
                    else:
                        timeSeq.append(0)
                year+=1
            writer.writerow(timeSeq)
            print(" finish writing ", company['code'], ' ......')

#将三个文件拼接成一个总的csv，三个文件分别是利润、现金、指标、外部特征
def getAllCsv(csvpath1,csvpath2,csvpath3,csvpath4,csvpath,startyear):
    df1=pd.read_csv(csvpath1)
    df2=pd.read_csv(csvpath2)
    df3=pd.read_csv(csvpath3)
    df4=pd.read_csv(csvpath4)
    #注意起始年份
    index1=0+(startyear-2012)*6
    index2=0+(startyear-2012)*3
    index3=0+(startyear-2012)*6
    index4=0+(startyear-2012)*1
    total_df=pd.DataFrame()
    for i in range(8):
        total_df=pd.concat([total_df,df1.iloc[:,index1:index1+6],df2.iloc[:,index2:index2+3],df3.iloc[:,index3:index3+6],df4.iloc[:,index4:index4+1]],axis=1)
        index1+=6
        index2+=3
        index3+=6
        index4+=1
    total_df.to_csv(csvpath,index=False)

#将csv文件中的数据变成输入数组
def getarr(csvpath,arrpath):
    df=pd.read_csv(csvpath)
    arr=np.array(df)
    rr = arr.astype(np.float32)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))   
    arr_minMax = min_max_scaler.fit_transform(arr)  
    np.savetxt(arrpath,arr_minMax)
    return arr

#将csv文件中的数据变成输出数组
def getarrY(csvpath,arrpath,topiclist):
    df=pd.read_csv(csvpath)
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    arr=np.array(df[topiclist[0]]).reshape(-1,1)
    for i in range(1,8):
        arr1=np.array(df[topiclist[i]]).reshape(-1,1)
        arr=np.concatenate((arr,arr1),axis=1)
    arr_minMax = min_max_scaler.fit_transform(arr)
    np.savetxt(arrpath,arr_minMax)

#匹配新闻和时间序列，将编码好的新闻csv文件与之前的时间序列数组拼接在一起，返回新的数组
def newsSeqconcat(newspath,timeseqpath,matchpath,arrpath):
    flag=1
    match_df=pandas.read_csv(matchpath,header=None)
    #取出18年至20年部分
    seq_arr=np.loadtxt(timeseqpath)
    seq_df=pandas.DataFrame(seq_arr).iloc[:,80:]
    news_df=pandas.read_csv(newspath,header=None)
    for i in range(match_df.shape[0]):
        seq_row_index=match_df.iat[i,1]
        news_row_index=match_df.iat[i,2]
        arr_pd=pandas.DataFrame()
        seq_col_index=0
        news_col_index=0
        for j in range(3):
            arr_pd=pandas.concat([seq_df.iloc[seq_row_index,seq_col_index:seq_col_index+16],news_df.iloc[news_row_index,news_col_index:news_col_index+1536]],axis=0)
            if flag:
                arr=np.array(arr_pd).reshape(1,-1)
                #表示是否是第一个时间特征  
                flag=0  
            else :
                arr=np.concatenate((arr,np.array(arr_pd).reshape(1,-1)),axis=1)       
            seq_col_index += 16
            news_col_index += 1536
        print(arr.shape)
        #表示是否是第一个时间特征
        flag=1
        #判断是否第一个样本
        if i == 0:
            total_arr=arr
        else:
            total_arr=np.concatenate((total_arr,arr),axis=0) 
    np.savetxt(arrpath,total_arr)
    print(total_arr.shape)

#得到相应数据集的对应输出Y值
def getNewsSeq_Y(lirunseqpath,matchpath,arrpath):
    match_df=pandas.read_csv(matchpath,header=None)
    #取出18年至20年部分
    seq_arr=np.loadtxt(lirunseqpath)
    seq_df=pandas.DataFrame(seq_arr).iloc[:,5:]
    for i in range(match_df.shape[0]):
        seq_row_index = match_df.iat[i,1]
        arr_pd = seq_df.iloc[seq_row_index,:]
        if i==0 :
            total_arr=np.array(arr_pd).reshape(1,-1)
        else:
            total_arr=np.concatenate((total_arr,np.array(arr_pd).reshape(1,-1)),axis=0) 
    np.savetxt(arrpath,total_arr)
    print(total_arr.shape)

#删除数组中的某部分特征
def delPartCode(arrpath,newarrpath,del_topic):
    arr=np.loadtxt(arrpath)
    if del_topic=='TimeSeq':
        start_index=0
        length=15
        tab_index=1537
    elif del_topic=='Environment':
        start_index=15
        length=1
        tab_index=1551
    elif del_topic=='News':
        start_index=16
        length=1536
        tab_index=16
    else :
        print("ERROR")
        return
    del_list=[]
    for i in range(3):
        del_list += range(start_index,start_index+length)
        start_index += tab_index+length
    new_arr=np.delete(arr,del_list,axis=1)
    np.savetxt(newarrpath,new_arr)
    print(new_arr.shape)
    return new_arr

if __name__=='__main__':
    csvpath1='3999_LiRunInfo11_20.csv' 
    csvpath2='3999_XianJInInfo11_20.csv' 
    csvpath3='3999_ZhiBiaoInfo11_20.csv' 
    csvpath4='3999_Environment_12_20.csv' 
    csvpath13_20='new_TotalInfo13_20.csv'
    csvpath12_19='3999_TotalInfo12_19.csv'
    arrpath12_19='3999_TotalInfoArr_12_19.txt'
    arrpath13_20='3999_LiRunArr_13_20'
    startyear=2012
    arrYpath='3999_LiRunArr_13_20.txt'
    topiclist=['2013净利润','2014净利润','2015净利润','2016净利润','2017净利润','2018净利润','2019净利润','2020净利润']
    getAllCsv(csvpath1,csvpath2,csvpath3,csvpath4,csvpath12_19,startyear)
    getarr(csvpath12_19,arrpath12_19)
    getarrY(csvpath13_20,arrYpath,topiclist)
    matchpath='407_Match.csv'
    arrnewspath='228_newsSeq.txt'
    arrnewsYpath='228_newsYSeq.txt'
    del_arrpath='228_newsSeq_del_TimeSeq.txt'
    del_topic='TimeSeq'
    newsSeqconcat(csvpath12_19,arrpath12_19,matchpath,arrnewspath)
    getNewsSeq_Y(arrYpath,matchpath,arrnewsYpath)
    delPartCode(arrpath12_19,del_arrpath,del_topic)
 

