#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3, pickle

import phraseTable

import os, time
import random
import math
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
import func_bnc
from datetime import datetime
import nbest

stopwords = set(['i', 'me', 'my', 'myself', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])



def find_contentwords(phrase):
	content_list = []
	for word in phrase.split():
		if word not in stopwords:
			content_list.append(word)
	return content_list
	

def cache_similary_word( word , LIMIT=15):
	con = sqlite3.connect("cache_similar_word.db")
	cur = con.cursor()
	con.text_factory = str
	cur.execute("SELECT Similar_word FROM Similar_Word WHERE Word = ?" , ( word, ) )

	try:
		#print cur.fetchall()
		results = cur.fetchall()[0][0]

	except IndexError:
		results = []

	if results:
		simword_lst = eval(results)
		just_syn = [word]
		for syn in simword_lst:
			for syn2 in syn[1][:LIMIT]:
				just_syn.append(syn2[0])

		con.close()
		return just_syn

	else:
		simword_lst = getSimSet.findPantelsim(word)
		cur.execute( "INSERT INTO Similar_Word( Word , Similar_word ) VALUES( ? , ? )",( word , str(simword_lst) ))
		con.commit()
		just_syn = [word]
		for syn in simword_lst:
			for syn2 in syn[1][:LIMIT]:
				just_syn.append(syn2[0])
		con.close()
		return just_syn

		

def cache_single_translate( word , LIMIT=15):
	con = sqlite3.connect("cache_single_translate.db")
	cur = con.cursor()
	
	cur.execute("SELECT chWords FROM SingleTranslation WHERE enWord = ?" , ( word, ) )

	try:
		#print cur.fetchall()
		results = cur.fetchall()[0][0]

	except IndexError:
		results = []

	if results:
		con.close()
		return eval(results)

	else:
		trans_lst = phraseTable.phrase(word ,10)
		
		if trans_lst:
			trans_lst = [ w[0] for w in trans_lst ]
			#for chWord in trans_lst:
			cur.execute( "INSERT INTO SingleTranslation( enWord , chWords ) VALUES( ? , ? )",( word , str(trans_lst) ))
			con.commit()
			return trans_lst
		else:
			con.close()
			return []
		#con.commit()

		con.close()
		#return eval(results)


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
		
		cur.execute( "INSERT INTO Paraphrase( Phrase , Similar , Extended , Pattern ) VALUES( ? , ? , ? , ? )", ( phrase , str(re_lst) , str(ex_lst) ,  str(pat_dic) )  )
		con.commit()
		return re_lst, ex_lst, pat_dic
		


def paraphrase_by_translation(phrase,limit=10):
	en_prob_list = []
	
	en_prob_dic = {}
	
	en_translation_dic = {}
	
	ch_trans = phraseTable.phrase(phrase,limit)
	en_pro_list = []
	for ch in ch_trans:

		ch_prob = ch[4] 			
		en_trans = phraseTable.phrase( ch[0] ,limit)
		for en in en_trans:
	
			en_prob = en[6]
			phrase_prob = ch_prob * en_prob
			
			#phrase = en[1].replace(",", "").replace('"', '').replace(' :', '').replace(".", "").replace(";", '').strip()
			phrase = en[1]
			try:
				en_prob_dic[ phrase ] += phrase_prob
			except KeyError:
				en_prob_dic[ phrase ] = phrase_prob
			
			if not en_translation_dic.has_key( en ):
				en_translation_dic[ en[1] ] = ch[0]
			



	return sorted(en_prob_dic.items() , key=lambda w:w[1] , reverse=True) , en_translation_dic





def sum_phrase_prob_exactly(lst):
	rank_dic ={}
	for phrase, prob in lst:
		try: 
			rank_dic[phrase] +=prob
		except KeyError:
			rank_dic[phrase] = prob

	rank_dic2lst = rank_dic.items()
	rank_dic2lst.sort( key=lambda w:w[1] , reverse=True )
	return rank_dic2lst
	

def sum_phrase_prob_combined(lst):  # combine all similar phrases e.g., " for example", ", for example", " for example,"...
	rank_dic ={}
	for phrase, prob in lst:
		phrase = phrase.replace(",", "").replace('"', '').replace(' :', '').replace(".", "").replace(";", '').strip() # combine all similar phrases e.g., " for example", ", for example", " for example,"... 
		try: 
			rank_dic[phrase] +=prob
		except KeyError:
			rank_dic[phrase] = prob

	rank_dic2lst = rank_dic.items()
	rank_dic2lst.sort( key=lambda w:w[1] , reverse=True )
	return rank_dic2lst	
	
	


