#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sqlite3

import sys

import func_paraphrase
import func_bnc
import sqlite3
from datetime import datetime
import phraseTable
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from simple_tag import simple_pos_dic

# compile results for both parphrase and extended paraphrase
def compile_results( lst , ex_phrase_dic , out_pos_phrase_dic , en_translation_dic ):
	results_lst = []
	for p in lst:
		results_ex_lst = []
		pattern_dic = {}
		ch_ph = ""

		for ex, ( otpos_lst , otpos_dic ) in out_pos_phrase_dic[ p[0] ]:
			ex_pattern_dic = {}	
			if not otpos_lst:
				continue
			
			for ( ( hpos, tpos ) , posfreq ) in otpos_lst:
				if posfreq <= 1:
					continue

				h_ex_lst = []
				t_ex_lst = []
				pat_ex_lst = []
				for ( ( ex_hpos ,ex_tpos ) , exposfreq ) in otpos_dic[ ( hpos, tpos ) ]:
					
					pat_ex_lst.append( ex_hpos + " " + ex + " " + ex_tpos )
					h_ex_lst.append( ( ex_hpos, exposfreq ) )
					t_ex_lst.append( ( ex_tpos, exposfreq ) )
				
				h_ex_lst = func_bnc.count_freq_tuple( h_ex_lst )
				t_ex_lst = func_bnc.count_freq_tuple( t_ex_lst )
				
				# try:
# 					pattern_dic[ ( ex_hpos , ex_tpos ) ].append(  ( pat_ex_lst , posfreq , h_ex_lst , t_ex_lst ) )
# 				except KeyError:
# 					pattern_dic[ ( ex_hpos , ex_tpos ) ] = [ ( pat_ex_lst , posfreq , h_ex_lst , t_ex_lst ) ]
				
				try:
					hpos = simple_pos_dic[ hpos ]
				except KeyError:
					pass
				
				try:
					tpos = simple_pos_dic[ tpos ]
				except KeyError:
					pass
					
				
				ex_pattern_tagged = "<a rel=\"wordlist.html?" + "|".join( [ it[0] for it in h_ex_lst ] ) + "\" class=\"wordlist\">" + hpos + "</span> " + ex + " <a rel=\"Example|" + "|".join( [ it[0] for it in t_ex_lst ] ) + "\" class=\"wordlist\">" + tpos + "</span>"
				ex_pattern_tup = ( hpos , "|".join( [ it[0] for it in h_ex_lst ] ) , ex , tpos , "|".join( [ it[0] for it in t_ex_lst ] ) )
				ex_pattern_dic[ ex_pattern_tup ] = ( posfreq , h_ex_lst , t_ex_lst , pat_ex_lst )

			ex_sent , ex_pos, ex_shallow = ex_phrase_dic[ tuple(ex) ][0]
			
			fpart_sent , tpart_sent = ex_sent.split( ex ,1 )
			
			# for layout
			ex_sent_tagged = fpart_sent + " <b>" + ex + "</b> " + tpart_sent
			ex_trans_tagged = en_translation_dic[ex].replace(" ","")
			if not ch_ph:
				ch_ph = ex_trans_tagged
			
			ex_pattern_lst = sorted( ex_pattern_dic.items() , key=lambda w:w[1][0] , reverse=True )
			results_ex_lst.append( ( ex , ex_sent_tagged , ex_trans_tagged , ex_pattern_lst ) )
			
		results_lst.append( ( " ".join(p[0]) , ch_ph , round( p[1] , 1 ) , results_ex_lst ) )
	
	return results_lst
	

	
	
	
