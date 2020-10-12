import json
import os
import re

#将第一个文件工商注册写成json，返回列表
def writeFirstInfo(filePath,featureList):
    totalCompanyInfo=[]
    #读出原来的json文件
    with open(filePath,'r',encoding='utf-8') as f:
        companyList=json.load(f)
    for company in companyList:
        CompanyInfo={}
        count=0
        for feature in featureList:
            #进行单位处理
            if feature == 'reg_capital':
                try:
                    string=str(company['reg_capital']['value'])
                    string=string.replace(',','') 
                    danwei=re.findall(r'((\D+))',string)[0]
                    money=int(re.findall(r'(\d+)',string)[0])
                    if danwei=='美元':
                        money*=6.83
                    if danwei=='香港元':
                        money*=0.88
                    oldCompany['reg_capital']=money  
                    count+=1
                except(Exception):
                    count+=1
                    print("error happend in ",count) 
            else:
                CompanyInfo[feature]=company[feature]['value']
                count+=1
        totalCompanyInfo.append(CompanyInfo)
    return totalCompanyInfo

#写入文本信息
def writeTextInfo(filePath,totalCompanyInfo,featureList):
    with open(filePath,'r',encoding='utf-8') as f:
        companyList=json.load(f)
    for oldCompany in totalCompanyInfo:
        flag=0
        for company in companyList:        
            if oldCompany['company_name']==company['company']['value']:
                for feature in featureList:
                    oldCompany[feature]=company[feature]['value']
                    flag=1
                break
       #找不到
        if flag==0:
            for feature in featureList:
                oldCompany[feature]=""
    return totalCompanyInfo

#写入统计数字信息
def writeNumberInfo(filePath,totalCompanyInfo,featurename):
    with open(filePath,'r',encoding='utf-8') as f:
        companyList=json.load(f)
    for oldCompany in totalCompanyInfo:
        count=0
        for company in companyList:        
            if oldCompany['company_name']==company['company']['value']:
                count+=1
        oldCompany[featurename]=count
        #print(oldCompany['company_name'],featurename,":",count)
    return totalCompanyInfo

#写入是/否信息
def writeBooleanInfo(filePath,totalCompanyInfo,featurename):
    with open(filePath,'r',encoding='utf-8') as f:
        companyList=json.load(f)
    for oldCompany in totalCompanyInfo:
        count=0
        for company in companyList:        
            if oldCompany['company_name']==company['company']['value']:
                count=1
                break
        oldCompany[featurename]=count
    return totalCompanyInfo

#将list写成json文件
def writeJson(totalCompanyInfo,savePath):
    res=json.dumps(totalCompanyInfo,indent=4, ensure_ascii=False)
    with open(savePath,'w',encoding='utf-8') as f:
        print("writing file ", savePath, ".......")
        f.write(res)

def FileProcess(filelist,typelist,featurelist,jsonpath):
    #处理基本信息文件，生成第一个字典
    totalCompanyInfo=writeFirstInfo(filelist[0],featurelist[0])
    print("processing file ", filelist[0])
    #根据类型处理后面的每一个文件
    for i in range(1,len(filelist)):
        if typelist[i] == 'text':
            totalCompanyInfo=writeTextInfo(filelist[i],totalCompanyInfo,featurelist[i])
        if typelist[i] == 'number':
            totalCompanyInfo=writeNumberInfo(filelist[i],totalCompanyInfo,featurelist[i])
        if typelist[i] == 'boolean':    
            totalCompanyInfo=writeBooleanInfo(filelist[i],totalCompanyInfo,featurelist[i])
        print("processing file ", filelist[i])
    writeJson(totalCompanyInfo,totalCompanyInfo)


if __name__ == '__main__':
    #filelist第一个必须是工商注册，后面为需要处理对的其他文件
    filelist=['01工商注册.json','05对外投资.json','13网站备案.json']
    #文件处理的类型,第一个对应工商注册文件，填空即可
    #text表示直接保留文本信息，需要特征列表，特征名称与json文件一致
    #number表示统计文件中某一公司出现的次数，，即公司某个特征的数量值，需要一个特征
    #boolean表示统计文件中是否出现了某个公司，即公司是否具有某个特征,需要一个特征
    typelist=['','number','boolean']
    featurelist=[['company_name','industry'],'投资企业个数','是否有网站备案']
    #形成的json文件保存的地址
    jsonlist='7290_BaseInfoList.json'
    FileProcess(filelist,typelist,featurelist,jsonlist)
    



    

