#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import util
import jpdep

def normalize_yogen(node):
    surfs = node['word']
    if node['tag'][0][0] == u"動詞":
        if len(node['tag'])>1 and node['tag'][1][0:2] == [u"動詞", u"接尾"]:
            return surfs[0]+node['tag'][1][-3]
        else:
            return node['tag'][0][-3]
    if node['tag'][0][0] == u"名詞" and len(node['tag'])>1 and node['tag'][1][0] == u"動詞":
        return surfs[0]+node['tag'][1][-3]
    if node['tag'][0][0] == u"形容詞":
        return node['tag'][0][-3]
    # 判定詞
    buf = ""
    for i in xrange(0, len(surfs)):
        if node['tag'][i][0] == u"助動詞" and (node['tag'][i][-3] == u"だ"
                                               or node['tag'][i][-3] == u"です"):
            return buf + node['tag'][i][-3]
        else:
            buf += surfs[i]

    return None


def is_yogen(node):
    bhead_tag = node['tag'][node['bhead']]
    bform_tag = node['tag'][node['bform']]

    if bhead_tag[0] == u"動詞":
        return True
    elif bhead_tag[0] == u"形容詞":
        return True
    elif bhead_tag[0] == u"名詞" and bform_tag[0] == u"助動詞":
        return True
    else:
        return False
    
def is_case(node):
    bhead_tag = node['tag'][node['bhead']]
    bform_tag = node['tag'][node['bform']]
    bform_surface = bform_tag[-1]
    if bform_tag[0] == u"助詞" and bform_tag[1] == u"格助詞" and (bform_surface in [u"ガ", u"ヲ", u"ニ", u"ト", u"デ", u"カラ", u"ヨリ", u"ヘ", u"マデ"]):
        return True
    elif bhead_tag[0] == u"名詞" and bform_tag[0:2] == [u"名詞", u"接尾"]:
        print "=== detected noun+suffix: %s" % jpdep.node2str(node)
        return True
    else:
        return False
    
def extract_verb_case(dg):
    # extract the list of verb(= yogen) and cases
    
    # list up all the verb nodes
    for node in dg.nodelist:
        util.log( jpdep.node2str(node) )
        if is_yogen(node):
            util.log( " <-- detected yogen: %s" % normalize_yogen(node) )
            # if yogen, list up all its dependees
            for case_cand in [dg.nodelist[i] for i in node['deps']]:
                if is_case(case_cand):
                    util.log( " <-- detected case: %s" % jpdep.node2str(case_cand) )

            util.log("")

if __name__ == '__main__':

    import sys

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
    jpdep.set_head_form(dg)
    
    extract_verb_case(dg)