def generate_pattern_from_phrase( tar_phrase ):

	cand_phrase_lst , en_translation_dic = func_paraphrase.paraphrase_by_bleu( tar_phrase )

	tar_sent_lst = func_bnc.get_sent_from_phrase_file( tar_phrase )
	
	pos_tar_phrase = func_paraphrase.pos_phrase( tar_phrase , tar_sent_lst )
	
	lem_tar_phrase = " ".join( func_paraphrase.lemma_sent2( tar_phrase , pos_tar_phrase ) )
	
	
	ht_pos_tar_phrase = pos_tar_phrase[0][0].lower() + "_" + pos_tar_phrase[-1][0].lower()
	
	
	cand_phrase_dic = {}
	
	ex_phrase_dic = {}
	
	out_pos_phrase_dic = {}
	
	
	extend_phrase_dic = {}
	
	extend_out_pos_phrase_dic = {}
	
	pattern_dic = {}
	
	# get sentences from BNC
	
	tstart = datetime.now()	
	
	
	
	inv_lst = []
	
	for ph in cand_phrase_lst:
		ex_phrase_dic[ tuple(ph[1]) ] =  func_bnc.get_sent_from_phrase_db( ph[1] )

	
	
	tend = datetime.now()
	print "Finish all " +str(len(inv_lst)) + " in " + str( (tend-tstart).seconds )

	
	
	
	
	
	# pack the example sentences and pattern of paraphrases		
	for ph in cand_phrase_lst:
	
		# get POS tag
		pos_lst = func_paraphrase.pos_phrase( ph[1] , ex_phrase_dic[ tuple(ph[1]) ] )
		
		# the head and tail pos inside target phrase
		try:
			ht_pos = pos_lst[0][0].lower() + "_" + pos_lst[-1][0].lower()
		except IndexError:
			continue
		
		# the head and tail pos outside target phrase
		# out_pos = [ ( ( Head POS , Tail POS ) , Freq of Head-Tail POS ) .... ] , Dictionary key=( Head POS , Tail POS ), Value=( ( Head Word , Tail Word ) , Freq )
		# example: [ ( ('MD', 'IN') , 25 ) ,... ] , { ('MD', 'IN'): [(('will', 'in'), 10), (('can', 'in'), 6), (('may', 'in'), 3) ... }
		out_pos = func_bnc.outside_pos( ex_phrase_dic[ tuple(ph[1]) ] , ph[1] )
		
		# Lemmatized phrase
		lem_ph = tuple( func_paraphrase.lemma_sent2( ph[1] , pos_lst ))
		
		#building pattern (pattern_dic)
		otpos_lst , otpos_dic = out_pos
		for otp in otpos_lst:
			ex_pos_lst = []
			for pos_tup , freq in otpos_dic[ otp[0] ]:
				ex_pos_lst.append( (  pos_tup[ 0 ] , ph[1] ,  pos_tup[ 1 ] ) )
			try:
				simple_pos_tup = tuple([ simple_pos_dic[t] for t in otp[0] ])
			except KeyError:
				simple_pos_tup =  otp[0] 
			try:
				pattern_dic[ simple_pos_tup ].append( ( otp[1] , ph[1] , ex_pos_lst ) )
			except KeyError:
				pattern_dic[ simple_pos_tup ] = [ ( otp[1] , ph[1] , ex_pos_lst ) ]
		
		# dispatch the phrases to similar and extended parts
		if ht_pos == ht_pos_tar_phrase:
		
			try:
				cand_phrase_dic[ lem_ph ] += ph[0]
			except KeyError:
				cand_phrase_dic[ lem_ph ] = ph[0]
		
			try:
				out_pos_phrase_dic[ lem_ph ].append( ( ph[1] , out_pos ) )
			except KeyError:
				out_pos_phrase_dic[ lem_ph ] = [ ( ph[1] , out_pos ) ]
		else:
			
		
			try:
				extend_phrase_dic[ lem_ph ] += ph[0]
			except KeyError:
				extend_phrase_dic[ lem_ph ] = ph[0]
		
			try:
				extend_out_pos_phrase_dic[ lem_ph ].append( ( ph[1] , out_pos ) )
			except KeyError:
				extend_out_pos_phrase_dic[ lem_ph ] = [ ( ph[1] , out_pos ) ]
			
	
	sorted_lem_cand_phrase = sorted( cand_phrase_dic.items() , key=lambda w:w[1] , reverse=True )
	sorted_extend_lem_cand_phrase = sorted( extend_phrase_dic.items() , key=lambda w:w[1] , reverse=True )

	results_lst = compile_results( sorted_lem_cand_phrase[:10] , ex_phrase_dic , out_pos_phrase_dic , en_translation_dic )
	extend_results_lst = compile_results( sorted_extend_lem_cand_phrase[:10] , ex_phrase_dic , extend_out_pos_phrase_dic , en_translation_dic )

	return results_lst, extend_results_lst, pattern_dic


def cache_paraphrase( phrase ):
	con = sqlite3.connect("cache_paraphrase.db")
	cur = con.cursor()
	
	cur.execute("SELECT Similar , Extended , Pattern FROM Paraphrase WHERE phrase = ?" , ( phrase, ) )

	try:
		results = cur.fetchall()[0]
	except IndexError:
		results = []

	if results:
		con.close()
		return eval(results[0]) , eval(results[1]) , eval(results[2])

	else:
		
		re_lst, ex_lst, pat_dic = generate_pattern_from_phrase( phrase )
		#if re_lst and ex_lst:
		cur.execute( "INSERT INTO Paraphrase( Phrase , Similar , Extended , Pattern ) VALUES( ? , ? , ? , ? )", ( phrase , str(re_lst) , str(ex_lst) ,  str(pat_dic) )  )
		con.commit()
		return re_lst, ex_lst, pat_dic

def cache_paraphrase_first( phrase ):
	con = sqlite3.connect("cache_paraphrase.db")
	cur = con.cursor()
	
	cur.execute("SELECT Similar , Extended , Pattern FROM Paraphrase WHERE phrase = ?" , ( phrase, ) )

	try:
		results = cur.fetchall()[0]
	except IndexError:
		results = []

	if results:
		con.close()
		return eval(results[0]) , eval(results[1]) , eval(results[2])

	else:
		
		
		return []

con = sqlite3.connect( "cache_paraphrase.bak_20111011.db" )
cur = con.cursor()

for ph,  in cur.execute("SELECT Phrase FROM Paraphrase"):

	if "+" not in ph:
		print ph		
		cache_paraphrase( ph )
	


fin = file("Testsentences")

for line in fin:

	line = " ".join( nltk.word_tokenize(line) ).lower()
	for i in range( 2 , 8 ):
		for p in func_bnc.ngram( line , i ):
			print p
			cache_paraphrase( " ".join(p))
	


