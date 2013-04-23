#! /usr/bin/python
# -*- coding: utf-8 -*-

import CaboCha
import sys

cabocha = CaboCha.Parser('--charset=UTF8')
sent = u"太郎はこの本を二郎を見た美しく女性に渡した。".encode('utf-8')

print cabocha.parseToString(sent)
tree = cabocha.parse(sent)

# CaboCha.FORMAT_TREE, FORMAT_LATTICE, TREE_LATTICE, XML
print tree.toString(CaboCha.FORMAT_LATTICE)

