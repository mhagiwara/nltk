#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
import util
import re


from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.probability import *

from nltk.text import Text
from chasen import *

import romkan

genpaku = ChasenCorpusReader('/home/hagiwara/dev/data/jeita/', 'g.*chasen', encoding='utf-8')

# print len(genpaku.words())
# print sum(len(w) for w in genpaku.words())

genpaku_t = Text(genpaku.words())

# --- 語彙列挙
# genpaku_vocab = set(w for w in genpaku.words() if re.match(ur"^[ぁ-んーァ-ンー\u4e00-\u9FFF]+$", w))
# print ' '.join( sorted(genpaku_vocab)[:10] )

# --- Exercise 学の列挙

# print ' '.join( set(w for w in genpaku.words() if w.endswith(u"学") and not w.endswith(u"大学") ) )

# --- Exercise -い＋名詞
# print ' '.join( wt1[0]+wt2[0] for wt1, wt2 in nltk.bigrams(genpaku.tagged_words()[2000:20000]) if wt1[0].endswith(u"い") and wt2[1][2].startswith(u"名詞") )

# --- Exercise 複合名詞
# mlen = 0
# cnoun = []
# for w, t in genpaku.tagged_words():
#     if t[2].startswith(u'名詞') and not t[2].endswith(u'数'):
#         cnoun.append("%s:%s" % (w, t[2]))
#         if len(cnoun) >= mlen:
#             print ' '.join(cnoun), mlen
#             mlen = len(cnoun)
#     else:
#          cnoun = []
        

# --- 同音異義語
# print ' '.join( set(w for w,t in genpaku.tagged_words() if t[0] == u"コウショウ") )

# genpaku_wfd = FreqDist(genpaku_t)
# genpaku_wfd.tabulate(10)

# genpaku_tfd = FreqDist(t[2] for (w, t) in genpaku.tagged_words())
# genpaku_tfd.tabulate(10)

# genpaku_wfd_u8 = FreqDist(romkan.to_roma(w) for w in genpaku_t)
# genpaku_wfd_u8.plot(10)

# --- コロケーション、ランダム文生成
# genpaku_t.collocations()

# genpaku_t.generate()

# --- 同義語

# genpaku_t.similar(u"ソフトウェア")
genpaku_t.similar(u"トイレ")
