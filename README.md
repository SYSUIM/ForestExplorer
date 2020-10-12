# ForestExplorer
> written by panzy.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8.5-red"/>
  <img src="https://img.shields.io/badge/pytorch-1.6.0-yellow"/>
  <img src="https://img.shields.io/badge/Anaconda-4.8.3-blue"/>
  <img src="https://img.shields.io/badge/docs-English-green"/>
  <img src="https://img.shields.io/badge/Bert-unknown-purple"/>
</p>

ForestExplorer 是完全基于python语言开发的，基于企业内部、行业市场外部特征进行发展预测的数据分析框架。使用 Anaconda (4.8.3) 和 pip (20.1.1) 配置代码环境。

<br><br>

## 0. Content
---
本节将对我们的工作作简要描述，根据数据处理的工作流程，分为以下三个模块：

- [特征分析框架](#tezhengfenxi)
  - [网络爬虫](#spider)
  - [数据抽取](#dataextraction)

- [多源数据策略编码器](#encoding)
  - [One-hot](#onehot)
  - [Bert](#bert)
  - [数据归一化](#datanormalization)

- [序列拟合模型(MultiSource-LSTM)](#model)
  - [Load DataSet](#loaddataset)
  - [Baseline](#baseline)

<br>

## <span id="tezhengfenxi">1. 特征分析框架</span>
---
特征分析框架主要完成以下工作：[网络爬虫](#spider)、[数据抽取](#dataextraction)。

<br>

### <span id="spider">1.1 网络爬虫</span>

实验中出于对行业的外部环境特征分析的需要，对高新科技门户网站的文本内容进行规则框架内、有限度的爬取，各网站内容详情请见[虎嗅网](https://www.huxiu.com/)，[199IT](http://www.199it.com/)，[36氪](https://36kr.com/)，[雷锋网](https://www.leiphone.com/)，[科学世界网](http://www.twwtn.com)，[维科网](https://www.ofweek.com)。



**爬虫开发环境**：以下为前期网站爬取过程中所使用的 python 第三方包：

|    Packages    | Version |
| :------------: | :-----: |
|    requests    | 2.24.0  |
|      bs4       |  0.0.1  |
| beautifulsoup4 |  4.9.1  |
|      lxml      |  4.5.1  |
|  APScheduler   |  2.1.2  |

<br>

保存以下代码至当前目录下新文件 `./SpiderRequirements.txt` 以安装python爬虫环境：

```
APScheduler==2.1.2
requests==2.24.0
bs4==0.0.1
beautifulsoup4==4.9.1
lxml==4.5.1
```

使用 `pip install -r ./SpiderRequirements.txt` 命令完成环境安装，或者可以使用我们提供的 `requirements.txt` 直接完整框架环境的安装。



**爬虫代码**：不同网站结构不同，我们针对每个网站编写了专门的爬虫脚本，在装有以上第三方包的python环境下即可直接运行，请确保文件保存路径符合系统要求。

- [*HuXiu Spider*](Spiders/HuXiu/Spider.py)：虎嗅网爬虫提供了两种爬取方式，分别是流式爬取和关键词爬取。其中，流式爬取主要由方法`crawlJob_Stream` 实现，关键词爬取由 `crawljob_search` 实现，由于流式爬取文章数的限制，现只默认调用关键词爬取方法。该爬虫提供了断点续爬功能，请创建 `./hotKeyword.txt` 文件作为关键词爬取的断点记录文件，或使用本项目提供的模版 [*hotKeyword.txt*](Spiders/HuXiu/hotKeyword.txt) 来实现该功能。此外，为避免高强度访问网站，设置了定时爬取功能，默认间隔时间为30分钟。
  - 运行 `python create.py ` 生成断点配置模板
  - 运行 `python Spider.py` 进行网页爬取，并保存到指定路径
- 36kr spider：36氪爬虫通过手动获取特定关键词以及callback编码，获取相应关键词的文章。当访问量过大时，会受到访问限制。
  - 运行 `python 36kr_spider.py` 进行网页爬取，并保存到指定路径
- 199IT spider：199IT爬虫通过自主选取关键词，通过`get_id`获取相应文章对应的id列表，写入文件，然后通过`get_articles`获取相应id的文章内容保存到path中。当访问量过大时，会受到访问限制。
  - 运行 `python 199_spider.py` 进行网页爬取，并保存到指定路径
- mckinsey spider：mckinsey爬虫通过租住选择关键词，爬取对应文章保存到path中。当访问量过大时，会受到访问限制。
  - 运行 `python mckinsey_spider.py` 进行网页爬取，并保存到指定路径

<br>

## <span id="dataextraction">1.2 数据抽取</span>

**FileProcess.py**：从26个json文件中抽取特征，处理成为一个静态特征的json文件。

参数设置：

filelist：需要进行特征抽取的json文件列表，第一个必须是01工商注册.json

typelist：每个json文件对应的处理函数，分别有text,number,boolean三种，text直接保留样本特征内容，number将统计文件中样本某个特征的出现次数，boolean统计样本是否含有某个特征

featurelist：每个json文件中要抽取的特征

jsonlist：静态特征的json文件的保存路径

调用方法：

FileProcess(filelist,typelist,featurelist,jsonlist)

**TimeSeqSpider.py：**通过公司的证券代码，爬取巨潮资讯上相应公司的基本信息，利润序列信息，现金序列信息，指标序列信息，并返回一个json文件。

参数设置：

companyCodeFile：公司证券代码的csv文件

BaseInfoPath：保存基本信息的json文件路径

LiRunPath：保存利润序列信息的json文件路径

XianJinPath：保存现金序列信息的json文件路径

ZhiBiaoPath：保存指标序列信息的json文件路径

调用方法：

Spider(companyCodeFile,BaseInfoPath,LiRunPath,XianJinPath,ZhiBiaoPath)

## 2. 多元数据策略编码

### 2.1 One-hot编码

Json2Onehot.py：将静态json的文件转为csv文件，对其中的离散型文字特征进行one-hot编码，对所有的数字特征进行归一化处理，转成数组并以txt形式保存。

参数设置：

jsonpath：静态特征json文件的路径

csvpath：形成csv文件的路径

arrpath：形成的数组文件的路径  

feaList：特征列表

调用方法：

JsonToCSV(csvpath,jsonpath,feaList)

getArr(csvpath,arrpath)

### 2.2 Bert编码

**GetNewsCode.py：**利用Google预训练好的模型，对抽取的新闻文本进行编码，填充至定长之后，以csv形式保存。

参数设置：

bertpath：Google预训练好的模型的保存路径

jsonpath：新闻文本的json文件路径

newsdirpath：将每一条新闻编号后形成的数组文件保存的目录

padnewsdirpath：将编码好的数组文件填充至定长的新数组文件的保存目录

csvpath：拼接好的所有样本的新闻编码csv文件的保存路径

调用方法：

BertCode(bertpath,jsonpath,newsdirpath) 

getPadCode(newsdirpath,padnewsdirpath)

getNewsCodeCsv(padnewsdirpath,csvpath,get_max_length(newsdirpath))

### 2.3 数据归一化

**TimeSeqProcess.py**：处理时间序列，包括特征的拼接，序列时间的跨度选择，数据的归一化处理，产生模型的输入输出数组。

参数设置：

csvpath1：利润序列json文件的路径

csvpath2：现金序列json文件的路径

csvpath3：指标序列json文件的路径

csvpath4：外部特征序列json文件的路径

csvpath12_19：不包括新闻特征的12-19年的时间序列csv文件

csvpath13_20：不包括新闻特征的13-20年的时间序列csv文件

arrpath12_19：不包括新闻特征的12-19年的时间序列数组txt文件

arrpath13_20：不包括新闻特征的13-20年的时间序列数组txt文件

startyear：输入数组的时间起始年份

arrYpath：不包含新闻特征的输出数组的txt文件保存的路径

topiclist：输出数组的特征名称

matchpath：新闻样本与时间序列样本的匹配关系的csv文件

arrnewspath：包含新闻特征的时间序列数组文件的保存路径

arrnewsYpath：包含新闻特征的输出数组的txt文件保存的路径

del_arrpath：删除某个特征后的输入数组txt文件保存的路径

del_topic：删除的特征，为“TimeSeq”，“Environment”，“News”

调用方法：

getAllCsv(csvpath1,csvpath2,csvpath3,csvpath4,csvpath12_19,startyear)

getarr(csvpath12_19,arrpath12_19)

getarrY(csvpath13_20,arrYpath,topiclist)

newsSeqconcat(csvpath12_19,arrpath12_19,matchpath,arrnewspath)

getNewsSeq_Y(arrYpath,matchpath,arrnewsYpath)

delPartCode(arrpath12_19,del_arrpath,del_topic)