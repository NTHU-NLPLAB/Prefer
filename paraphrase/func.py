# -*- coding: UTF-8 -*-                                                                                                            

#=========================  Import libs  ================================
import sqlite3
import math
import os
import subprocess
import func
#========================= Def function  ================================
en_table = ['JA', 'IN', 'SU', 'UF', 'TE', 'EW', 'PA', 'AC', 'HE', 'HO', 'MU', 'JO', 'IZ', 'QA', 'MI', 'FA', 'ME', 'NI', 'IH', 'IR', 'UJ', 'OD', 'TO', 'AQ', 'EH', 'UH', 'DI', 'NA', 'G', 'NE', 'EC', 'VA', 'D', 'AM', 'EP', 'LU', 'TI', 'QE', 'UG', 'IP', 'DE', 'OC', 'A', 'OK', 'UW', 'KO', 'OZ', 'I', 'QI', 'SI', 'GO', 'OR', 'OY', 'ER', 'RO', 'AX', 'DO', 'RE', 'SO', 'T', 'IQ', 'UR', 'IF', 'L', 'UL', 'M', 'IM', 'V', 'OT', 'AN', 'AT', 'UC', 'IW', 'JI', 'EY', 'EN', 'AD', 'EF', 'UX', 'DU', 'JE', 'B', 'VU', 'SE', 'KE', 'OH', 'J', 'LE', 'UV', 'O', 'IT', 'GU', 'IB', 'VE', 'RU', 'P', 'EB', 'RA', 'HU', 'PE', 'PO', 'HA', 'FE', 'FU', 'OV', 'IL', 'UT', 'OB', 'ON', 'E', 'LA', 'IV', 'Q', 'UD', 'LO', 'RI', 'FI', 'UQ', 'ES', 'KA', 'EJ', 'LI', 'SA', 'UZ', 'AP', 'OW', 'UP', 'AV', 'US', 'AB', 'AG', 'NO', 'OG', 'AW', 'QU', 'EX', 'KI', 'GI', 'VI', 'GA', 'F', 'MA', 'AF', 'UY', 'EK', 'AS', 'K', 'AJ', 'AK', 'AZ', 'FO', 'JU', 'MO', 'CA', 'OQ', 'AR', 'IS', 'PI', 'EM', 'C', 'IJ', 'HI', 'N', 'OF', 'UN', 'ET', 'UM', 'CU', '0', 'IG', 'OX', 'DA', 'AY', 'OM', 'OJ', 'BE', 'BO', 'CO', 'QO', 'IK', 'KU', 'UK', 'WA', 'TU', 'W', 'UB', 'S', 'IY', 'NU', 'PU', 'R', 'CI', 'BU', 'IX', 'ID', 'EL', 'BI', 'BA', 'EZ', 'EQ', 'GE', 'CE', 'AH', 'VO', 'EV', 'ED', 'EG', 'H', 'TA', 'OP', 'IC', 'U', 'OS', 'OL', 'AL' , 'OTHERS']
cnt_uni = 36240520
cnt_bi = 218984273

def hash_func( s ):
	
	if s[:2].upper() in en_table:
		return s[:2].upper()
	elif s[0].upper() in en_table:
		return s[0].upper()
	else:
		return 'OTHERS'

def cooccurence_sent( word_lst1 , word_lst2 ):
	sent_lst1 = set([ w[0] for w in word_lst1 ])
	sent_lst2 = set([ w[0] for w in word_lst2 ])
	inter = sent_lst1.intersection( sent_lst2 )
	return inter


def find_bnc_sent( word , limit=0):
	con_bnc = sqlite3.connect('Inverted_table.db')
	con_bnc_sent = sqlite3.connect('BNC_Sent_POS.db')
	
	cur_bnc = con_bnc.cursor()
	cur_bnc_sent = con_bnc_sent.cursor()
	
	
	table_name = "en_" + hash_func( word )
	if limit==0:
		cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? ORDER BY Sent_no" % table_name , ( word , ) )
	else:
		cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? ORDER BY Sent_no LIMIT ?" % table_name , ( word , limit ) )
	results = cur_bnc.fetchall()
	
	bnc_ex = []
	for (r,) in results:
		#print r
		cur_bnc_sent.execute( "SELECT * FROM Sent WHERE Sn = ?" , (r-1,) )
		bnc_ex += cur_bnc_sent.fetchall()
	
	con_bnc.close()
	cur_bnc_sent.close()
	return bnc_ex

def find_bnc_sent_twoWord( word1 , word2 ):
	
	con_bnc = sqlite3.connect('Inverted_table.db')
	con_bnc_sent = sqlite3.connect('BNC_Sent_POS.db')
	
	cur_bnc = con_bnc.cursor()
	cur_bnc_sent = con_bnc_sent.cursor()
	
	table_name1 = "en_" + hash_func( word1 )
	table_name2 = "en_" + hash_func( word2 )
	
	cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? ORDER BY Sent_no" % table_name1 , ( word1 , ) )
	results_1 = cur_bnc.fetchall()
	
	cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? ORDER BY Sent_no" % table_name2 , ( word2 , ) )
	results_2 = cur_bnc.fetchall()
	if not ( results_1 and results_2 ):
		return None
	

	co_sent_lst = cooccurence_sent( results_1 , results_2 )
	if not co_sent_lst:
		return None
	#print co_sent_lst
	#for s in co_sent_lst:
	result = []
	for s in co_sent_lst:
		cur_bnc_sent.execute( "SELECT Sent FROM Sent WHERE Sn = ?" , ( s-1 , ) )
		sents = cur_bnc_sent.fetchall()
		for s in sents:
			result.append( s[0] )
	
	
	
	
	
	con_bnc.close()
	con_bnc_sent.close()
	return result

