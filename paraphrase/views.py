# -*- coding: utf8 -*-
# Create your views here.

import sqlite3
import json
import os

from django.shortcuts import render_to_response
from django.http import HttpResponse

from nltk.stem.wordnet import WordNetLemmatizer
from datetime import datetime

import paraphrase.func_paraphrase as func_paraphrase
import paraphrase.func_bnc as func_bnc
import paraphrase.phraseTable as phraseTable
from paraphrase.simple_tag import simple_pos_dic


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")

lmtzr = WordNetLemmatizer()


# compile results for both parphrase and extended paraphrase
def compile_results(lst, ex_phrase_dic, out_pos_phrase_dic, en_translation_dic):
    results_lst = []
    for p in lst:
        results_ex_lst = []
        pattern_dic = {}
        ch_ph = ""

        for ex, (otpos_lst, otpos_dic) in out_pos_phrase_dic[ p[0] ]:
            ex_pattern_dic = {}
            if not otpos_lst:
                continue
            
            for ((hpos, tpos), posfreq) in otpos_lst:
                if posfreq <= 1:
                    continue

                h_ex_lst = []
                t_ex_lst = []
                pat_ex_lst = []
                for ((ex_hpos, ex_tpos), exposfreq) in otpos_dic[(hpos, tpos)]:
                    pat_ex_lst.append(ex_hpos + " " + ex + " " + ex_tpos)
                    h_ex_lst.append((ex_hpos, exposfreq))
                    t_ex_lst.append((ex_tpos, exposfreq))

                h_ex_lst = func_bnc.count_freq_tuple(h_ex_lst)
                t_ex_lst = func_bnc.count_freq_tuple(t_ex_lst)

                # try:
# 					pattern_dic[ ( ex_hpos , ex_tpos ) ].append(  ( pat_ex_lst , posfreq , h_ex_lst , t_ex_lst ) )
# 				except KeyError:
# 					pattern_dic[ ( ex_hpos , ex_tpos ) ] = [ ( pat_ex_lst , posfreq , h_ex_lst , t_ex_lst ) ]

                try:
                    hpos = simple_pos_dic[hpos]
                except KeyError:
                    pass

                try:
                    tpos = simple_pos_dic[tpos]
                except KeyError:
                    pass

                ex_pattern_tagged = "<a rel=\"wordlist/?" + "|".join([it[0] for it in h_ex_lst]) + "\" class=\"wordlist\">" + hpos + "</span> " + ex + " <a rel=\"Example|" + "|".join([it[0] for it in t_ex_lst]) + "\" class=\"wordlist\">" + tpos + "</span>"
                ex_pattern_tup = (hpos, "|".join([it[0] for it in h_ex_lst]), ex, tpos, "|".join([it[0] for it in t_ex_lst]))
                ex_pattern_dic[ex_pattern_tup] = (posfreq, h_ex_lst, t_ex_lst, pat_ex_lst)

            ex_sent, ex_pos, ex_shallow = ex_phrase_dic[tuple(ex)][0]

            fpart_sent, tpart_sent = ex_sent.split(ex, 1)

            # for layout
            ex_sent_tagged = fpart_sent + " <b>" + ex + "</b> " + tpart_sent
            ex_trans_tagged = en_translation_dic[ex].replace(" ", "")
            if not ch_ph:
                ch_ph = ex_trans_tagged

            ex_pattern_lst = sorted(ex_pattern_dic.items(), key=lambda w: w[1][0], reverse=True)
            results_ex_lst.append((ex, ex_sent_tagged, ex_trans_tagged, ex_pattern_lst))

        results_lst.append((" ".join(p[0]), ch_ph, round(p[1], 1), results_ex_lst))

    return results_lst


def get_simple_paraphrase(request):
    try:
        qphrase = request.GET['qphrase']
    except KeyError:
        return HttpResponse("")

    return HttpResponse(json.dumps(dict([(v[1], v[0]) for v in func_paraphrase.paraphrase_by_bleu(qphrase)[0]])))


