#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
from chasen_reader import *

genpaku = ChasenCorpusReader('/home/hagiwara/dev/data/jeita_genpaku', '0014.chasen', encoding='utf-8') 

print '/'.join( genpaku.words()[80:120] ) 

# 呼び鈴/を/押す/こと/だろ/う/。/アスカム/が/時間/に/几帳面/で/助かっ/た/。/どっち/つか/ず/の/状態/は/、/グラニス/の/神経/にとって/、/徐々に/耐え難い/もの/に/なっ/て/い/た/。/呼び鈴/の/音

grammer = u'''JIRITSU: {<形容詞-自立>|<名詞.*>|<未知語>|<動詞-自立>|<記号-一般>|<副詞.*>}
FUZOKU: {<助動詞>|<助詞.*>|<動詞-接尾>|<動詞-非自立>|<名詞-非自立>}
CHUNK: {(<JIRITSU>+<FUZOKU>*)|<接続詞>}'''

cp = nltk.RegexpParser(grammer)

print cp.parse([(x, '-'.join(y[2].split('-')[0:2])) for x,y in genpaku.tagged_words()[80:120]])

