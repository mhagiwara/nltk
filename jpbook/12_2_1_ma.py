#! /usr/bin/python
# -*- coding: utf-8 -*-

import nltk
import util

# 12.3 日本語形態素解析用

def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        if not 'value' in trie:
            trie['value'] = []
        trie['value'].append(value)

matrie = nltk.defaultdict(dict)


_BOS_ENTRY = {'length':1, 'pos':'BOS', 'lemma': u'BOS', 'cost': 0}
_EOS_ENTRY = {'length':1, 'pos':'EOS', 'lemma': u'EOS', 'cost': 0}
# V-動詞: Z-未然 Y-連用 S-終止 T-連体 K-仮定 R-命令
# J-助詞: K-格助詞 F-副助詞
# A-助動詞

dict_entries = [
    [u"かれ",   {'pos':'V-Y', 'lemma':u"枯れ"}],
    [u"かれ",   {'pos':'V-Y', 'lemma':u"枯れ"}],
    [u"かれ",   {'pos':'N', 'lemma':u"彼"}],
    [u"の",     {'pos':'J-K', 'lemma':u"の"}],
    [u"く",     {'pos':'N', 'lemma':u"区"}],
    [u"くる",   {'pos':'V-S', 'lemma':u"来る"}],
    [u"くる",   {'pos':'V-T', 'lemma':u"来る"}],
    [u"くるま", {'pos':'N', 'lemma':u"車"}],
    [u"ま",     {'pos':'N', 'lemma':u"間"}],
    [u"まで",   {'pos':'J-F', 'lemma':u"まで"}],
    [u"で",     {'pos':'J-K', 'lemma':u"で"}],
    [u"でま",   {'pos':'N', 'lemma':u"デマ"}],
    [u"まつ",   {'pos':'N', 'lemma':u"松"}],
    [u"まつ",   {'pos':'V-S', 'lemma':u"待つ"}],
    [u"まつ",   {'pos':'V-T', 'lemma':u"待つ"}],
    [u"つ",     {'pos':'N', 'lemma':u"津"}]
]

def add_entries_to_trie(trie, entries):

    for entry in entries:
        entry[1]['length'] = len(entry[0])
        insert(trie, entry[0].encode('utf-8'), entry[1])


add_entries_to_trie(matrie, dict_entries)

# SF: 接尾辞, T-連体詞
# A: 助動詞

dict_entries2 = [
    [u"こ",      {'pos':'SF', 'lemma':u"個",   'cost': 10}],
    [u"この",    {'pos':'T',  'lemma':u"この", 'cost': 10}],
    [u"ひ",      {'pos':'N',  'lemma':u"日",   'cost': 40}],
    [u"ひと",    {'pos':'N',  'lemma':u"人",   'cost': 40}],
    [u"ひとこと",{'pos':'N',  'lemma':u"一言", 'cost': 40}],
    [u"と",      {'pos':'J',  'lemma':u"と",   'cost': 10}],
    [u"こと",    {'pos':'N',  'lemma':u"事",   'cost': 10}],
    [u"で",      {'pos':'V-Z','lemma':u"出",   'cost': 40}],
    [u"で",      {'pos':'V-Y','lemma':u"出",   'cost': 40}],
    [u"で",      {'pos':'J',  'lemma':u"で",   'cost': 10}],
    [u"げんき",  {'pos':'N',  'lemma':u"元気", 'cost': 40}],
    [u"に",      {'pos':'J',  'lemma':u"に",   'cost': 10}],
    [u"になっ",  {'pos':'V-Y','lemma':u"担っ", 'cost': 40}],
    [u"なっ",    {'pos':'V-Y','lemma':u"なっ", 'cost': 40}],
    [u"た",      {'pos':'A',  'lemma':u"た",   'cost': 10}]
]

matrie2 = nltk.defaultdict(dict)
add_entries_to_trie(matrie2, dict_entries2)

def common_prefix_search(trie, key):
    ret = []
    if 'value' in trie:
        ret += trie['value']
    if key:
        first, rest = key[0], key[1:]
        if first in trie:
            ret += common_prefix_search(trie[first], rest)
    return ret
    
def is_connective(bnode, cnode):
    ctable = set([
        ('BOS', 'N'), ('BOS', 'V'), ('BOS', 'T'),
        ('T', 'N'), ('N', 'J'), ('J', 'N'),  ('J', 'V'),
        ('V-T', 'N'), ('V-T', 'J-F'), ('V-Y', 'A'),  ('V-S', 'EOS'), ('A', 'EOS')
        ])
    bpos = bnode['entry']['pos']
    bpos_s = bpos.split('-')[0]
    cpos = cnode['entry']['pos']
    cpos_s = cpos.split('-')[0]

    return (((bpos, cpos) in ctable) or ((bpos_s, cpos) in ctable)
            or ((bpos, cpos_s) in ctable) or ((bpos_s, cpos_s) in ctable))


