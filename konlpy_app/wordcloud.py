#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter

from konlpy.tag import Hannanum, Kkma, Mecab


def get_tags(text, ntags=50, multiplier=10):
    t = Mecab()
    nouns = t.nouns(text)
    count = Counter(nouns)
    tags = [{ 'text': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]
    return tags
