# ForestExplorer
> written by panzy.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8.5-red"/>
  <img src="https://img.shields.io/badge/pytorch-1.6.0-yellow"/>
  <img src="https://img.shields.io/badge/Anaconda-4.8.3-blue"/>
  <img src="https://img.shields.io/badge/docs-English-green"/>
  <img src="https://img.shields.io/badge/Bert-unknown-purple"/>
</p>

ForestExplorer 是完全基于python语言开发的，基于企业内部、行业市场外部特征进行发展预测的数据分析框架。使用 Anaconda (4.8.3) 和 pip (20.1.1) 管理第三方包。



## 0. Content

本节将对我们的工作作简要描述，根据数据处理的工作流程，分为以下三个模块：

- [特征分析框架](#tezhengfenxi)
  - [网络爬虫](#spider)

- [策略编码器](#encoding)
  - [fd]() 
- [序列拟合模型](#model)
  - [Baseline](#baseline)



## 1. 特征分析框架

特征分析框架主要完成以下工作：数据爬取、数据抽取。



### 1.1 数据爬取

实验中出于对行业的外部环境特征分析的需要，对高新科技门户网站的文本内容进行规则框架内、有限度的爬取，各网站内容详情请见[虎嗅网](https://www.huxiu.com/)，[199IT](http://www.199it.com/)，[36氪](https://36kr.com/)，[雷锋网](https://www.leiphone.com/)，[科学世界网](http://www.twwtn.com)，[维科网](https://www.ofweek.com)。



**爬虫开发环境**：以下为前期网站爬取过程中所使用的 python 第三方包：

|    Packages    | Version |
| :------------: | :-----: |
|    requests    | 2.24.0  |
|      bs4       |  0.0.1  |
| beautifulsoup4 |  4.9.1  |
|      lxml      |  4.5.1  |
|  APScheduler   |  2.1.2  |


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

- fd



**数据抽取**：



