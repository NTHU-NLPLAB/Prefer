#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sqlite3


stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
en_table = ['JA', 'IN', 'SU', 'UF', 'TE', 'EW', 'PA', 'AC', 'HE', 'HO', 'MU', 'JO', 'IZ', 'QA', 'MI', 'FA', 'ME', 'NI', 'IH', 'IR', 'UJ', 'OD', 'TO', 'AQ', 'EH', 'UH', 'DI', 'NA', 'G', 'NE', 'EC', 'VA', 'D', 'AM', 'EP', 'LU', 'TI', 'QE', 'UG', 'IP', 'DE', 'OC', 'A', 'OK', 'UW', 'KO', 'OZ', 'I', 'QI', 'SI', 'GO', 'OR', 'OY', 'ER', 'RO', 'AX', 'DO', 'RE', 'SO', 'T', 'IQ', 'UR', 'IF', 'L', 'UL', 'M', 'IM', 'V', 'OT', 'AN', 'AT', 'UC', 'IW', 'JI', 'EY', 'EN', 'AD', 'EF', 'UX', 'DU', 'JE', 'B', 'VU', 'SE', 'KE', 'OH', 'J', 'LE', 'UV', 'O', 'IT', 'GU', 'IB', 'VE', 'RU', 'P', 'EB', 'RA', 'HU', 'PE', 'PO', 'HA', 'FE', 'FU', 'OV', 'IL', 'UT', 'OB', 'ON', 'E', 'LA', 'IV', 'Q', 'UD', 'LO', 'RI', 'FI', 'UQ', 'ES', 'KA', 'EJ', 'LI', 'SA', 'UZ', 'AP', 'OW', 'UP', 'AV', 'US', 'AB', 'AG', 'NO', 'OG', 'AW', 'QU', 'EX', 'KI', 'GI', 'VI', 'GA', 'F', 'MA', 'AF', 'UY', 'EK', 'AS', 'K', 'AJ', 'AK', 'AZ', 'FO', 'JU', 'MO', 'CA', 'OQ', 'AR', 'IS', 'PI', 'EM', 'C', 'IJ', 'HI', 'N', 'OF', 'UN', 'ET', 'UM', 'CU', '0', 'IG', 'OX', 'DA', 'AY', 'OM', 'OJ', 'BE', 'BO', 'CO', 'QO', 'IK', 'KU', 'UK', 'WA', 'TU', 'W', 'UB', 'S', 'IY', 'NU', 'PU', 'R', 'CI', 'BU', 'IX', 'ID', 'EL', 'BI', 'BA', 'EZ', 'EQ', 'GE', 'CE', 'AH', 'VO', 'EV', 'ED', 'EG', 'H', 'TA', 'OP', 'IC', 'U', 'OS', 'OL', 'AL' , 'OTHERS']

db_root = "BNC_SENT/"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")

# CREATE TABLE Invert_UkWac1 ( Word , SentNo , Posi );
# CREATE INDEX Idx_Word on Invert_UkWac1(Word);


def get_Contentword(phrase):
    phrase = set(phrase.split())
    cnt_word = phrase.difference(stopwords)
    return cnt_word


# def get_Sent_by_phrase(phrase):
#     cnt_words = get_Contentword(phrase)
#     cur_inv.execute("SELECT A.Sent , A.Lemma , A.POS FROM UkWac1 A , Invert_UkWac1 B WHERE A.Sn=B.SentNo AND B.Word=?" , ( word, ) )


def hash_func(s):
    if s[:2].upper() in en_table:
        return s[:2].upper()
    elif s[0].upper() in en_table:
        return s[0].upper()
    else:
        return 'OTHERS'


def get_Sent(word):
    db_path = os.path.join(DB_DIR, "Inverted_table.db")
    con_inv = sqlite3.connect(db_path)
    db_path = os.path.join(DB_DIR, "BNC_Sent_POS.db")
    con_sent = sqlite3.connect(db_path)
    # cur_inv.execute("SELECT A.Sent , A.Lemma , A.POS FROM UkWac1 A , Invert_UkWac1 B WHERE A.Sn=B.SentNo AND B.Word=?", (word,))
    # results = cur_inv.fetchall()
    # for line in results:
    #     print(line)
    table_name = "en_" + hash_func(word)
    # cur_inv.execute( "SELECT Sent_no FROM %s WHERE enWord = ? " % table_name , ( word , ) )
    # results = cur_inv.fetchall()
    sents = []
    cur_inv = con_inv.cursor()
    for sn, in cur_inv.execute("SELECT Sent_no FROM %s WHERE enWord = ? " % table_name, (word, )):
        n = int(sn)
        cur_sent = con_sent.cursor()
        cur_sent.execute("SELECT Sent, POS_tag , Shallow FROM Sent WHERE Sn=?", (sn,))
        sents.append(cur_sent.fetchall()[0])
    return sents


