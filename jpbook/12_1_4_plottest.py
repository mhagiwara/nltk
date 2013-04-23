#! /usr/bin/python
# -*- coding: utf-8 -*-



import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from nltk.probability import *


import pylab
from matplotlib.font_manager import FontProperties

figtitle = u"日本語のタイトルは？"
t = pylab.gcf().text(0.5, 0.95, figtitle,
                     horizontalalignment='center',
                     fontproperties=FontProperties(fname='/home/hagiwara/dev/src/nlp/nlpwp/VLGothic/VL-Gothic-Regular.ttf'))

arr = [u"イ", u"ロ", u"ハ", u"甲", u"乙", u"丙"]
fd = FreqDist(arr)
fd.plot(6)
