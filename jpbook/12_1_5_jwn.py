#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import util

from nltk.corpus.reader.wordnet import *

class JapaneseWordNetCorpusReader(WordNetCorpusReader):
    
    def __init__(self, root, filename):
        WordNetCorpusReader.__init__(self, root)

        import codecs
        f=codecs.open(filename, encoding="utf-8")
        self._jword2offset = {}
        for line in f:
            _cells = line.strip().split('\t')
            _offset_pos = _cells[0]
            _word = _cells[1]
            if len(_cells)>2: _tag = _cells[2]
            _offset, _pos = _offset_pos.split('-')
            self._jword2offset[_word] = {'offset': int(_offset), 'pos': _pos}


    def synset(self, word):
        if word in self._jword2offset:
            return WordNetCorpusReader._synset_from_pos_and_offset(
                self, self._jword2offset[word]['pos'], self._jword2offset[word]['offset']
                )
        else:
            return None

if __name__ == '__main__':
    jwn = JapaneseWordNetCorpusReader(nltk.data.find('corpora/wordnet'),
                                      '/home/hagiwara/dev/data/jwordnet/wnjpn-ok.tab')
    jsyn_whale = jwn.synset(u"鯨") 
    jsyn_apple = jwn.synset(u"りんご") 
    jsyn_orange = jwn.synset(u"ミカン") 
    
    print jsyn_apple.path_similarity( jsyn_orange)
    print jsyn_whale.path_similarity( jsyn_orange)
