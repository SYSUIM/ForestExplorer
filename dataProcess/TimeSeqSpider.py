import json
import requests
import time

def getBaseInfo(code):
    null=""
    fromData={'mergerMark':'sysapi1068','paramStr':'scode='+code}  
    page=requests.post('http://www.cninfo.com.cn/data/project/commonInterface', data = fromData) 
    BaseInfoDic={} 
    BaseInfoDic['code']=code
    try:
        BaseInfo = json.loads(page.text[1:-1])
        BaseInfoDic['成立时间']=BaseInfo['F001D']
        BaseInfoDic['上市日期']=BaseInfo['F002D']
        BaseInfoDic['所属行业']=BaseInfo['F010V']
        BaseInfoDic['上市板块']=BaseInfo['F011V']
        print('succeed in processing ',code)
    except:
        print('fail to process ',code)
    finally:
        return BaseInfoDic

def getZhiBiao(code):
    null=""
    fromData={'mergerMark':'sysapi1074','paramStr':'scode='+code+';rtype=1'}  
    page=requests.post('http://www.cninfo.com.cn/data/project/commonInterface', data = fromData) 
    ZhiBiaoDic={} 
    ZhiBiaoDic['code']=code
    try:
        ZhiBiaoList=eval(page.text)
        for ZhiBiao in ZhiBiaoList:
            ZhiBiaoDic[ZhiBiao['index']]={}
            year=2011
            for i in range(10):
                if str(year) in ZhiBiao.keys():
                    ZhiBiaoDic[ZhiBiao['index']][str(year)]=ZhiBiao[str(year)]
                else:
                    ZhiBiaoDic[ZhiBiao['index']][str(year)]=''
                year+=1
        print('succeed in processing ',code)
    except:
        print('fail to process ',code)
    finally:
        return ZhiBiaoDic

def getLiRun(code):
    null=''
    fromData={'mergerMark':'sysapi1075','paramStr':'scode='+code+';rtype=1;sign=2'}
    page=requests.post('http://www.cninfo.com.cn/data/project/commonInterface', data = fromData) 
    LiRunDic={} 
    LiRunDic['code']=code
    try:
        LiRunList=eval(page.text)
        for LiRun in LiRunList:
            LiRunDic[LiRun['index']]={}
            year=2011
            for i in range(10):
                if str(year) in LiRun.keys():
                    LiRunDic[LiRun['index']][str(year)]=LiRun[str(year)]
                else:
                    LiRunDic[LiRun['index']][str(year)]=''
                year+=1
        print('succeed in processing ',code)
    except:
        feature=['营业收入','营业成本','营业利润','利润总额','所得税','净利润']
        for fea in feature:
            LiRunDic[fea]={}
            year=2011
            for i in range(10):
                LiRunDic[fea][str(year)]=''
                year+=1
        print('fail to process ',code)
    finally:
        return LiRunDic

def getXianJin(code):
    null=''
    fromData={'mergerMark':'sysapi1076','paramStr':'scode='+code+';rtype=1;sign=2'}
    page=requests.post('http://www.cninfo.com.cn/data/project/commonInterface', data = fromData) 
    XianJinDic={} 
    XianJinDic['code']=code
    try:
        XianJinList=eval(page.text)
        for XianJin in XianJinList:
            XianJinDic[XianJin['index']]={}
            year=2011
            for i in range(10):
                if str(year) in XianJin.keys():
                    XianJinDic[XianJin['index']][str(year)]=XianJin[str(year)]
                else:
                    XianJinDic[XianJin['index']][str(year)]=''
                year+=1
        print('succeed in processing ',code)
    except:
        feature=['经营活动产生的现金流量净额','投资活动产生的现金流量净额','筹资活动产生的现金流量净额']
        for fea in feature:
            XianJinDic[fea]={}
            year=2011
            for i in range(10):
                XianJinDic[fea][str(year)]=''
                year+=1
        print('fail to process ',code)
    finally:
        return XianJinDic

def writeJson(List,path):
    res=json.dumps(List, indent=4, ensure_ascii=False)
    with open(path,'w',encoding='utf-8') as f:
        print("writing file ", path, ".......")
        f.write(res)

def readFile(path,startline):
    List=[]
    with open(path,'r',encoding='utf-8') as f:
        while(startline>0):
            code=f.readline().replace('.SZ','').replace('.SH','').replace('.OC','').replace('\n','')
            startline-=1
        while(code):
            List.append(code)
            code=f.readline().replace('.SZ','').replace('.SH','').replace('.OC','').replace('\n','')
    return List

def readJson(path):
    with open(path,'r',encoding='utf-8') as f:
        InfoList=json.load(f)
    return InfoList

def Spider(companyCodeFile,BaseInfoPath,LiRunPath,XianJinPath,ZhiBiaoPath):
    companyCodeList = readFile(companyCodeFile,0)
    BaseInfoList=[]
    LiRunList=[]
    XianJinList=[]
    ZhiBiaoList=[]
    for code in companyCodeList:
        writeJson(BaseInfoList.append(getBaseInfo(code)),BaseInfoPath)
    for code in companyCodeList:
        writeJson(LiRunList.append(getLiRun(code)),LiRunPath)
    for code in companyCodeList:
        writeJson(XianJinList.append(getXianJin(code)),XianJinPath)
    for code in companyCodeList:
        writeJson(ZhiBiaoList.append(getZhiBiao(code)),ZhiBiaoPath)

    
if __name__=='__main__':
    #共有3999个公司代码
    companyCodeFile = '证券代码.txt'
    BaseInfoPath ='3999_BaseInfoList.json'
    LiRunPath = '3999_LiRunList.json'
    XianJinPath = '3999_XianJinList.json'
    ZhiBiaoPath = '3999_ZhiBiaoList.json'
    Spider(companyCodeFile,BaseInfoPath,LiRunPath,XianJinPath,ZhiBiaoPath)





    






    






