import numpy as np
import re
import json
import os
import csv
import pandas
from transformers import BertModel,BertTokenizer
import torch

#将文本长度按照568个字切分成多个部分，返回列表
def seg_text(text):
    index=0
    textlist=[]
    count=0
    while True:
        if len(text[index:]) < 128 :
            textlist.append(text[index:])
            count += 1
            break
        subtext=text[index:index+128]
        textlist.append(subtext)
        index += 128
        count += 1
    return textlist

#拼接数组保存，保存
def concat(arr_list,arrpath):
    arr = arr_list[0]
    for i in range(1, len(arr_list)):
        arr=np.concatenate((arr,arr[i]), axis=0)
    np.safetxt(arrpath, arr)
    return arr

#加载模型
def load_model(bertpath):
    bertmodel = BertModel.from_pretrained(bert-base-chinese)
    tokenizer = BertTokenizer.from_pretrained(bertpath)
    return bertmodel,tokenizer

#利用bert模型编码
def get_code(bertmodel,tokenizer,text):
    text = tokenizer.encode(text[1:-1])
    input_ids = torch.tensor(text).unsqueeze(0)
    outputs = bertmodel(input_ids)
    arr = outputs[1][0].cuda().data.cpu().numpy()
    return arr

#对新闻进行Bert编码
def BertCode(bertpath,jsonpath,arrpath):
    bertmodel,tokenizer=load_model(bertpath)
    with open(jsonpath,'r',encoding='utf-8') as f:
        company_list=json.load(f)
    for company in company_list:
        if os.path.exists(arrpath+company['company']+company['date']+'.txt'):
            print("skip file ",arrpath+company['company']+company['date']+'.txt')
            continue
        textlist=seg_text(company['text'])
        arrlist=[]
        for text in textlist:
            arrlist.append(get_code(bertmodel,tokenizer,text))
        concat(arrlist,arrpath+company['company']+company['date']+'.txt')        
        print(company['company'],company['date'],'.txt    ')   


#将数组填充至定长    
def pad(arr,maxlength):
    length=arr.shape[0]
    pad_length=maxlength-length
    arr=np.pad(arr,(0,pad_length),'constant', constant_values=(0,0))
    print("padding to ", maxlength)
    return arr 

#读取数组
def getArr(arrpath):
    arr=np.loadtxt(arrpath)
    print(arrpath," 数组维度：",arr.shape)
    return arr

#写入数组
def writeArr(newarrpath,arr):
    np.savetxt(newarrpath,arr)
    print("saving in ",newarrpath)

#获得文件夹下的数组文件的最高纬度
def get_max_length(dir_path):
    filelist=os.listdir(dir_path)
    max_length=0
    for filename in filelist:
        length=getArr(dir_path+filename).shape[0]
        if length>max_length:
            max_length=length
    print("max length ", max_length)
    return max_length

#将新闻数组填充
def getPadCode(dir_path,pad_arr_path):    
    max_length=get_max_length(dir_path)
    filelist=os.listdir(dir_path)
    for filename in filelist:
       writeArr(pad_arr_path+filename,pad(getArr(dir_path+filename),max_length))

#产生新闻编码的csv文件
def getNewsCodeCsv(dirpath,csvpath,size):
    namelist=[]
    filelist=os.listdir(dirpath)
    #取出所有的公司名称
    for filename in filelist:
        namelist.append(filename[0:-8])
    with open(csvpath,'w',encoding='utf-8') as f:
        wrtier=csv.writer()
        for company in namelist:
            if company+'2018.txt' in filelist:
                arr1=np.loadtxt(csvpath+company+'2018.txt')
            else:
                arr1=np.zeros(shape=(size,))
            if company+'2019.txt' in filelist:
                arr2=np.loadtxt(csvpath+company+'2019.txt')
            else:
                arr2=np.zeros(shape=(size,))      
            if company+'2020.txt' in filelist:
                arr3=np.loadtxt(csvpath+company+'2020.txt')
            else:
                arr3=np.zeros(shape=(size,))
            wrtier.writerow(np.concatenate(arr1,arr2,arr3))
    #返回公司名称
    return namelist


if __name__=='__main__':
    bertpath='bert-base-chinese'
    jsonpath='MatchNews_len_1024.json'
    newsdirpath='newsarr\\'
    padnewsdirpath='padnewsarr\\'
    csvpath='407_newsarr.csv'
    BertCode(bertpath,jsonpath,newsdirpath) 
    getPadCode(newsdirpath,padnewsdirpath)
    getNewsCodeCsv(padnewsdirpath,csvpath,get_max_length(newsdirpath))