def get_sentSn(word):
    db_path = os.path.join(DB_DIR, "Inverted_table.db")
    con_inv = sqlite3.connect(db_path)
    cur_inv = con_inv.cursor()
    table_name = "en_" + hash_func(word)
    cur_inv.execute("SELECT Sent_no FROM %s WHERE enWord = ? " % table_name, (word,))
    return [i for i, in cur_inv.fetchall()]


def get_path(sn):
    level3 = sn % 200
    level2 = (sn/200) % 200
    level1 = (sn/40000) % 200
    return [str(level1), str(level2), str(level3)]


def get_sn(path):
    level1, level2, level3 = path.split("/")
    return int(level3) + int(level2)*200 + int(level1)*40000


# process the sentences return by BNC
def compile_sent_lst(lst):
    sent = lst[0].split()
    pos = lst[1].split()

    results = [(sent[i], pos[i]) for i in range(len(sent))]

    return results


def get_mutiword_index(cnt_word_lst):
    inv_lst = []

    for word in cnt_word_lst:
        results = get_sentSn(word)
        if not inv_lst:
            inv_lst = set(results)
        else:
            inv_lst = inv_lst.intersection(set(results))

    inv_lst = list(inv_lst)
    inv_lst.sort()

    return inv_lst


def get_Sent_from_sn_file(inv_lst):

    sent_lst = []

    for sn in inv_lst:
        # inverted sn has to minus 1 to meet the sn of sentences
        path = get_path(sn-1)
        sent_lst.append([line.strip() for line in open(db_root + "/".join(path), "rU")])
    return sent_lst


def get_Sent_from_sn_db(inv_lst):
    db_path = os.path.join(DB_DIR, "BNC_Sent_POS.db")
    con_sent = sqlite3.connect(db_path)
    sent_lst = []
    for sn in inv_lst:
        # inverted sn has to minus 1 to meet the sn of sentences
        cur_sent = con_sent.cursor()
        cur_sent.execute("SELECT Sent, POS_tag , Shallow FROM Sent WHERE Sn=?", (sn-1,))
        sent_lst.append(cur_sent.fetchall()[0])
    return sent_lst


def get_sent_from_phrase_file(tphrase):
    cnt_word_lst = get_Contentword(tphrase)
    inv_lst = get_mutiword_index(cnt_word_lst)

    sent_lst = [ts for ts in get_Sent_from_sn_file(inv_lst) if list_cmp(tphrase, ts[0])]

    return sent_lst


def ngram(sent, n):
    sent = sent.split()
    return [sent[i:i+n] for i in range(len(sent)) if i < len(sent)-n+1]


def list_cmp(phrase, sent):
    phrase = phrase.split()
    sent = sent.split()
    j = 0
    i = 0
    st = False
    while j < len(sent):
        if i == len(phrase):
            return True
        if phrase[i] == sent[j]:
            st = True

        if phrase[i] != sent[j]:
            st = False
            i = 0
        elif st:
            i += 1

        j += 1
    if i == len(phrase):
        return True
    return False


def get_sent_from_phrase_db(tphrase):
    cnt_word_lst = get_Contentword(tphrase)
    inv_lst = get_mutiword_index(cnt_word_lst)
    sent_lst = [ts for ts in get_Sent_from_sn_db(inv_lst) if tphrase.split() in ngram(ts[0], len(tphrase.split()))]
    return sent_lst


def get_sent_from_phrase_db2(tphrase):
    db_path = os.path.join(DB_DIR, "invert_phrase.db")
    con_inv_p = sqlite3.connect(db_path)
    cur_inv_p = con_inv_p.cursor()
    # inverted sn has to minus 1 to meet the sn of sentences
    cur_inv_p.execute("SELECT Sent_No FROM Inv_Phrase WHERE Phrase=?", (tphrase,))
    # print(cur_inv_p.fetchall()[0])
    try:
        res = eval(cur_inv_p.fetchall()[0][0])
    except IndexError:
        return []
    if res:
        sent_lst = get_Sent_from_sn_db(res)
        return sent_lst
    else:
        return []