def find_candidate_phrase( content_words ):
	conn = sqlite3.connect("ACL_only_phrases.db")
	cur = conn.cursor()
	all_phrase = []
	for content in content_words:
		similar_word = cache_similary_word( content , LIMIT=5)
		
		for word in similar_word:
			try:
				word_family = reverted_dict[gslawl_dic[ word ]]
			except KeyError:			
				continue 

			for w in word_family:
				cur.execute("SELECT Sn FROM inverted_phrase WHERE word = ?  GROUP BY Sn", (w,))
				word_no = cur.fetchall()
				
				cur.execute("SELECT phrase,freq FROM linking_phrase JOIN inverted_phrase ON linking_phrase.Sn=inverted_phrase.Sn WHERE word=? " ,(w,))

				all_phrase += list(set(cur.fetchall()))
	conn.close()
	return all_phrase


	
	
def seg_gram(Ch):
	Ch = Ch.decode("utf8")
	uni_list = []
	bi_list = []
	for i in range(len(Ch)):
		uni_list.append(Ch[i])
	
	for i in range(len(Ch)-1):
		bi_list.append(Ch[i] + Ch[i+1])
		
	total = (uni_list, bi_list)
	return total	
	


def penalty(c, r):
	bp = 1-r/c  # if r=c -->bp = 0 --> math.exp(0) = 1.0   --> math.exp(1) = 2.71828
	if c>r:
		BP = 1
	else:
		BP = math.exp(bp)
	return BP
	
def same_cn(L1, L2):
	count_uni_1 = 0
	for i in L1:
		if i in L2:
			count_uni_1 +=1
	return count_uni_1

	
def edit_path( L1 , L2 ):

	A1 = L1.split()
	A2 = L2.split()

	#init Matrix M
	M = [[0 for k in range(len(A1)+1)] for m in range(len(A2)+1)]
	for i in range(len(A2)+1):
		M[i][0] = i
	for j in range(len(A1)+1):
		M[0][j] = j

	#doing edit distance matrix
	for j in range(1,len(A2)+1):
		for i in range(1,len(A1)+1):
			cost = 0
			if A1[i-1] == A2[j-1]:
				cost = 0
			else:
				cost = 1
			
			M[j][i] = min( M[j][i-1]+1 , M[j-1][i]+1 , M[j-1][i-1]+cost)
			
			if j > 2 and i > 2:
				if A1[i-1] == A2[j-2] and A1[i-2] == A2[j-1]:
					M[j][i] = min( M[j-2][i-2]+1 , M[j][i] ) 
			
	path = []

	R2 = reversed(range(len(A2)))
	R1 = reversed(range(len(A1)))

	x = range(len(A1))[-1]
	y = range(len(A2))[-1]
	while x != -1 and y !=-1 :
		ls = [ M[y][x] , M[y+1][x] , M[y][x+1] ]
		if  A1[x] == A2[y]:
			path.append(A2[y])
		else:
			if A1[x] == A2[y-1] and A1[x-1] == A2[y]:
				path.append('{' + A2[y-1] + ' ' + A2[y] + '/' + A1[x-1] + ' ' + A1[x] + '}')
			elif ls.index(min(ls)) == 1:
				path.append('{0/' + A1[x] +'}')
			elif ls.index(min(ls)) == 2:
				path.append('{' + A2[y] + '/0}')
			else:
				path.append('{' + A2[y] + '/' + A1[x] + '}' )
				
		if ls.index(min(ls)) == 0:
			if A1[x] == A2[y-1] and A1[x-1] == A2[y]:
				x -= 2
				y -= 2
			else:
				x -= 1
				y -= 1
		elif ls.index(min(ls)) == 1:
			x -= 1
		elif ls.index(min(ls)) == 2:
			y -= 1

	path.reverse()

	return path
	