def generate_pattern_from_phrase(tar_phrase):
    cand_phrase_lst, en_translation_dic = func_paraphrase.paraphrase_by_bleu(tar_phrase)
    tar_sent_lst = func_bnc.get_sent_from_phrase_db2(tar_phrase)
    pos_tar_phrase = func_paraphrase.pos_phrase(tar_phrase, tar_sent_lst)
    lem_tar_phrase = " ".join(func_paraphrase.lemma_sent2(tar_phrase, pos_tar_phrase))
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
        ex_phrase_dic[tuple(ph[1])] = func_bnc.get_sent_from_phrase_db2(ph[1])

    tend = datetime.now()
    print("Finish all " + str(len(inv_lst)) + " in " + str((tend-tstart).seconds))

    # pack the example sentences and pattern of paraphrases
    for ph in cand_phrase_lst:
        # get POS tag
        pos_lst = func_paraphrase.pos_phrase(ph[1], ex_phrase_dic[tuple(ph[1])])

        # the head and tail pos inside target phrase
        try:
            ht_pos = pos_lst[0][0].lower() + "_" + pos_lst[-1][0].lower()
        except IndexError:
            continue

        # the head and tail pos outside target phrase
        # out_pos = [ ( ( Head POS , Tail POS ) , Freq of Head-Tail POS ) .... ] , Dictionary key=( Head POS , Tail POS ), Value=( ( Head Word , Tail Word ) , Freq )
        # example: [ ( ('MD', 'IN') , 25 ) ,... ] , { ('MD', 'IN'): [(('will', 'in'), 10), (('can', 'in'), 6), (('may', 'in'), 3) ... }
        out_pos = func_bnc.outside_pos(ex_phrase_dic[tuple(ph[1])], ph[1])

        # Lemmatized phrase
        lem_ph = tuple(func_paraphrase.lemma_sent2(ph[1], pos_lst))

        # building pattern (pattern_dic)
        otpos_lst, otpos_dic = out_pos
        for otp in otpos_lst:
            ex_pos_lst = []
            for pos_tup, freq in otpos_dic[otp[0]]:
                ex_pos_lst.append((pos_tup[0], ph[1],  pos_tup[1]))
            try:
                simple_pos_tup = tuple([simple_pos_dic[t] for t in otp[0]])
            except KeyError:
                simple_pos_tup = otp[0]
            try:
                pattern_dic[simple_pos_tup].append((otp[1], ph[1], ex_pos_lst))
            except KeyError:
                pattern_dic[simple_pos_tup] = [(otp[1], ph[1], ex_pos_lst)]

        # dispatch the phrases to similar and extended parts
        if ht_pos == ht_pos_tar_phrase:
            try:
                cand_phrase_dic[lem_ph] += ph[0]
            except KeyError:
                cand_phrase_dic[lem_ph] = ph[0]

            try:
                out_pos_phrase_dic[lem_ph].append((ph[1], out_pos))
            except KeyError:
                out_pos_phrase_dic[lem_ph] = [(ph[1], out_pos)]
        else:
            try:
                extend_phrase_dic[lem_ph] += ph[0]
            except KeyError:
                extend_phrase_dic[lem_ph] = ph[0]

            try:
                extend_out_pos_phrase_dic[lem_ph].append((ph[1], out_pos))
            except KeyError:
                extend_out_pos_phrase_dic[lem_ph] = [(ph[1], out_pos)]

    sorted_lem_cand_phrase = sorted(cand_phrase_dic.items(), key=lambda w: w[1], reverse=True)
    sorted_extend_lem_cand_phrase = sorted(extend_phrase_dic.items(), key=lambda w: w[1], reverse=True)

    results_lst = compile_results(sorted_lem_cand_phrase[:10], ex_phrase_dic, out_pos_phrase_dic, en_translation_dic)
    extend_results_lst = compile_results(sorted_extend_lem_cand_phrase[:10], ex_phrase_dic, extend_out_pos_phrase_dic, en_translation_dic)

    return results_lst, extend_results_lst, pattern_dic


