from math import e
import os
import sys
import csv
from xlsxwriter import worksheet
from xlsxwriter.workbook import Workbook

conferences=["AAAI",
"CVPR",
"ICCV",
"ECCV",
"ICLR",
"ICML",
"IJCAI",
"NIPS",]

workbook=Workbook("Collector.xlsx")
total=workbook.add_worksheet("Total")
count=0
for i,con in enumerate(conferences):
    sheet=workbook.add_worksheet(con)
    papers=[]
    print("NAME: ",con)
    with open(con+".csv","r",encoding="utf-8") as f:
        reader=csv.reader(f)
        try:
            for r,row in enumerate(reader):
                if not row or not len(row[0]): continue
                for c,cell in enumerate(row):
                    sheet.write(r,c,cell)
                    total.write(count,c,cell)
                count+=1
        except BaseException as e:
            print("ERROR in {},{}: {}".format(r,c,repr(e)))
workbook.close()