def BLEU(C, R_lst): # input: one candidate phrase and a list of reference phrases to measure BLEU
	c = len(C) # for penalty
	
	Candidate_lst = []	# only one element in Ch1
	for gram_list in seg_gram(C): 
		Candidate_lst.append(gram_list) ##[uni1], [bi1], [tri], [four1]
		
	Ref_lst = []
	for ele in R_lst:
		r = len(ele) # for penalty
		Ref_lst.append(seg_gram(ele))   ##[([uni1], [bi1], [tri], [four1]), ([uni2], [bi2], [tri2], [four2])]  #ele[0]-->>[uni1],[uni2]

	max_lst = [] 	
	for i in range(len(Candidate_lst)):
		candidate_gram_no = len([x for x in Candidate_lst if x]) 
		if i > candidate_gram_no-1: # if "any ngram list" in Candidate_lst is empty, pass it
			break
		
		max = 0
		weighted_log_pn = 0
		for ref in Ref_lst:
			
			num = same_cn(Candidate_lst[i], ref[i])
			if num > max:
				max = num
		
		if len(Candidate_lst[i])!=0:
			precision = max/float(len(Candidate_lst[i]))
			if precision !=0:
				log_pn = math.log(precision)
				weighted_log_pn = log_pn*(float(1)/candidate_gram_no)
			else:
				weighted_log_pn = -999999999
			
			
			max_lst.append(weighted_log_pn)
	
	sum_precision = sum(max_lst)
	BLEU = math.exp(sum_precision)
	
	if not R_lst:
		return 0.0
		
	r = sum( [ len(l) for l in R_lst ] )/ float( len([ len(l) for l in R_lst ]) )

	BLEU = penalty(c,r)*BLEU
	
	return BLEU	

	
	
def compare_BLEU( E1 , E2 , thresh=20 ):  # input two english phrases to measure the BLEU of the translation of a candidate phrase and reference list e.g., 1 candidate vs. 5 references -->>5 BLEU  
	C_list = []
	R_list = []
	pivot_ch_trans = phraseTable.phrase( E1 , thresh ) #find Chinese translations
	for ele in pivot_ch_trans:
		C_list.append(ele[0].replace(" ", "")) #the candidate phrases-->>例如, 舉例來說, 為例, 舉例說, 舉例而言
	#print C_list
	
	E2_ch_trans = phraseTable.phrase( E2 , thresh ) #find Chinese translations	
	
	for ele in E2_ch_trans:
		R_list.append(ele[0].replace(" ", ""))# the reference phrases-->>  舉例來說, 例如, 為例, 舉例說, 譬如

	count = 0
	count_0 = 0
	BLEU_lst = []
	for ele in C_list: 
		BLEU_score = BLEU(ele, R_list)
		BLEU_lst.append(BLEU_score)
	final_BLEU = sum(BLEU_lst)/len(C_list)
	return final_BLEU	#[1.0, 1.0, 1.0, 1.0, 0.0]

def all_BLEU_BURCH(E1): # input a phrase (E1) -->> find all possible phrases (E2) including the synonyms of the content words of the given phrase -->> measure E1 and all E2
	all_phrase = []
	
	phrase_set = paraphrase_by_translation(E1,limit=10) #[('for example', 0.38606418360797889), ('such as', 0.26103938656615994), ('for instance', 0.11788190559805098), ('as an example', 0.019727182253200002), ('like', 0.018110080116559998), ('e.g.', 0.0125408938259949), ('if', 0.011593793760800001), ('example', 0.010506768617485), ('such as the', 0.008407152252600001), ('say', 0.0079267509457999989), ('as', 0.0027910131832799999), ('one example', 0.0015242601399020001), ...
	for ele in phrase_set:
		all_phrase.append(ele[0])  # every phrase in phrase_set
	# print all_phrase[:5]  #['more precisely', 'more accurately', 'more accurate', 'more specific', 'a more accurate']
	# print "UUUUUUUUU"
	all_BLEU_BURCH_lst = []
	BLEU_candidate_BURCH_lst = []
	for E2 in all_phrase:
		if E2!= E1:
			all_BLEU_BURCH_lst.append((compare_BLEU(E1, E2), E1, E2))
			all_BLEU_BURCH_lst.sort( key=lambda w:w[0] , reverse=True )
	for ele in all_BLEU_BURCH_lst[:50]:  
		# print ele  #(2.2071067811865475, 'more precisely', 'more explicit')
		# print "LLLLLLL"
		BLEU_candidate_BURCH_lst.append(ele[2])
	return BLEU_candidate_BURCH_lst