def enum_solutions(node):
    results = []
    if node['entry']['lemma'] == u'EOS':
        return [[u'EOS']]
    for nnode in node['next']:
        for solution in enum_solutions(nnode):
            results.append([node['entry']['lemma']]+solution)
    return results


def analyze(trie, sent, connect_func=lambda x,y: True, cost_func=lambda x,y: 0):
    bos_node = {'begin':-1, 'next':[], 'entry': _BOS_ENTRY, 'cost': 0}
    end_node_list = nltk.defaultdict(list)
    end_node_list[0].append(bos_node)
    
    for i in range(0, len(sent)+1):
        if i < len(sent):
            cps_results = common_prefix_search(trie, sent[i:].encode('utf-8'))
        else:
            # EOS
            cps_results = [_EOS_ENTRY]

        print "i=%d" % i
        # bnode_trace
        node_repr = lambda x: "%s[%d-%d][%s]" % (x['entry']['lemma'],
                                                 x['begin'], x['begin']+x['entry']['length'],
                                                 x['entry']['pos'])
        print "end_node_list[%d]=%s" % (i, '/'.join(node_repr(x) for x in end_node_list[i]))

        # cps_result trace
        print "cps_result of pos %d = %s" % (i, '/'.join(x['lemma'] for x in  cps_results))

        for centry in cps_results:
            cnode = {'begin': i, 'next':[], 'entry':centry}
            min_cost = -1
            min_bnodes = []

            for bnode in end_node_list[i]:
                if connect_func(bnode, cnode):
                    cost = bnode['cost'] + cost_func(bnode, cnode)

                    if min_cost < 0 or cost < min_cost:
                        min_cost = cost
                        min_bnodes = [bnode]
                    elif cost == min_cost:
                        min_bnodes.append(bnode)

            if len(min_bnodes) > 0:
                for bnode in min_bnodes:
                    cnode['cost'] = min_cost
                    bnode['next'].append(cnode)
                    
                end_nodes = end_node_list[i+centry['length']]
                if not cnode in end_nodes: end_nodes.append(cnode)
        print ""

    # analysis finished
    return enum_solutions(bos_node)

def analyze_simple(trie, sent, connect_func=lambda x, y: True):
    bos_node = {'next':[], 'entry': _BOS_ENTRY}
    end_node_list = nltk.defaultdict(list)
    end_node_list[0].append(bos_node)
    
    for i in range(0, len(sent)+1):
        if i < len(sent):
            cps_results = common_prefix_search(trie, sent[i:].encode('utf-8'))
        else:
            # EOS
            cps_results = [_EOS_ENTRY]

        for centry in cps_results:
            cnode = {'next':[], 'entry':centry}

            for bnode in end_node_list[i]:
                if connect_func(bnode, cnode):
                    bnode['next'].append(cnode)
                    
                    end_nodes = end_node_list[i+centry['length']]
                    if not cnode in end_nodes: end_nodes.append(cnode)

    return enum_solutions(bos_node)

def cost_minimum(bnode, cnode):
    ctable = {
        ('BOS', 'T'): 10,
        ('T', 'N'):   10,
        ('N', 'J'):   10,
        ('J', 'N'):   10,
        ('N', 'N'):   10,
        ('N', 'V-Z'): 40,
        ('N', 'V-Y'): 40,
        ('V-Z', 'N'): 40,
        ('V-Y', 'N'): 40,
        ('J', 'V-Z'): 10,
        ('J', 'V-Y'): 10,
        ('V-Y', 'A'): 10,
        ('A', 'EOS'): 10
    }
    pos_2gram = (bnode['entry']['pos'], cnode['entry']['pos'])
    return cnode['entry']['cost'] + (ctable[pos_2gram] if pos_2gram in ctable else 100)

cost_uniform = lambda bnode, cnode: 0
cost_morpheme_num = lambda bnode, cnode: 1
jiritsugo = set(['N', 'V'])
cost_bunsetsu_num = lambda bnode, cnode: 1 if cnode['entry']['pos'].split('-')[0] in jiritsugo else 0

# res = analyze_simple(matrie, u"かれのくるまでまつ", is_connective,  cost_minimum)
# res = analyze(matrie2, u"このひとことでげんきになった", is_connective,  cost_minimum)
res = analyze(matrie2, u"このひとことでげんきになった", lambda x,y: True,  cost_bunsetsu_num)
print '\n'.join('/'.join(sent) for sent in res)
