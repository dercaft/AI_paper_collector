# AI_paper_collector
A simple, lightweight, easy use pythonic AI Conference paper collector.
## Too long to read:
Open Manual_total.xlsx, all crawled papers are listed in there.
### Guidence for effcient search in EXCEL:
- [Tutorial of Excel Advance Filter](https://support.microsoft.com/en-us/office/filter-by-using-advanced-criteria-4c9222fe-8529-4cd7-a898-3f16abdff32b)
- [百度知道](https://jingyan.baidu.com/article/295430f1e438be0c7e0050e9.html)

```
与：条件在同一行
或： 条件在不同行
不包含： <>*包含字符*
包含： *包含字符* 
注意：条件不加引号
```

## Collected Conferences& Journals
### Conferences

| Conferences    | 2018    | 2019    | 2020    | 2021    | 2022 |
| -------------- | ------- | ------- | ------- | ------- | ---- |
| AAAI &#X1F41B; | &#9745; | &#9745; | &#9745; | &#9745; |      |
| CVPR           | &#9745; | &#9745; | &#9745; | &#9745; |      |
| ICCV           | &#9745; | &#9745; | &#9745; | &#9745; |      |
| ECCV           | &#9745; | &#9745; | &#9745; | &#9745; |      |
| ICLR           | &#9745; | &#9745; | &#9745; | &#9745; |      |
| ICML           | &#9745; | &#9745; | &#9745; | &#9745; |      |
| IJCAI          | &#9745; | &#9745; | &#9745; | &#9745; |      |
| NIPS           | &#9745; | &#9745; | &#9745; | &#9745; |      |
|                |         |         |         |         |      |

### Journals

| Journals |      |      |      |
| -------- | ---- | ---- | ---- |
| AI       |      |      |      |
| TPAMI    |      |      |      |
| TNN      |      |      |      |

## Environment:

- Scrapy
- Selenium
- ~~[Peewee](https://github.com/coleifer/peewee) (ORM framework for SQLite)~~

## How to Run

### One Command to get all

We offer a shell script to crawl all Conferences' papers. 

We assuming your start path is this repo's directory.

After your environment is ready, just run:

```shell
cd spider_conference
bash ./crawl.sh
```

CSV files will be created under project path.

If you just want to crawl Specific Conferences' paper, run:

```shell
scrapy crawl <CONFERENCE_NAME>
```

you can find <CONFERENCE_NAME> in crawl.sh

### CSV to XLSX

After collect all conferences, go to project path, run:

```
python csv2xlsx.py
```

and you will get Collector.xlsx, containing all papers.

## Structure:

- Use scrapy to get paper infos from denoted Conference urls, for example title, abstract, etc.
- Save these infos into CSV files, or lightweight sqlite3 database.
- Offer tools to get papers we want from database, convert into excel format (In the furture).

## Develop Resources

This chapter records resources for developing a spider program.

### Spider

- [Xpath入门教程](https://www.runoob.com/xpath/xpath-nodes.html)
- [W3school Xpath](https://www.w3school.com.cn/xpath/index.asp)
- [形象解释Scrapy](https://www.cnblogs.com/ellisonzhang/p/11113277.html)
- [常用库汇总](https://zhuanlan.zhihu.com/p/81944559)
### SQL&SQL ORM
### Website

## BUG?

- Abstract in two record in ECCV.csv is spliced into multiple lines, need manual correction. 

  In csv, find : 

  ```
  angle$ triplet needs to be maintained correctly. For example
  ```

  ```
  ho$. Furthermore
  ```

  to see these two bad records.

- AAAI: collect over 1000 more records than published, indicating that some records are splited in to multiple rows.

- NIPS: when write into csv file, there is some records' chaos.

  ![image-20211117140907657](README.assets/image-20211117140907657.png)

  - Possible Problem:

    Excel encoding should be saved and opened in UTF-8 encoding.

     Content of these record make an error when opening the CSV format file.

## Future
- Finish all listed conferences' spider
- Add sql support
- Create a tiny website, with UI and some search tools.