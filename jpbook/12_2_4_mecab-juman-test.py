# -*- coding: utf-8 -*-

import nlp.cJuman as cJuman

cJuman.init(['-B', '-e2'])
S = [u'30年も前に言語と画像を研究していた。'.encode('euc-jp')]
print cJuman.parse_opt(S, cJuman.SKIP_NO_RESULT).decode('euc-jp')

