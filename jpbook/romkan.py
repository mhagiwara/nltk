#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re

#
# Ruby/Romkan - a Romaji <-> Kana conversion library for Ruby.
#
# Copyright (C) 2001 Satoru Takabayashi <satoru@namazu.org>
#     All rights reserved.
#     This is free software with ABSOLUTELY NO WARRANTY.
#
# You can redistribute it and/or modify it under the terms of 
# the Ruby's licence.
#
# NOTE: Ruby/Romkan can work only with EUC_JP encoding. ($KCODE="e")
#

# This table is imported from KAKASI <http://kakasi.namazu.org/> and modified.

def pairs(arr, size=2):
    for i in range(0, len(arr)-1, size):
        yield arr[i:i+size]

KUNREITAB = u"""ァ	xa	ア	a	ィ	xi	イ	i	ゥ	xu
ウ	u	ヴ	vu	ヴァ	va	ヴィ	vi 	ヴェ	ve
ヴォ	vo	ェ	xe	エ	e	ォ	xo	オ	o 

カ	ka	ガ	ga	キ	ki	キャ	kya	キュ	kyu 
キョ	kyo	ギ	gi	ギャ	gya	ギュ	gyu	ギョ	gyo 
ク	ku	グ	gu	ケ	ke	ゲ	ge	コ	ko
ゴ	go 

サ	sa	ザ	za	シ	si	シャ	sya	シュ	syu 
ショ	syo	シェ    sye
ジ	zi	ジャ	zya	ジュ	zyu	ジョ	zyo 
ス	su	ズ	zu	セ	se	ゼ	ze	ソ	so
ゾ	zo 

タ	ta	ダ	da	チ	ti	チャ	tya	チュ	tyu 
チョ	tyo	ヂ	di	ヂャ	dya	ヂュ	dyu	ヂョ	dyo 
ティ    ti

ッ	xtu 
ッヴ	vvu	ッヴァ	vva	ッヴィ	vvi 
ッヴェ	vve	ッヴォ	vvo 
ッカ	kka	ッガ	gga	ッキ	kki	ッキャ	kkya 
ッキュ	kkyu	ッキョ	kkyo	ッギ	ggi	ッギャ	ggya 
ッギュ	ggyu	ッギョ	ggyo	ック	kku	ッグ	ggu 
ッケ	kke	ッゲ	gge	ッコ	kko	ッゴ	ggo	ッサ	ssa 
ッザ	zza	ッシ	ssi	ッシャ	ssya 
ッシュ	ssyu	ッショ	ssho	ッシェ	ssye
ッジ	zzi	ッジャ	zzya	ッジュ	zzyu	ッジョ	zzyo
ッス	ssu	ッズ	zzu	ッセ	sse	ッゼ	zze	ッソ	sso 
ッゾ	zzo	ッタ	tta	ッダ	dda	ッチ	tti     ッティ  tti
ッチャ	ttya	ッチュ	ttyu	ッチョ	ttyo	ッヂ	ddi 
ッヂャ	ddya	ッヂュ	ddyu	ッヂョ	ddyo	ッツ	ttu 
ッヅ	ddu	ッテ	tte	ッデ	dde	ット	tto	ッド	ddo 
ッドゥ  ddu
ッハ	hha	ッバ	bba	ッパ	ppa	ッヒ	hhi 
ッヒャ	hhya	ッヒュ	hhyu	ッヒョ	hhyo	ッビ	bbi 
ッビャ	bbya	ッビュ	bbyu	ッビョ	bbyo	ッピ	ppi 
ッピャ	ppya	ッピュ	ppyu	ッピョ	ppyo	ッフ	hhu     ッフュ  ffu
ッファ	ffa	ッフィ	ffi	ッフェ	ffe	ッフォ	ffo 
ッブ	bbu	ップ	ppu	ッヘ	hhe	ッベ	bbe	ッペ    ppe
ッホ	hho	ッボ	bbo	ッポ	ppo	ッヤ	yya	ッユ	yyu 
ッヨ	yyo	ッラ	rra	ッリ	rri	ッリャ	rrya 
ッリュ	rryu	ッリョ	rryo	ッル	rru	ッレ	rre 
ッロ	rro 

ツ	tu	ヅ	du	テ	te	デ	de	ト	to
ド	do      ドゥ    du

ナ	na	ニ	ni	ニャ	nya	ニュ	nyu	ニョ	nyo 
ヌ	nu	ネ	ne	ノ	no 

ハ	ha	バ	ba	パ	pa	ヒ	hi	ヒャ	hya 
ヒュ	hyu	ヒョ	hyo	ビ	bi	ビャ	bya	ビュ	byu 
ビョ	byo	ピ	pi	ピャ	pya	ピュ	pyu	ピョ	pyo 
フ	hu	ファ	fa	フィ	fi	フェ	fe	フォ	fo
フュ    fu
ブ	bu	プ	pu	ヘ	he	ベ	be	ペ	pe
ホ	ho	ボ	bo	ポ	po 

マ	ma	ミ	mi	ミャ	mya	ミュ	myu	ミョ	myo 
ム	mu	メ	me	モ	mo 

ャ	xya	ヤ	ya	ュ	xyu	ユ	yu	ョ	xyo
ヨ	yo

ラ	ra	リ	ri	リャ	rya	リュ	ryu	リョ	ryo 
ル	ru	レ	re	ロ	ro 

ヮ	xwa	ワ	wa	ウィ    wi      ヰ	wi	ヱ	we      ウェ	we
ヲ	wo	ウォ    wo      ン	n 

ン     n'
ディ   dyi
ー     -
チェ    tye
ッチェ	ttye
ジェ	zye
"""

