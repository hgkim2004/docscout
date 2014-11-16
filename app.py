#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter
import os
import time

from flask import Flask, jsonify, render_template, redirect, request, url_for
from konlpy.corpus import kolaw
from konlpy.tag import Hannanum, Kkma, Mecab
import regex

from settings import BRAND, SERVER_SETTINGS


HERE = os.path.abspath(os.path.dirname(__file__))
with open('%s/templates/default.svg' % HERE, 'r') as f:
    default_tags = f.read().decode('utf-8')


def get_tags(text, minsyl=1, ntags=10, tagger='Hannanum', posnv='N', stopwords=[]):
    if tagger:
        # FIXME: count가 맞지 않음
        tags = globals()[tagger]().pos(text)
        filtered = [t for t in tags if t[1][0] in posnv]
        words = [w + u'다' if t[0] in 'VP' else w for w, t in filtered]
    else:
        words = regex.findall(ur'[\p{Hangul}|\p{Latin}|\p{Han}]+', text)

    words = [w.lower() for w in words]
    words = [w for w in words if w not in stopwords]

    count = sorted(\
            ((k, v) for k, v in Counter(words).iteritems() if len(k)>=minsyl),\
            key=lambda x: x[1], reverse=True)

    multiplier = max(1, 100 / count[0][1])
    return [{ 'text': n, 'size': c*multiplier } for n, c in count[:ntags]]


def create_app():
    app = Flask(__name__)
    app.debug = SERVER_SETTINGS['debug']

    @app.route('/')
    def home():
        default_text= kolaw.open('constitution.txt').read()
        return render_template('home.html',\
               text=default_text, tags=default_tags)

    @app.route('/faq')
    def faq():
        return render_template('faq.html')

    @app.route('/_cloudify')
    def cloudify():
        minsyl = request.args.get('minsyl', 1, type=int)
        ntags = request.args.get('ntags', 10, type=int)
        rotated = request.args.get('rotated', 1, type=int)
        tagger = request.args.get('tagger', 'Hannanum', type=unicode)
        text = request.args.get('text', '', type=unicode)
        posnv = request.args.get('posnv', 'NPV', type=unicode)
        stopwords = request.args.get('stopwords', '', type=unicode).split(',')
        s = time.clock()
        tags = get_tags(text, minsyl, ntags, tagger, posnv, stopwords)
        return jsonify(rotated=rotated,
                       tags=tags,
                       time=time.clock()-s,
                       textlen=len(text),
                       posnv=posnv,
                       ntags=len(tags))

    @app.context_processor
    def inject_vars():
        return dict(BRAND=BRAND)

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', SERVER_SETTINGS['port']))
    app.run(SERVER_SETTINGS['host'], port)
