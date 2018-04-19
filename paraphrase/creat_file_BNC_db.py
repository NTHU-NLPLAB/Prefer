#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os

con = sqlite3.connect("BNC_Sent_POS.db")

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

cur = con.cursor()

lo = 5000000
c = 0


db_root = "BNC_SENT/"


level1 = 0
level2 = 0
level3 = 0


def get_path(sn):
    level3 = sn % 200
    level2 = (sn/200) % 200
    level1 = (sn/40000) % 200
    return [str(level1), str(level2), str(level3)]
    # return str(level1)+"/"+str(level2)+"/"+str(level3)


def get_sn(path):
    level1, level2, level3 = path.split("/")
    return int(level3) + int(level2)*200 + int(level1)*40000


con.text_factory = str
db_dir1 = os.listdir(db_root)

for Sn, Sent, POS, Shallow in cur.execute("SELECT Sn, Sent, POS_tag , Shallow FROM Sent"):
    path = get_path(Sn)
    for i in range(len(path)-1):
        # print(path[:i])
        if path[i] not in os.listdir(db_root + "/".join(path[:i])):
            # print(db_root + "/".join( path[:i+1]))
            os.mkdir(db_root + "/".join(path[:i+1]))
    fout = open(db_root + "/".join(path), "w")
    fout.write(Sent + "\n" + POS + "\n" + Shallow)
    fout.close()
    c += 1
    if c % 50000 == 0:
        print(str(float(c)*100/lo)[:4] + "%")
