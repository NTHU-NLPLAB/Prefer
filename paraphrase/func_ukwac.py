#!/usr/bin/env python
# -*- coding: utf8 -*-
import sqlite3
from datetime import datetime


stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

con_sent = sqlite3.connect("UkwacSentNew.db3")
cur_sent = con_sent.cursor()

# CREATE TABLE Invert_UkWac1 ( Word , SentNo , Posi );
# CREATE INDEX Idx_Word on Invert_UkWac1(Word);
con_inv = sqlite3.connect("UkWacInvertedTable.db")
cur_inv = con_inv.cursor()

con_sent.text_factory = str
con_inv.text_factory = str


def get_Contentword(phrase):
    phrase = set(phrase.split())
    cnt_word = phrase.intersection(stopwords)
    return cnt_word


def get_Sent_by_phrase(phrase):
    cnt_words = get_Contentword(phrase)
    cur_inv.execute("SELECT A.Sent , A.Lemma , A.POS FROM UkWac1 A , Invert_UkWac1 B WHERE A.Sn=B.SentNo AND B.Word=?", (word,))


def get_Sent(word):
    # cur_inv.execute( "SELECT A.Sent , A.Lemma , A.POS FROM UkWac1 A , Invert_UkWac1 B WHERE A.Sn=B.SentNo AND B.Word=?" , ( word, ) )
    # results = cur_inv.fetchall()
    # for line in results:
    # 	print(line)
    cur_inv.execute("SELECT SentIndex FROM Invert_UkWac1 WHERE Word=?", (word,))
    results = [l[0] for l in eval(cur_inv.fetchall()[0][0])]
    sents = []
    for sn in results:
        sn = int(sn)
        cur_sent.execute("SELECT Sent FROM UkWac1 WHERE Sn=?", (sn,))
        sents.append(cur_sent.fetchall()[0][0])
    return sents
    # sent_lst = eval(results[0])


tstart = datetime.now()

print(len(get_Sent("role")))

tend = datetime.now()

print("Finish index in " + str((tend-tstart).seconds))
