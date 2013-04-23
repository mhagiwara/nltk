#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import util

from knbc import *
from nltk.corpus.util import LazyCorpusLoader

root = nltk.data.find('corpora/KNBC_v1.0_090925/corpus1')
fileids = [f for f in find_corpus_fileids(FileSystemPathPointer(root), ".*")
           if re.search(r"\d\-\d\-[\d]+\-[\d]+", f)]

def _knbc_fileids_sort(x):
    cells = x.split('-')
    return (cells[0], int(cells[1]), int(cells[2]), int(cells[3]))

knbc = LazyCorpusLoader('KNBC_v1.0_090925/corpus1', KNBCorpusReader, sorted(fileids, key=_knbc_fileids_sort), encoding='euc-jp')

# print knbc.fileids()

# print '\n'.join( ''.join(sent) for sent in knbc.words() )

print '\n\n'.join( '%s' % tree for tree in knbc.parsed_sents()[0:2] )
print type(knbc.parsed_sents()[0])

# print '\n'.join( ' '.join("%s/%s"%(w[0], w[1][2]) for w in sent) for sent in knbc.tagged_words()[0:20] )
