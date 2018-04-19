#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy

# Request
# server = ServerProxy('http://nlp0.cs.nthu.edu.tw:8080')
# result = server.translate({'text': '我 是 一 個 學 生 。', 'align': 'True'})


def get_nbest(phrase):
    server = ServerProxy('http://nlp0.cs.nthu.edu.tw:8081')
    result = server.translate({'text': phrase, 'align': 'False'})
    return sorted(result['nbest'].encode("utf8").splitlines())[0].split(":")[1]
