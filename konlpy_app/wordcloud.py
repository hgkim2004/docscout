#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter
import random
from string import Template

from konlpy.tag import Hannanum, Kkma, Mecab
import pytagcloud # requires Korean font support


HTML_TEMPLATE = '<style type="text/css">$css</style><ul class="cloud">$tags</ul>'
TAGS_TEMPLATE = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx;"><a class="tag %(cls)s" href="#%(tag)s" style="top: %(top)dpx; left: %(left)dpx; font-size: %(size)dpx; height: %(height)dpx; line-height:%(lh)dpx;">%(tag)s</a></li>'

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())


def draw_cloud(text, ntags=50, fontname='Noto Sans CJK', multiplier=1):
    t = Mecab()
    nouns = t.nouns(text)
    count = Counter(nouns)
    tags = [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

    data = pytagcloud.create_html_data(tags, fontname=fontname)

    context = {}
    context['tags'] = '\n'.join([TAGS_TEMPLATE % link for link in data['links']])
    context['css'] = '\n'.join(\
        "a.%(cname)s {color: %(normal)s;} a.%(cname)s:hover {color: %(hover)s;}"\
         % {'cname': k, 'normal': v[0], 'hover': v[1]}\
                                 for k, v in data['css'].items())

    return Template(HTML_TEMPLATE).substitute(context)