HEPBURNTAB = u"""ァ	xa	ア	a	ィ	xi	イ	i	ゥ	xu
ウ	u	ヴ	vu	ヴァ	va	ヴィ	vi	ヴェ	ve
ヴォ	vo	ェ	xe	エ	e	ォ	xo	オ	o
	

カ	ka	ガ	ga	キ	ki	キャ	kya	キュ	kyu
キョ	kyo	ギ	gi	ギャ	gya	ギュ	gyu	ギョ	gyo
ク	ku	グ	gu	ケ	ke	ゲ	ge	コ	ko
ゴ	go	

サ	sa	ザ	za	シ	shi	シャ	sha	シュ	shu
ショ	sho	シェ    she
ジ	ji	ジャ	ja	ジュ	ju	ジョ	jo
ス	su	ズ	zu	セ	se	ゼ	ze	ソ	so
ゾ	zo

タ	ta	ダ	da	チ	chi	チャ	cha	チュ	chu
チョ	cho	ヂ	di	ヂャ	dya	ヂュ	dyu	ヂョ	dyo
ティ    ti

ッ	xtsu	
ッヴ	vvu	ッヴァ	vva	ッヴィ	vvi	
ッヴェ	vve	ッヴォ	vvo	
ッカ	kka	ッガ	gga	ッキ	kki	ッキャ	kkya	
ッキュ	kkyu	ッキョ	kkyo	ッギ	ggi	ッギャ	ggya	
ッギュ	ggyu	ッギョ	ggyo	ック	kku	ッグ	ggu	
ッケ	kke	ッゲ	gge	ッコ	kko	ッゴ	ggo	ッサ	ssa
ッザ	zza	ッシ	sshi	ッシャ	ssha	
ッシュ	sshu	ッショ	ssho	ッシェ  sshe
ッジ	jji	ッジャ	jja	ッジュ	jju	ッジョ	jjo	
ッス	ssu	ッズ	zzu	ッセ	sse	ッゼ	zze	ッソ	sso
ッゾ	zzo	ッタ	tta	ッダ	dda	ッチ	cchi	ッティ  tti
ッチャ	ccha	ッチュ	cchu	ッチョ	ccho	ッヂ	ddi	
ッヂャ	ddya	ッヂュ	ddyu	ッヂョ	ddyo	ッツ	ttsu	
ッヅ	ddu	ッテ	tte	ッデ	dde	ット	tto	ッド	ddo
ッドゥ  ddu
ッハ	hha	ッバ	bba	ッパ	ppa	ッヒ	hhi	
ッヒャ	hhya	ッヒュ	hhyu	ッヒョ	hhyo	ッビ	bbi	
ッビャ	bbya	ッビュ	bbyu	ッビョ	bbyo	ッピ	ppi	
ッピャ	ppya	ッピュ	ppyu	ッピョ	ppyo	ッフ	ffu     ッフュ  ffu
ッファ	ffa	ッフィ	ffi	ッフェ	ffe	ッフォ	ffo	
ッブ	bbu	ップ	ppu	ッヘ	hhe	ッベ	bbe	ッペ	ppe
ッホ	hho	ッボ	bbo	ッポ	ppo	ッヤ	yya	ッユ	yyu
ッヨ	yyo	ッラ	rra	ッリ	rri	ッリャ	rrya	
ッリュ	rryu	ッリョ	rryo	ッル	rru	ッレ	rre	
ッロ	rro	

ツ	tsu	ヅ	du	テ	te	デ	de	ト	to
ド	do      ドゥ    du

ナ	na	ニ	ni	ニャ	nya	ニュ	nyu	ニョ	nyo
ヌ	nu	ネ	ne	ノ	no	

ハ	ha	バ	ba	パ	pa	ヒ	hi	ヒャ	hya
ヒュ	hyu	ヒョ	hyo	ビ	bi	ビャ	bya	ビュ	byu
ビョ	byo	ピ	pi	ピャ	pya	ピュ	pyu	ピョ	pyo
フ	fu	ファ	fa	フィ	fi	フェ	fe	フォ	fo
フュ    fu
ブ	bu	プ	pu	ヘ	he	ベ	be	ペ	pe
ホ	ho	ボ	bo	ポ	po	

マ	ma	ミ	mi	ミャ	mya	ミュ	myu	ミョ	myo
ム	mu	メ	me	モ	mo

ャ	xya	ヤ	ya	ュ	xyu	ユ	yu	ョ	xyo
ヨ	yo	

ラ	ra	リ	ri	リャ	rya	リュ	ryu	リョ	ryo
ル	ru	レ	re	ロ	ro	

ヮ	xwa	ワ	wa	ウィ    wi      ヰ	wi	ヱ	we      ウェ    we
ヲ	wo	ウォ    wo      ン	n	

ン     n'
ディ   di
ー     -
チェ    che
ッチェ	cche
ジェ	je"""

