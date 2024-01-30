#!/usr/bin/python
import sys
import sqlite3

db = sqlite3.connect(sys.argv[2])
cur = db.cursor()

with open(sys.argv[1], 'r') as fp:
    for line in fp.readlines():
        imsi, gnb, latency, sinr, result = line.split(',')
        sql = f"""update admissions set 
                   latency = {latency}, sinr = {sinr}
                    where imsi = "{imsi}" and gnb = "{gnb}" and result = {1 if result else 0};"""
        print(sql)
        cur.execute(sql)
db.commit()