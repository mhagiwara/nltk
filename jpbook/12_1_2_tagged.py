#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import util

from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.probability import *

from nltk.text import Text
from chasen import *

jeita = ChasenCorpusReader('/home/hagiwara/dev/data/jeita/', '.*chasen', encoding='utf-8')
print '/'.join( jeita.words()[22100:22140] )

print '\nEOS\n'.join(['\n'.join("%s/%s" % (w[0],w[1][2]) for w in sent) for sent in jeita.tagged_sents()[2170:2173]]) 
