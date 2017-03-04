# MCMResult
数模美赛成绩抓取、分析工具
## 一、美赛简介
> 美国大学生数学建模竞赛（MCM/ICM）是唯一的国际性数学建模竞赛，也是世界范围内最具影响力的数学建模竞赛，为现今各类数学建模竞赛之鼻祖。MCM/ICM 是 Mathematical Contest In Modeling 和 Interdisciplinary Contest In Modeling 的缩写，即“数学建模竞赛”和“交叉学科建模竞赛”。MCM 始于 1985 年，ICM 始于 2000 年，由 COMAP（the Consortium for Mathematics and Its Application，美国数学及其应用联合会）主办，得到了 SIAM，NSA，INFORMS 等多个组织的赞助。MCM/ICM 着重强调研究问题、解决方案的原创性、团队合作、交流以及结果的合理性。

——摘自百度百科

美赛的奖项设置如下：

|全称|翻译|简称|  
|---|---|---|  
|Outstanding|特等奖|O奖|  
|Finalist|特等提名奖|F奖|  
|Meritorious Winner|一等奖|M奖|  
|Honorable Mention|二等奖|H奖|  
|Successful Participant|三等奖|SP奖|  
|Unsuccessful|不成功参赛|U奖|  

每年的美赛都会有来自各大高校的上万支队伍参加，其中中国队伍占80%以上。
本人参加了2016年的美赛，仅获得H奖，非常遗憾。
参赛后非常好奇，本校内其他队伍成绩如何？参加美赛的学校如此众多，各学校的参赛规模都有多大？获奖比例如何？
于是就写了本项目——一个通过爬虫抓取美赛数据，进行美赛成绩统计分析的工具。

## 二、项目思路
每年的美赛成绩公布后，各队伍可以在如下的网址下载队伍证书：`'http://www.comap-math.com/mcm/2016Certs/00000.pdf'`。
其中'2016'可以修改为其他的年份，'00000'是五位的队伍号。

证书的内容是这样的：

![certificate](https://github.com/zhangpc123/MCMResult/raw/master/doc/image/certificate.png)

可以看到里面包含学校、指导教师、队员、奖项等信息，我们可以采集这些公开的证书，进行一定的处理得到可用的格式化数据。
处理则分两步：首先提取pdf文件中的文本；然后使用这样一条正则表达式：
```python
pattern = re.compile(r'[\s\S]*Be It Known That The Team Of(?P<name>[\s\S]*)With Faculty Advisor(?P<advisor>[\s\S]*?)Of'
                     r'(?P<school>[\s\S]*)Was Designated As(?P<award>[\s\S]*)Administered by[\s\S]*')
```
匹配出所需信息。

接下来将上面匹配出的name、advisor、school、award信息格式化写入csv，再使用ipython notebook读取csv便可以进一步分析了。

综上所述，本项目分为如下几步：

1. 抓取12466支参赛队的获奖证书pdf文件  
2. 使用`pdftotext`工具提取所有pdf文件中的文字，存储为txt文件  
3. 读取txt文件，使用正则式提取出name、advisor、school、award四项信息格式化写入csv
4. 使用ipython notebook进行数据分析

## 三、依赖
本项目在ubuntu14.04上构建，依赖如下工具：
- python3.4.3  
使用如下命令安装：
`sudo apt-get install python3`
- python pandas0.18.0库  
使用如下命令安装：
`pip3 install pandas`  
若提示找不到pip3命令，请首先安装pip3：`sudo apt-get install pip3`
- jupyter notebook4.1.0  
使用如下命令安装：`pip3 install ipython`
- pdftotext0.24.5  
使用如下命令安装：`sudo apt-get install pdftotext`

## 四、模块说明
### 模块
|文件|说明|  
|---|---|  
|scratch.py|抓取文件相关函数，包含多线程批量抓取、单线程单独抓取等|  

### 可执行文件
|文件|说明|  
|---|---|  
|work.py|抓取pdf文档到当前目录下的'pdf'目录|  
|list_state.py|统计当前抓取状态，统计信息包含抓取正常、404、其他异常三种状态|  
|extractdata.py|从抓取好的pdf文件提取出txt存储到'text'目录，然后提取所有txt文件内的信息格式化写入data.csv|  

### notebook
|文件|说明|  
|---|---|  
|anylysis.ipynb|读取data.csv建立DataFrame进行数据分析|

### 目录
|目录|说明|  
|---|---|  
|pdf|存储抓取好的pdf证书文件|  
|text|从pdf提取出的txt文本|  
|state|存储各队伍证书的抓取状态，为方便多进程使用，为每10000i~10000(i+1)队号范围单独建立一个状态文件|  

## 五、示例
### 首先运行work.py抓取数据
2016年美赛队号范围是42064～54840，中间有队号未使用，这是人工干预手动测的，后续会考虑加入自动化的步骤。

由于证书网站网速状况不是很好，此步可能会经历较长时间。

执行完此步，可以看到pdf目录内已经存在很多的pdf文件了。
### 运行extractdata.py提取数据
执行完此步，可以发现txt文件被成功提取到text目录。
同时项目根目录下新增一个data.csv文件，这便是格式化的全部队伍的数据了，
各列含义为：

|team|advisor|award|name|school|  
|-----|-----|-----|-----|-----|  
|队号|指导老师|奖项|三位队员名字|学校|  

2016年的全部数据data.csv已经上传到本仓库，大家可以将其导入excel或数据库进行独立分析。
### 使用jupyter notebook打开anylysis.ipynb
anylysis.ipynb是给出的示例分析代码，可直接在线查看代码及结果。
其中统计了各学校的参赛队伍数和获奖比例等信息，同时可以根据队员名、教练名、学校、奖项等进行模糊查询。

非常有意思的一个结果是下面这张图：

![rate](https://github.com/zhangpc123/MCMResult/raw/master/doc/image/rate.png)

图中统计的是参赛队伍大于30支的学校的获奖比例，All一列是参赛队伍总数，排名按照M奖以上的比例。
类比派出110支队伍的北大和派出160支队伍的浙大，可以发现西安三校在数模竞赛上的实力非常强，这和学校的传统和对比赛的重视程度是分不开的。