KANROM = {}
ROMKAN = {}

for pair in pairs(re.split("\s+", KUNREITAB + HEPBURNTAB)):
    kana, roma = pair
    KANROM[kana] = roma
    ROMKAN[roma] = kana

# special modification
# wo -> ヲ, but ヲ/ウォ -> wo
# du -> ヅ, but ヅ/ドゥ -> du
# we -> ウェ, ウェ -> we
ROMKAN.update( {"du": u"ヅ", "di": u"ヂ", "fu": u"フ", "ti": u"チ",
                "wi": u"ウィ", "we": u"ウェ", "wo": u"ヲ" } )

# Sort in long order so that a longer Romaji sequence precedes.

_len_cmp = lambda x: -len(x)
ROMPAT = re.compile("|".join(sorted(ROMKAN.keys(), key=_len_cmp)) )

_kanpat_cmp = lambda x, y: cmp(len(y), len(x)) or cmp(len(KANROM[x]), len(KANROM[x]))
KANPAT = re.compile( u"|".join(sorted(KANROM.keys(), cmp=_kanpat_cmp )) )

KUNREI = [y for (x, y) in pairs(re.split("\s+", KUNREITAB)) ]
HEPBURN = [y for (x, y) in pairs(re.split("\s+", HEPBURNTAB) )]

KUNPAT = re.compile( u"|".join(sorted(KUNREI, key=_len_cmp)) )
HEPPAT = re.compile( u"|".join(sorted(HEPBURN, key=_len_cmp)) )

TO_HEPBURN = {}
TO_KUNREI =  {}

for kun, hep in zip(KUNREI, HEPBURN):
    TO_HEPBURN[kun] = hep
    TO_KUNREI[hep] = kun

