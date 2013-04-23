# -*- coding: utf-8 -*-

import nltk

from nltk.corpus.reader import *
from nltk.corpus.reader.util import *

import jptokenizer

jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^　「」！？。]*[！？。]')

reader = PlaintextCorpusReader("/home/hagiwara/dev/data/jpbook/", r'gingatetsudono_yoru.txt',
                               encoding='utf-8',
                               para_block_reader=read_line_block,
                               sent_tokenizer=jp_sent_tokenizer,
                               word_tokenizer=jptokenizer.JPSimpleTokenizer())

print ' '.join(reader.words()[20:80])
