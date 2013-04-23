#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
# from nltk.book import *

jpgrammer1 = nltk.parse_cfg("""
S -> PP VP
PP -> NP P
VP -> PP VP
VP -> V TENS
NP -> NP 'の' NP
NP -> NP 'と' NP
NP -> N
N -> '先生' | '自転車' | '学校' | '僕'
P -> 'は' | 'が' | 'を' | 'で' | 'に'
V -> '行k' | '殴r' | '見'
TENS -> 'ru' | 'ita'
""")

sent = "先生 は 自転車 で 学校 に 行k ita".split(' ')
parser = nltk.ChartParser(jpgrammer1)
for tree in parser.nbest_parse(sent):
    print tree

sent2 = "学校 に 自転車 で 先生 は 行k ita".split(' ')
for tree in parser.nbest_parse(sent2):
    print tree
   