# print(get_sent_from_phrase_db2("play an important role"))


def inside_pos(sent_lst, tphrase):
    pos_dic = {}

    for s in sent_lst:
        cpsent = compile_sent_lst(s)
        try:
            lp, rp = s[0].split(tphrase, 1)
        except ValueError:
            print(s[0])
            print(s[0].split(tphrase))
            exit()

        i = len(lp.split())
        j = len(s[0].split()) - len(rp.split()) - 1

        pos_tup = tuple([p[1] for p in cpsent[i:j+1]])
        try:
            pos_dic[pos_tup] += 1
        except KeyError:
            pos_dic[pos_tup] = 1

    rkpos = sorted(pos_dic.items(), key=lambda w: w[1], reverse=True)
    return rkpos


def count_freq(lst):
    dic = {}
    for l in lst:
        try:
            dic[l] += 1
        except KeyError:
            dic[l] = 1
    return sorted(dic.items(), key=lambda w: w[1], reverse=True)


def count_freq_tuple(lst):
    dic = {}
    for l in lst:
        try:
            dic[l[0]] += l[1]
        except KeyError:
            dic[l[0]] = l[1]
    return sorted(dic.items(), key=lambda w: w[1], reverse=True)


def outside_pos(sent_lst, tphrase):
    fp_dic = {}
    fp_ex_dic = {}
    for s in sent_lst:
        cpsent = compile_sent_lst(s)
        s_lst = s[0].split()
        lp, rp = s[0].split(tphrase, 1)
        i = len(lp.split())
        j = len(s_lst) - len(rp.split()) - 1
        pre = i-1
        fow = j+1

        if (j-i) >= len(s_lst)-1:
            continue

        if pre < 0:
            fp_tup = ("<START>", cpsent[fow][1])
            fp_ex_tup = ("<START>", cpsent[fow][0])
        elif fow > len(s[0].split())-1:
            fp_tup = (cpsent[pre][1], "<END>")
            fp_ex_tup = (cpsent[pre][0], "<END>")
        else:
            fp_tup = (cpsent[pre][1], cpsent[fow][1])
            fp_ex_tup = (cpsent[pre][0], cpsent[fow][0])

        try:
            fp_dic[fp_tup] += 1
        except KeyError:
            fp_dic[fp_tup] = 1
        try:
            fp_ex_dic[fp_tup].append(fp_ex_tup)
        except KeyError:
            fp_ex_dic[fp_tup] = [fp_ex_tup]

    for k in fp_ex_dic:
        fp_ex_dic[k] = count_freq(fp_ex_dic[k])

    fppos = sorted(fp_dic.items(), key=lambda w: w[1], reverse=True)
    # [ ( ( Head POS , Tail POS ) , Freq of Head-Tail POS ) .... ] , Dictionary key=( Head POS , Tail POS ), Value=( ( Head Word , Tail Word ) , Freq )
    return (fppos, fp_ex_dic)

# tphrase = "play"
# tstart = datetime.now()

# pid = os.getpid()
# sent_lst = get_sent_from_phrase_db( tphrase  )
# #sent_lst = get_Sent( tphrase )
# #sent_lst = get_sent_from_phrase( tphrase  )
# #print sent_lst
# tend = datetime.now()
# print "Finish all " + str(len(sent_lst)) + " in " + str( (tend-tstart).microseconds/1000000.0 )


# tstart = datetime.now()

# pid = os.getpid()
# #sent_lst = get_sent_from_phrase_db( tphrase  )
# #sent_lst = get_Sent( tphrase )
# sent_lst = get_sent_from_phrase_file( tphrase )
# #print sent_lst
# tend = datetime.now()
# print "Finish all " + str(len(sent_lst)) + " in " + str( (tend-tstart).microseconds/1000000.0 )

# exit()
# #========================= main  ================================

# tstart = datetime.now()
# sent_lst = get_sent_from_phrase( tphrase )

# tend = datetime.now()
# print "Finish " + str(len(sent_lst)) + " query in " + str( (tend-tstart).seconds )
# print inside_pos( sent_lst )
# print outside_pos( sent_lst )

# tend = datetime.now()
# print "Finish all in " + str( (tend-tstart).seconds )
