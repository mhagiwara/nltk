#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import util
import nltk

# 12.4 日本語構文解析

from nltk.parse import DependencyGraph
import jpdep

def _node_map(node):
    # node['word'] = u"<node:%d %s h/f=%d/%d %s>" % (node['address'],
    #                                               '/'.join(node['word']),
    #                                               node['bhead'], node['bform'],
    #                                               '/'.join(t[0] for t in node['tag']))
    
    node['word'] = '/'.join(node['word']).encode('utf-8')
    return node

def reset_deps(dg):
    for node in dg.nodelist:
        node['deps'] = []        
        node['closed'] = False

    dg.root = dg.nodelist[-1]

NEXT_NODE = 1
NEXT_VERB_NODE = 2
NEXT_NOUN_NODE = 3

def get_dep_type(node):
    bform_tag = node['tag'][node['bform']]

    if bform_tag[0] == u"助詞" and bform_tag[1] == u"格助詞":
        return NEXT_VERB_NODE
    elif bform_tag[0] == u"助動詞" and bform_tag[-1] == u"タ":
        return NEXT_NOUN_NODE
    else:
        return NEXT_NODE

def analyze_dependency(dg):
    num_nodes = len(dg.nodelist)
    for i in xrange(num_nodes-1, 0, -1):
        node = dg.nodelist[i]

        util.log( "node i = %d %s" % (i, node['word']) )
        if i == num_nodes - 1:
            # last node -> to_node = 0
            to_node = 0
        elif i == num_nodes - 2:
            # one from the last node -> to_node = num_nodes - 1
            to_node = num_nodes - 1
        else:
            # other nodes
            dep_type = get_dep_type(node)
            if dep_type == NEXT_NODE:
                util.log( " - dep_type: NEXT_NODE" )
                to_node = i + 1
            elif dep_type == NEXT_VERB_NODE or dep_type == NEXT_NOUN_NODE:
                util.log( " - dep_type: NEXT_VERB/NOUN_NODE(%d)" % dep_type )
                for j in xrange(i+1, num_nodes):
                    node_j = dg.nodelist[j]
                    node_j_headtag = node_j['tag'][node_j['bhead']]
                    if (node_j['closed'] == False and
                        (dep_type == NEXT_VERB_NODE and node_j_headtag[0] == u"動詞") or
                        (dep_type == NEXT_NOUN_NODE and node_j_headtag[0] == u"名詞" and
                         node_j_headtag[1] != u"形容動詞語幹")):
                        to_node = j
                        break

        util.log( "  -- to_node = %d %s" % (to_node, dg.nodelist[to_node]['word']) )
        node['head'] = to_node
        dg.nodelist[to_node]['deps'].append(i)
        for j in xrange(i+1, to_node):
            dg.nodelist[j]['closed'] = True

if __name__ == '__main__':

    util.set_utf8_to_stdio()

    cabocha_result = u'''* 0 7D 0/1 0.000000
太郎	名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー	B-PERSON
は	助詞,係助詞,*,*,*,*,は,ハ,ワ	O
* 1 2D 0/0 1.468291
この	連体詞,*,*,*,*,*,この,コノ,コノ	O
* 2 4D 0/1 0.742535
本	名詞,一般,*,*,*,*,本,ホン,ホン	O
を	助詞,格助詞,一般,*,*,*,を,ヲ,ヲ	O
* 3 4D 1/2 1.892480
二	名詞,数,*,*,*,*,二,ニ,ニ	O
郎	名詞,一般,*,*,*,*,郎,ロウ,ロー	O
を	助詞,格助詞,一般,*,*,*,を,ヲ,ヲ	O
* 4 6D 0/1 0.702689
見	動詞,自立,*,*,一段,連用形,見る,ミ,ミ	O
た	助動詞,*,*,*,特殊・タ,基本形,た,タ,タ	O
* 5 6D 0/1 1.193842
きれい	名詞,形容動詞語幹,*,*,*,*,きれい,キレイ,キレイ	O
な	助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ	O
* 6 7D 0/1 0.000000
女性	名詞,一般,*,*,*,*,女性,ジョセイ,ジョセイ	O
に	助詞,格助詞,一般,*,*,*,に,ニ,ニ	O
* 7 -1D 0/1 0.000000
渡し	動詞,自立,*,*,五段・サ行,連用形,渡す,ワタシ,ワタシ	O
た	助動詞,*,*,*,特殊・タ,基本形,た,タ,タ	O
。	記号,句点,*,*,*,*,。,。,。	O
EOS
'''

    dg = jpdep.parse(cabocha_result)
    reset_deps(dg)
    jpdep.set_head_form(dg)

    dg.nodelist = [_node_map(n) for n in dg.nodelist]

    util.ppp( dg.nodelist)

    analyze_dependency(dg)

    print str(dg.tree()).decode('utf-8')

    
    
