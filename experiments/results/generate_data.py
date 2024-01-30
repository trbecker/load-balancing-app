#!/usr/bin/python
import pandas as pd
import sqlite3
import sys


def aggregated(data):
    data = data[['tu', 'LATENCY']][data['RESULT'] == 1].groupby('tu').mean()
    data.to_csv(exp + '/aggregated.csv')

def accepted(data):
    predata = data[['tu', 'GNB']][data['RESULT'] == 1]
    finaldata = predata.groupby(['tu']).count()
    finaldata.to_csv(exp + '/accepted.csv')

def denied(data):
    predata = data[['tu', 'GNB']][data['RESULT'] == 0]
    finaldata = predata.groupby(['tu']).count()
    finaldata.to_csv(exp + '/denied.csv')

def accepted_per_gnb(data):
    for i in range(1, 7):
        predata = data[['tu', 'GNB']][data['RESULT'] == 1]
        finaldata = predata[predata['GNB'] == f'gnb{i}'].groupby(['tu']).count()
        finaldata.to_csv(exp + f'/accepted_gnb{i}.csv')
    
def denied_per_gnb(data):
    for i in range(1, 7):
        predata = data[['tu', 'GNB', 'RESULT']][data['RESULT'] == 0]
        finaldata = predata[predata['GNB'] == f'gnb{i}'].groupby(['tu']).count()
        finaldata.to_csv(exp + f'/denied_gnb{i}.csv')

for exp in sys.argv[1:]:
    conn = sqlite3.connect(exp + '/experiment.db')

    data = pd.read_sql_query("select unixepoch(timestamp) as tu, gnb, imsi, sinr, latency, result from admissions order by tu", conn)

    data['tu'] = data['tu'] - data['tu'].min()
    data['LATENCY'] = data['LATENCY'] / 1000000
    
    aggregated(data)
    accepted(data)
    denied(data)
    accepted_per_gnb(data)
    denied_per_gnb(data)