def paraphrase_by_bleu(E1): # input a phrase (E1) -->> find all possible phrases (E2) including the synonyms of the content words of the given phrase -->> measure E1 and all E2
	all_phrase = []
	
	phrase_set, en_translation_dic = paraphrase_by_translation(E1,limit=10) #[('for example', 0.38606418360797889), ('such as', 0.26103938656615994),
	
	BLEU_candidate_BURCH_lst = []
	for tpe, prob in phrase_set:
		if tpe!= E1:
			BLEU_candidate_BURCH_lst.append( (compare_BLEU( E1, tpe), tpe ) )
	
	BLEU_candidate_BURCH_lst.sort( key=lambda w:w[0] , reverse=True )
	
	return BLEU_candidate_BURCH_lst , en_translation_dic

def dice( lst1 , lst2 ):
	inter_no = len(set( lst1 ).intersection( set( lst2) ))
	return (float(inter_no)*2)/(len(set(lst1))+len(set(lst2)))
	

def in_pos_constrain( ph1 , ph2_lst ):
	cand_pos = [ p[1] for p in pos_tag( ph1.split() ) ]
	ht_pos = cand_pos[0] + "_" + cand_pos[-1]
	results_lst = []
	for ph in ph2_lst:
		res_pos = [ p[1] for p in pos_tag( ph ) ]
		ht_res_pos = res_pos[0] + "_" + res_pos[-1]
		if ht_res_pos == ht_pos:
			results_lst.append( ph )
	return results_lst

	
def lemma_sent( phrase ):
	
	sent_pos = [ p[1].lower()[0] for p in pos_tag( phrase ) ]
	phrase = phrase.split()
	results = []
	
	for i in range(len( phrase )):
		if sent_pos[i] in 'vn':
			results.append( lmtzr.lemmatize( phrase[i] , sent_pos[i] ) )
		else:
			results.append( phrase[i] )
		
	return results
	
def lemma_sent2( phrase , pos_lst ):
	
	pos_lst = [ p[0].lower() for p in pos_lst ]
	
	phrase = phrase.split()
	
	results = []
	
	for i in range(len( phrase )):
		
		if pos_lst[i] in 'vn':
			results.append( lmtzr.lemmatize( phrase[i] , pos_lst[i] ) )
		else:
			results.append(  phrase[i]  )	
	return results


def pos_phrase( phrase , sent_lst ):
	try:		
		return func_bnc.inside_pos( sent_lst , phrase )[0][0]
	except IndexError:
		return [ p[1] for p in pos_tag( phrase.split() ) ]


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
				ex_pattern_tagged = "<span title=\"Example|" + "|".join( [ it[0] for it in h_ex_lst ] ) + "\" class=\"wordlist\">" + hpos + "</span> " + ex + " <span title=\"Example|" + "|".join( [ it[0] for it in t_ex_lst ] ) + "\" class=\"wordlist\">" + tpos + "</span>"
				ex_pattern_dic[ ex_pattern_tagged ] = ( posfreq , h_ex_lst , t_ex_lst , pat_ex_lst )
			ex_sent , ex_pos, ex_shallow = ex_phrase_dic[ tuple(ex) ][0]
			
			fpart_sent , tpart_sent = ex_sent.split( ex ,1 )
			
			# for layout
			ex_sent_tagged = fpart_sent + " <b>" + ex + "</b> " + tpart_sent
			ex_trans_tagged = en_translation_dic[ex].replace(" ","")
			if not ch_ph:
				ch_ph = ex_trans_tagged
			
			results_ex_lst.append( ( ex , ex_sent_tagged , ex_trans_tagged , ex_pattern_dic ) )
			
		results_lst.append( ( " ".join(p[0]) , ch_ph , round( p[1] , 1 ) , results_ex_lst ) )
	
	return results_lst
	