def find_bnc_twoWord_by_dist( word1 , word2 , dist ):
	
	con_bnc = sqlite3.connect('Inverted_table.db')
	con_bnc_sent = sqlite3.connect('BNC_Sent_POS.db')
	
	cur_bnc = con_bnc.cursor()
	cur_bnc_sent = con_bnc_sent.cursor()
	
	table_name1 = "en_" + hash_func( word1 )
	table_name2 = "en_" + hash_func( word2 )
	
	cur_bnc.execute( "SELECT Sent_no,Word_posi FROM %s WHERE enWord = ? ORDER BY Sent_no" % table_name1 , ( word1 , ) )
	results_1 = cur_bnc.fetchall()
	
	cur_bnc.execute( "SELECT Sent_no,Word_posi FROM %s WHERE enWord = ? ORDER BY Sent_no" % table_name2 , ( word2 , ) )
	results_2 = cur_bnc.fetchall()
	if not ( results_1 and results_2 ):
		return None
	
	
	r1_sents = dict( results_1 )
	r2_sents = dict( results_2 )
	co_sent_lst = set( r1_sents.keys() ).intersection( set( r2_sents.keys() ) )
	if not co_sent_lst:
		return None
	
	new_co_sent = []
	for sent_no in co_sent_lst:
		words_dist = abs(r2_sents[ sent_no ] - r1_sents[ sent_no ])
		if words_dist == dist:
			new_co_sent.append( sent_no )

	#print co_sent_lst
	#for s in co_sent_lst:
	result = []
	for s in co_sent_lst:
		cur_bnc_sent.execute( "SELECT Sent FROM Sent WHERE Sn = ?" , ( s-1 , ) )
		sents = cur_bnc_sent.fetchall()
		for s in sents:
			result.append( s[0] )
	
	
	
	
	
	con_bnc.close()
	con_bnc_sent.close()
	return result

#print find_bnc_twoWord_by_dist("play","role",4)
#print find_bnc_sent("lest")[:10]
def count_cooccur( word1 , word2 ):
	con_bnc = sqlite3.connect('Inverted_table.db')
	
	cur_bnc = con_bnc.cursor()
	
	
	table_name1 = "en_" + hash_func( word1 )
	table_name2 = "en_" + hash_func( word2 )
	
	cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? " % table_name1 , ( word1 , ) )
	results_1 = cur_bnc.fetchall()
	
	cur_bnc.execute( "SELECT Sent_no FROM %s WHERE enWord = ? " % table_name2 , ( word2 , ) )
	results_2 = cur_bnc.fetchall()
	if not ( results_1 and results_2 ):
		return None
	

	co_sent_lst = cooccurence_sent( results_1 , results_2 )
	con_bnc.close()
	
	if not co_sent_lst:
		return int(0)
	return len( co_sent_lst )

def count_word( word ):
	con_bnc = sqlite3.connect('Inverted_table.db')
	
	cur_bnc = con_bnc.cursor()
	table_name1 = "en_" + hash_func( word )
	
	cur_bnc.execute( "SELECT count(*) FROM %s WHERE enWord = ? " % table_name1 , ( word , ) )
	
	return int(cur_bnc.fetchall()[0][0])

def eval_MI( word1 , word2 ):
	co_ocr = math.log( count_cooccur( word1 , word2 )/float(cnt_bi) )
	uni1 = math.log ( count_word( word1 )/float(cnt_uni) )
	uni2 = math.log ( count_word( word2 )/float(cnt_uni) )
	if not co_ocr:
		return -999
	mi = co_ocr-(uni1+uni2)
	return mi

def beauty_print( lst , cols , sep=":" , line_sep="\\n" ):
	col = "\"%s\".join( [ " % line_sep
	col += str(" + \"" + sep + "\" + ").join( ["str(c[" + str(ent) + "])" for ent in cols ])
	col += " for c in lst ] )"
	print eval(col)

	
def collocation_postag( word1 , word2 ):
	#Sn INTEGER PRIMARY KEY ASC,word1,word2,syn1,syn2,MI,freq
	con = sqlite3.connect("BNC_Skip_Bigram_Index.db3")
	cur = con.cursor()
	cur.execute( "SELECT syn1,syn2 FROM BNC_Skip_Bigram WHERE word1=? and word2=? ORDER BY freq DESC LIMIT 1" , ( word1 , word2 ) )
	result = cur.fetchall()
	if result:
		return result[0]
	else:
		return ["N/A","N/A"]



def progress_count( count , totalCount , step = 1000):

	if count%step==0:
		print str((float(count)/totalCount)*100)[:5] + "%"
	return count + 1	
	
	
def geniatagger( sent ):
	nowdir = os.getcwd()
	os.chdir("/media/win2/NLP_DATA/TOOLS/geniatagger-3.0.1")
	shrpoc = subprocess.Popen( ' echo "' + sent + '" | ./geniatagger ', shell=True, stdout=subprocess.PIPE )
	ostr = shrpoc.stdout.read()
	os.chdir( nowdir )
	
	
	#this    this    DT      B-NP    O
	
	pos_lst = []
	for line in ostr:
		line = line.split()
		print line
		pos_lst.append(line[2])
		
	
	
	return pos_lst
#=========================     main      ================================

		