def cache_paraphrase(phrase):
    db_path = os.path.join(DB_DIR, "cache_paraphrase.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT Similar , Extended , Pattern FROM Paraphrase WHERE phrase = ?", (phrase,))

    try:
        results = cur.fetchall()[0]
    except IndexError:
        results = []

    if results:
        con.close()
        return eval(results[0]), eval(results[1]), eval(results[2])
    else:
        re_lst, ex_lst, pat_dic = generate_pattern_from_phrase(phrase)
        cur.execute("INSERT INTO Paraphrase(Phrase, Similar, Extended, Pattern) VALUES( ? , ? , ? , ? )", (phrase, str(re_lst), str(ex_lst), str(pat_dic)))
        con.commit()
        return re_lst, ex_lst, pat_dic


def cache_paraphrase_first(phrase):
    db_path = os.path.join(DB_DIR, "cache_paraphrase.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT Similar , Extended , Pattern FROM Paraphrase WHERE phrase = ?", (phrase, ))

    try:
        results = cur.fetchall()[0]
    except IndexError:
        results = []

    if results:
        con.close()
        return eval(results[0]), eval(results[1]), eval(results[2])
    else:
        return []


def get_example(request):
    try:
        qphrase = request.GET['qp']
    except KeyError:
        return HttpResponse("")
    sent_lst = func_bnc.get_sent_from_phrase_db2(qphrase)
    sent_lst = [s[0].replace(qphrase, "<b>" + qphrase + "</b>") for s in sent_lst if len(s[0].split()) < 25][:2]
    return render_to_response("example.html", {'sent_lst': sent_lst})


def get_translation(request):
    try:
        qphrase = request.GET['qp']
    except KeyError:
        return HttpResponse("")
    qphrase = qphrase.replace("_", " ")
    tPhrase = phraseTable.phrase(qphrase)
    if not tPhrase:
        return HttpResponse("")

    if phraseTable.isChinese(qphrase):
        tPhrase = tPhrase[0][1]
    else:
        tPhrase = tPhrase[0][0]
    return render_to_response("translate.html", {'tPhrase': tPhrase})


def get_wordlist(request):
    try:
        qword = request.GET['qword']
    except KeyError:
        return HttpResponse("")
    qword_lst = qword.split("|")
    qword_lst = [lmtzr.lemmatize(w) for w in qword_lst]
    trans_lst = []
    for w in qword_lst:
        tw = phraseTable.phrase(w)
        if not w:
            continue
        if tw:
            trans_lst.append((w, tw[0][0]))
    return render_to_response("wordlist.html", {'trans_lst': trans_lst})


def get_paraphrase2(request):
    if "qphrase" not in request.GET:
        return render_to_response("index.html")
    qphrase = request.GET['qphrase'].strip()
    if not qphrase:
        return render_to_response("index.html")

    tstart = datetime.now()
    results_lst, extend_results_lst, pattern_dic = cache_paraphrase_first(qphrase)
    tend = datetime.now()

    return render_to_response("index2.html", {'qphrase': qphrase, 'results_lst': results_lst, 'extend_results_lst': extend_results_lst , 'pattern_lst': sorted( pattern_dic.items(), key=lambda w: len(w[1]), reverse=True)[:10]})


def get_paraphrase(request):
    # c = {}
    # c.update(csrf(request))
    # print c
    # uid = validate(request)
    # if not uid:
    # 	return render_to_response("index.html",{ "msg":"You have to login" } )
    if "qphrase" not in request.GET:
        return render_to_response("index.html")

    qphrase = request.GET['qphrase'].strip()

    if not qphrase:
        return render_to_response("index.html", {'qphrase': qphrase, "msg": "Please Enter a phrase"})
    # if uid:
    # 	rec( uid , qphrase )	
    uid = ""
    res = cache_paraphrase(qphrase)
    if res:
        if res[0] or res[1]:
            results_lst, extend_results_lst, pattern_dic = res
        else:
            return render_to_response("index.html", {'qphrase': qphrase, "msg": "Not Found"})
    else:
        return render_to_response("index.html", {'qphrase': qphrase, "msg": "Not Found"})

    return render_to_response("index.html", {'qphrase': qphrase, 'uid': uid, 'results_lst': results_lst, 'extend_results_lst': extend_results_lst, 'pattern_lst': sorted(pattern_dic.items(), key=lambda w: len(w[1]), reverse=True)[:10]})


