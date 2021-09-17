# AI_paper_collector
A simple, lightweight, easy use pythonic AI Conference paper collector.
## Eight Conference&Journals 2018-2021:
- [x] AAAI
- [x] CVPR
- [x] ICCV
- [x] ECCV
- [x] ICLR 

- [x] ICML
- [x] IJCAI
- [x] NIPS

## Environment:

- Scrapy
- Selenium
- ~~[Peewee](https://github.com/coleifer/peewee) (ORM framework for SQLite)~~

## How to Use

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

go to project path, run:

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

## BUG

- Abstract in two record in ECCV.csv is spliced into multiple lines, need manual correction. 

  In csv, find : 

  ```
  angle$ triplet needs to be maintained correctly. For example
  ```

  ```
  ho$. Furthermore
  ```

  to see these two bad records.

## Future
- Finish all listed conferences' spider
- Add sql support
- Create a tiny website, with UI and some search tools.