TO_HEPBURN.update( {'ti': 'chi' })

def normalize_double_n(str):
    str = re.sub("nn", "n'", str)
    str = re.sub("n'(?=[^aiueoyn]|$)", "n", str)
    return str

def to_kana(str):
    tmp = normalize_double_n(str)
    tmp = ROMPAT.sub(lambda x: ROMKAN[x.group(0)], tmp)
    return tmp

def to_hepburn(str):
    tmp = normalize_double_n(str)
    tmp = KUNPAT.sub(lambda x: TO_HEPBURN[x.group(0)], tmp)
    return tmp

def to_kunrei(str):
    tmp = normalize_double_n(str)
    tmp = HEPPAT.sub(lambda x: TO_KUNREI[x.group(0)], tmp)
    return tmp

def to_roma(str):
    tmp = KANPAT.sub(lambda x: KANROM[x.group(0)], str)
    tmp = re.sub("n'(?=[^aeiuoyn]|$)", "n", tmp)
    return tmp

def is_consonant(str):
    return re.match("[ckgszjtdhfpbmyrwxn]", str)

def is_vowel(str):
    return re.match("[aeiou]", str)

# `z' => (za ze zi zo zu)
def expand_consonant(str):
    return [x for x in ROMKAN.keys() if re.match("^%s.$"%str, x)]

if __name__ == '__main__':
    assert to_kana("kanji") == u"カンジ"
    assert to_kana("kanzi") == u"カンジ"
    assert to_kana("kannji") == u"カンジ"
    assert to_kana("chie") == u"チエ"
    assert to_kana("tie") == u"チエ"
    assert to_kana("kyouju") == u"キョウジュ"
    assert to_kana("syuukyou") == u"シュウキョウ"
    assert to_kana("shuukyou") == u"シュウキョウ"
    assert to_kana("saichuu") == u"サイチュウ"
    assert to_kana("saityuu") == u"サイチュウ"
    assert to_kana("cheri-") == u"チェリー"
    assert to_kana("tyeri-") == u"チェリー"
    assert to_kana("shinrai") == u"シンライ"
    assert to_kana("sinrai") == u"シンライ"
    assert to_kana("hannnou") == u"ハンノウ"
    assert to_kana("han'nou") == u"ハンノウ"

    assert to_kana("wo") == u"ヲ"
    assert to_kana("we") == u"ウェ"
    assert to_kana("du") == u"ヅ"
    assert to_kana("she") == u"シェ"
    assert to_kana("di") == u"ヂ"
    assert to_kana("fu") == u"フ"
    assert to_kana("ti") == u"チ"
    assert to_kana("wi") == u"ウィ"

    assert to_hepburn("kannzi") == "kanji"
    assert to_hepburn("tie") == "chie"

    assert to_kunrei("kanji") == "kanzi"
    assert to_kunrei("chie") == "tie"

    assert to_kana("je") == u"ジェ"
    assert to_kana("e-jento") == u"エージェント"

    assert to_roma(u"カンジ") == "kanji"
    assert to_roma(u"チャウ") == "chau"
    assert to_roma(u"ハンノウ") == "han'nou"

    assert not is_consonant("a")
    assert is_consonant("k")

    assert is_vowel("a")
    assert not is_vowel("z")

    assert sorted(expand_consonant("k")) == ['ka', 'ke', 'ki', 'ko', 'ku']
    assert sorted(expand_consonant("s")) == ['sa', 'se', 'si', 'so', 'su']
    assert sorted(expand_consonant("t")) == ['ta', 'te', 'ti', 'to', 'tu']
    
    assert sorted(expand_consonant("ky")) == ['kya', 'kyo', 'kyu']
    assert sorted(expand_consonant("kk")) == ["kka", "kke", "kki", "kko", "kku"]
    assert sorted(expand_consonant("sh")) == ["sha", "she", "shi", "sho", "shu"]
    assert sorted(expand_consonant("sy")) == ["sya", "sye", "syo", "syu"]
    assert sorted(expand_consonant("ch")) == ["cha", "che", "chi", "cho", "chu"]