def get_similar_paraphrase(request):
    try:
        qphrase = request.GET['qphrase'].strip()
    except KeyError:
        return HttpResponse("")	

    tstart = datetime.now()
    results_lst, extend_results_lst, pattern_dic = cache_paraphrase(qphrase)
    tend = datetime.now()

    return render_to_response("similar.html", {'qphrase': qphrase, 'results_lst': results_lst, 'extend_results_lst': [], 'pattern_lst': []})


def get_extended_paraphrase(request):
    try:
        qphrase = request.GET['qphrase'].strip()
    except KeyError:
        return HttpResponse("")
    tstart = datetime.now()
    results_lst, extend_results_lst, pattern_dic = cache_paraphrase(qphrase)
    tend = datetime.now()

    return render_to_response("extended.html", {'qphrase': qphrase, 'results_lst': results_lst, 'extend_results_lst': extend_results_lst, 'pattern_lst': []})


def get_pattern_paraphrase(request):
    try:
        qphrase = request.GET['qphrase'].strip()
    except KeyError:
        return HttpResponse("")	

    tstart = datetime.now()
    results_lst, extend_results_lst, pattern_dic = cache_paraphrase(qphrase)
    tend = datetime.now()

    return render_to_response("pattern.html", {'qphrase': qphrase, 'results_lst': [], 'extend_results_lst': [], 'pattern_lst': sorted(pattern_dic.items(), key=lambda w: len(w[1]), reverse=True)[:10]})


def validate(request):
    return request.session.get('uid', False)


def validate_html(request):
    if 'uid' in request.session:
        return HttpResponse("<p>登入使用者為：" + str(request.session['uid']) + "</p>")
    else:
        return HttpResponse("<p>未登入</p>")


def rec(uid, qphrase):
    db_path = os.path.join(DB_DIR, "user.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("INSERT INTO Log ( uid , Query , Time )VALUES( ? , ? , ? )", (uid, qphrase, datetime.now()))
    con.commit()
    con.close()


def login(request):
    db_path = os.path.join(DB_DIR, "user.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    uname = request.POST['name'].strip()
    passwd = request.POST['password'].strip()

    cur.execute("SELECT Passwd FROM User WHERE Uid =?", (uname,))

    try:
        pwd = cur.fetchall()[0][0]

    except IndexError:
        pwd = 0
    # print(pwd)
    con.close()

    if pwd == passwd:
        request.session['uid'] = uname
        return HttpResponse("<p>登入使用者為：" + str(uname) + "</p>")
    else:
        pass


def preview(request):
    try:
        qphrase = request.GET['qphrase'].strip()
    except KeyError:
        return HttpResponse("")

    paraphrase_lst, trans_dic = func_paraphrase.paraphrase_by_bleu(qphrase)

    if not paraphrase_lst:
        return render_to_response("preview.html", {'qphrase': qphrase, 'paraphrase_lst': results_lst[:10], 'msg': "無可用資料, 請更改片語再查"})

    results_lst = []
    for sc, ph in paraphrase_lst:
        results_lst.append((ph, round(sc, 1), trans_dic[ph]))

    return render_to_response("preview.html", {'qphrase': qphrase, 'paraphrase_lst': results_lst[:10], 'msg': "資料彙整中, 請稍候"})

# import sys
# for line in sys.stdin:
# 	line = " ".join(nltk.word_tokenize(line)).lower()
# 	for i in range(2, 8):
# 		for p in func_bnc.ngram(line, i):
# 			print(p)
# 			cache_paraphrase( " ".join(p))