def generate_pattern_from_phrase( tar_phrase ):


	
	
	cand_phrase_lst , en_translation_dic = paraphrase_by_bleu( tar_phrase )
	
	tar_sent_lst = func_bnc.get_sent_from_phrase_db2( tar_phrase )
	
	pos_tar_phrase = pos_phrase( tar_phrase , tar_sent_lst )
	
	lem_tar_phrase = " ".join( lemma_sent2( tar_phrase , pos_tar_phrase ) )
	
	
	ht_pos_tar_phrase = pos_tar_phrase[0][0].lower() + "_" + pos_tar_phrase[-1][0].lower()
	
	
	cand_phrase_dic = {}
	
	ex_phrase_dic = {}
	
	out_pos_phrase_dic = {}
	
	
	extend_phrase_dic = {}
	
	extend_out_pos_phrase_dic = {}
	
	pattern_dic = {}
	
	# get sentences from BNC
	for ph in cand_phrase_lst:
		ex_phrase_dic[ tuple(ph[1]) ] =  func_bnc.get_sent_from_phrase_db2( ph[1] )
	
	# pack the example sentences and pattern of paraphrases		
	for ph in cand_phrase_lst:
	
		# get POS tag
		pos_lst = pos_phrase( ph[1] , ex_phrase_dic[ tuple(ph[1]) ] )
		
		# the head and tail pos inside target phrase
		ht_pos = pos_lst[0][0].lower() + "_" + pos_lst[-1][0].lower()
		
		# the head and tail pos outside target phrase
		# out_pos = [ ( ( Head POS , Tail POS ) , Freq of Head-Tail POS ) .... ] , Dictionary key=( Head POS , Tail POS ), Value=( ( Head Word , Tail Word ) , Freq )
		# example: [ ( ('MD', 'IN') , 25 ) ,... ] , { ('MD', 'IN'): [(('will', 'in'), 10), (('can', 'in'), 6), (('may', 'in'), 3) ... }
		out_pos = func_bnc.outside_pos( ex_phrase_dic[ tuple(ph[1]) ] , ph[1] )
		
		# Lemmatized phrase
		lem_ph = tuple(lemma_sent2( ph[1] , pos_lst ))
		
		#building pattern (pattern_dic)
		otpos_lst , otpos_dic = out_pos
		for otp in otpos_lst:
			ex_pos_lst = []
			for pos_tup , freq in otpos_dic[ otp[0] ]:
				ex_pos_lst.append( ( pos_tup[ 0 ] , ph[1] , pos_tup[ 1 ] ) )
			try:
				pattern_dic[ otp[0] ].append( ( otp[1] , ph[1] , ex_pos_lst ) )
			except KeyError:
				pattern_dic[ otp[0] ] = [ ( otp[1] , ph[1] , ex_pos_lst ) ]
		
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



#========================= main  ================================



# render the results to compiled parameter

# ================ Present ======================
# 
# tar_phrase = "play an important role"
# tstart = datetime.now()
# results_lst, extend_results_lst, pattern_dic = generate_pattern_from_phrase( tar_phrase)
# 
# for phrase, ch_ph , score, ex_lst in results_lst:
# 	print phrase 
# print
# for phrase, ch_ph , score, ex_lst in extend_results_lst:
# 	print phrase
# 
# print
# 
# 
# 
# 
# 
# for phrase, ch_ph , score, ex_lst in results_lst:
# 	print phrase 
# 	print ch_ph
# 	print score
# 	print "=========== example =============="
# 	for ex in ex_lst:
# 
# 		print "=========== pattern =============="
# 		for pat in ex[3]:
# 			print pat
# 			print ex[3][pat][1]
# 			print ex[3][pat][2]
# 			print "Example: "
# 			for ex_phrase in ex[3][pat][3]:
# 				print "\t" + ex_phrase
# 			print ""
# 		print ex[0]
# 		print ex[2]
# 		print ex[1]
# 		print 
# 	print
# 	
# for phrase, ch_ph , score, ex_lst in extend_results_lst:
# 	print phrase 
# 	print ch_ph
# 	print score
# 	print "=========== example =============="
# 	for ex in ex_lst:
# 
# 		print "=========== pattern =============="
# 		for pat in ex[3]:
# 			print pat
# 			print ex[3][pat][1]
# 			print ex[3][pat][2]
# 			print "Example: "
# 			for ex_phrase in ex[3][pat][3]:
# 				print "\t" + ex_phrase
# 			print ""
# 		print ex[0]
# 		print ex[2]
# 		print ex[1]
# 		print 
# 
# 	print
# 
# 
# print "=========== General pattern =============="
# for pat, detail in sorted( pattern_dic.items() , key=lambda w:len(w[1]) , reverse=True )[:10]:
# 	print pat
# 	print detail
# 	print pattern_dic[pat][1]
# 	print pattern_dic[pat][2]
# 	print "Example: "
# 	for ex_phrase in pattern_dic[pat][3]:
# 		print "\t" + ex_phrase
# print
# tend = datetime.now()
# print "Finish all in " + str( (tend-tstart).seconds )	




	