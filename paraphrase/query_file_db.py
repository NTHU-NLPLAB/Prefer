#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
from datetime import datetime

con = sqlite3.connect("UkWacInvertedTable.db")

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

cur = con.cursor()
con.text_factory = str

db_root = "SENTDB/"

def get_path( sn ):
	level3=sn % 300
	level2=(sn/300) % 300
	level1=(sn/90000) % 300
	return [ str(level1) , str(level2) , str(level3) ]
	#return str(level1)+"/"+str(level2)+"/"+str(level3)

def get_sn( path ):
	level1, level2, level3 = path.split("/")

	return int(level3) + int(level2)*300 + int(level1)*90000  

tstart = datetime.now()

inv_lst = set([])
cnt_word_lst = [ "abandon" , "punishment"  ]

for word in cnt_word_lst:
	cur.execute("SELECT SentIndex FROM Invert_UkWac1 WHERE Word=?", ( word , ) )
	results =  [ l[0] for l in eval(cur.fetchall()[0][0]) ]
	#print results

	if not inv_lst:
		inv_lst = set( results )
	else:
		inv_lst = inv_lst.intersection( set(results) ) 

#print len(inv_lst)
inv_lst = list(inv_lst)
inv_lst.sort()


sent_lst = []

for sn in inv_lst:
	path = get_path( sn )
	sent_lst.append(  [ line.strip() for line in file( db_root + "/".join( path )  , "rU") ]   )

print sent_lst
print len(sent_lst)
tend = datetime.now()

print "Finish index in " + str( (tend-tstart).seconds )

		
		
	


