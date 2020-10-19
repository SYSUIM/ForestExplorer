# ForestExplorer
> written by panzy.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8.5-red"/>
  <img src="https://img.shields.io/badge/pytorch-1.6.0-yellow"/>
  <img src="https://img.shields.io/badge/Anaconda-4.8.3-blue"/>
  <img src="https://img.shields.io/badge/docs-English-green"/>
  <img src="https://img.shields.io/badge/Transformer-2.11.0-purple"/>
</p>

ForestExplorer 是完全基于python语言开发的，基于企业内部、行业市场外部特征进行发展预测的数据分析框架。使用 Anaconda (4.8.3) 和 pip (20.1.1) 配置代码环境。

<br><br>

## 0. Content

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
特征分析框架主要完成以下工作：[网络爬虫](#spider)、[数据抽取](#dataextraction)。

<br>

### <span id="spider">1.1 网络爬虫</span>

实验中出于对行业的外部环境特征分析的需要，对高新科技门户网站的文本内容进行规则框架内、有限度的爬取，各网站内容详情请见[虎嗅网](https://www.huxiu.com/)，[199IT](http://www.199it.com/)，[36氪](https://36kr.com/)，[雷锋网](https://www.leiphone.com/)，[科学世界网](http://www.twwtn.com)，[维科网](https://www.ofweek.com)。

<br>

**爬虫开发环境**

---
以下为前期网站爬取过程中所使用的 python 第三方包：

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

使用 `pip install -r ./SpiderRequirements.txt` 命令完成环境安装，或者可以使用我们提供的 `requirements.txt` 使用相同指令直接实现完整框架环境的安装。

<br>

**爬虫代码**：

---
不同网站结构不同，我们针对每个网站编写了专门的爬虫脚本，在装有以上第三方包的python环境下即可直接运行，请确保文件保存路径符合系统路径规则。

- [*HuXiu Spider*](Spiders/HuXiu/Spider.py)：虎嗅网爬虫提供了两种爬取方式，分别是流式爬取和关键词爬取。其中，流式爬取主要由方法`crawlJob_Stream` 实现，关键词爬取由 `crawljob_search` 实现，由于流式爬取文章数的限制，现只默认调用关键词爬取方法。该爬虫提供了断点续爬功能，请创建 `./hotKeyword.txt` 文件作为关键词爬取的断点记录文件，或使用本项目提供的模版 [*hotKeyword.txt*](Spiders/HuXiu/hotKeyword.txt) 来实现该功能。此外，为避免高强度访问网站，设置了定时爬取功能，默认间隔时间为30分钟。
  - 运行 `python create.py ` 生成断点配置模板
  - 运行 `python Spider.py` 进行网页爬取，并保存到指定路径
- [*36kr Spider*](Spiders/36kr/36kr_spider.py)：36氪爬虫通过手动获取特定关键词以及callback编码，获取相应关键词的文章。使用时当对网站服务器访问量过大，会受到网站访问限制。
  - 运行 `python 36kr_spider.py` 进行网页爬取，并保存到指定路径
- [*199IT Spider*](Spiders/199IT/199_spider.py)：199IT爬虫通过自主选取关键词，通过 `get_id` 获取相应文章对应的id列表，写入文件，然后通过 `get_articles` 获取相应id的文章内容保存到path中。当访问量过大时，会受到访问限制。
  - 运行 `python 199_spider.py` 进行网页爬取，并保存到指定路径
- [*Mckinsey Spider*](Spiders/mckinsey/mckinsey_spider.py)：mckinsey爬虫通过租住选择关键词，爬取对应文章保存到path中。当访问量过大时，会受到访问限制。
  - 运行 `python mckinsey_spider.py` 进行网页爬取，并保存到指定路径
- [*Kexueshijie Spider*]()：用 `requests` 库爬取文本，对Unicode进行解码，再删除HTML的标签和“\“符号，使文本成为可转化为json的字符串。再将字符串转为json格式，获取新闻的标题、id、时间和内容，并写入txt文件中保存。
  - 运行 `python kexueshijie_spider.py`进行网页爬取，并保存到指定路径

<br>

### <span id="dataextraction">1.2 数据抽取</span>
实验中对赛事方给出数据集进行抽取工作，从26个数据集中选取相关度较高的数据类型输入模型分析。该部分将简要介绍如何从数据集中抽取数据。

<br>

[**FileProcess.py**](dataProcess/FlieProcess.py)

---
从26个json文件中抽取特征，处理成为一个静态特征的json文件。

- 参数设置：

|    Parameter    | Description |
| :------------: | :-----: |
|    filelist    |  需要进行特征抽取的json文件列表，第一个必须是 `01工商注册.json` |
|     typelist       |  每个json文件对应的处理函数，分别有text, number, boolean三种，text直接保留样本特征内容，number将统计文件中样本某个特征的出现次数，boolean统计样本是否含有某个特征  |
| featurelist |  每个json文件中要抽取的特征 |
|     jsonlist       |  每个json文件中要抽取的特征  |

<br>

- 调用方法：`FileProcess(filelist,typelist,featurelist,jsonlist)`

<br>

[**TimeSeqSpider.py**](dataProcess/TimeSeqSpider.py)

---
通过公司的证券代码，爬取巨潮资讯上相应公司的基本信息，利润序列信息，现金序列信息，指标序列信息，并返回一个json文件。

- 参数设置：

|    Parameter    | Description |
| :------------: | :-----: |
|    companyCodeFile    |  公司证券代码的csv文件 |
|    BaseInfoPath        |  保存基本信息的json文件路径  |
| LiRunPath | 保存利润序列信息的json文件路径  |
|   XianJinPath      |  保存现金序列信息的json文件路径  |
| ZhiBiaoPath | 保存指标序列信息的json文件路径 |

<br>

- 调用方法：
`Spider(companyCodeFile,BaseInfoPath,LiRunPath,XianJinPath,ZhiBiaoPath)`

<br>

[**getExternalCharacteristic.py**](dataProcess/getExternalCharateristic.py)

---
通过爬取国家统计局[https://data.stats.gov.cn/](https://data.stats.gov.cn/)发布的年度数据，得到50个行业的年度报表csv文件，归一化处理外部特征数据，将行业外部特征（行业所得利润）全部转换为该年利润与上一年利润的比值，根据企业所属行业与爬取得到的行业报表进行匹配，得到公司最终行业以及外部特征。

- 参数设置：

| Parameter                  | Description                          |
| -------------------------- | ------------------------------------ |
| IndustryList               | 爬取所得行业的名称列表               |
| csvfilePath                | 爬取所得行业报表csv文件路径          |
| BaseInfoList               | 保存企业行业代码、所属行业信息的列表 |
| Characteristic             | 保存某行业2012-2020年度特征的字典    |
| ExternalCharacteristicDic  | 保存某企业行业代码、外部特征的字典   |
| ExternalCharacteristicList | 保存所有企业行业代码、外部特征的列表 |

- 调用方法:
  - `getBaseInfo()`
  - `getAccelerate(industry)`
  - `getCSV(AccelerateInfo)`

<br>

## <span id="encoding">2. 多元数据策略编码</span>

<br>

### <span id = "onehot">2.1 One-hot编码</span>
针对数据集中的结构化非数据特征，根据one-hot编码规则进行转换。

<br>

[**Json2Onehot.py**](dataProcess/Json2Onehot.py)

---
将静态json的文件转为csv文件，对其中的离散型文字特征进行one-hot编码，对所有的数字特征进行归一化处理，转成数组并以txt形式保存。

- 参数设置：

|    Parameter    | Description |
| :------------: | :-----: |
|    jsonpath    | 静态特征json文件的路径  |
|    csvpath     |  形成csv文件的路径  |
| arrpath |  形成的数组文件的路径 |
|     feaList    |  特征列表  |

<br>

- 调用方法：
  - `JsonToCSV(csvpath,jsonpath,feaList)`
  - `getArr(csvpath,arrpath)`

<br>

### <span id = "bert">2.2 Bert编码</span>

<br>

[**GetNewsCode.py**](dataProcess/GetNewsCode.py)

---
利用Google预训练好的模型，对抽取的新闻文本进行编码，填充至定长之后，以csv形式保存。

- 参数设置：

|    Parameter    | Description |
| :------------: | :-----: |
|    bertpath    | Google预训练好的模型的保存路径  |
|    jsonpath     |  新闻文本的json文件路径  |
| newsdirpath |  将每一条新闻编号后形成的数组文件保存的目录 |
| padnewsdirpath    |  将编码好的数组文件填充至定长的新数组文件的保存目录  |
| csvpath | 拼接好的所有样本的新闻编码csv文件的保存路径 |

<br>

- 调用方法：
  - `BertCode(bertpath,jsonpath,newsdirpath)`
  - `getPadCode(newsdirpath,padnewsdirpath)`
  - `getNewsCodeCsv(padnewsdirpath,csvpath,get_max_length(newsdirpath))`

<br>

### <span id = "datanormalization">2.3 数据归一化</span>

<br>

[**TimeSeqProcess.py**](dataProcess/TimeSeqProcess.py)

---
处理时间序列，包括特征的拼接，序列时间的跨度选择，数据的归一化处理，产生模型的输入输出数组。

- 参数设置：

|    Parameter    | Description |
| :------------: | :-----: |
|  csvpath1    | 利润序列json文件的路径  |
|  csvpath2     |  现金序列json文件的路径  |
| csvpath3 |  指标序列json文件的路径 |
| csvpath4 |  外部特征序列json文件的路径  |
| csvpath12_19 | 不包括新闻特征的12-19年的时间序列csv文件 |
| csvpath13_20 | 不包括新闻特征的13-20年的时间序列csv文件 |
| arrpath12_19 | 不包括新闻特征的12-19年的时间序列数组txt文件 |
| arrpath13_20 | 不包括新闻特征的13-20年的时间序列数组txt文件 |
| startyear | 输入数组的时间起始年份 |
| arrYpath | 不包含新闻特征的输出数组的txt文件保存的路径 |
| topiclist | 输出数组的特征名称 |
| matchpath | 新闻样本与时间序列样本的匹配关系的csv文件 |
| arrnewspath | 包含新闻特征的时间序列数组文件的保存路径 |
| arrnewsYpath | 包含新闻特征的输出数组的txt文件保存的路径 |
| del_arrpath | 删除某个特征后的输入数组txt文件保存的路径 |
| del_topic | 删除的特征，为“TimeSeq”，“Environment”，“News” |

<br>

- 调用方法：
  - `getAllCsv(csvpath1,csvpath2,csvpath3,csvpath4,csvpath12_19,startyear)`
  - `getarr(csvpath12_19,arrpath12_19)`
  - `getarrY(csvpath13_20,arrYpath,topiclist)`
  - `newsSeqconcat(csvpath12_19,arrpath12_19,matchpath,arrnewspath)`
  - `getNewsSeq_Y(arrYpath,matchpath,arrnewsYpath)`
  - `delPartCode(arrpath12_19,del_arrpath,del_topic)`