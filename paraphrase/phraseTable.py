# -*- coding: UTF-8 -*-
import sqlite3
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")

pch = re.compile(u"^[\u4E00-\u9FA5 *,\d]+$")


def isChinese(s):
    if pch.findall(s) == []:
        return False
    else:
        return True


def phrase(q, limit=5):
    if not q:
        return []

    opr = "="
    # limit = 5
    db_path = os.path.join(DB_DIR, "phrase_table.db")
    con = sqlite3.connect(db_path)
    con.text_factory = str
    cur = con.cursor()

    if isChinese(q):
        ch = q.replace(" ", "")
        if limit == 0:
            sql = "select * from phrase_table where cphrasekey %s ? order by min(pec, pce) desc" % (opr,)
        else:
            sql = "select * from phrase_table where cphrasekey %s ? order by min(pec, pce) desc limit %d" % (opr, limit)
        cur.execute(sql, [ch])
    else:
        en = q
        if limit == 0:
            sql = "select * from phrase_table where ephrase %s ? order by min(pec, pce) desc" % (opr,)
        else:
            sql = "select * from phrase_table where ephrase %s ? order by min(pec, pce) desc limit %d" % (opr, limit)
        cur.execute(sql, [en])

    result = []
    for row in cur:
        result.append(row)
    return result
