#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys; sys.path.insert(0, 'libs')

from collections import Counter
import os

from flask import Flask, jsonify, render_template, redirect, request, url_for
from konlpy.corpus import kolaw
from konlpy.tag import Hannanum, Kkma, Mecab

from settings import SERVER_SETTINGS


HERE = os.path.abspath(os.path.dirname(__file__))
with open('%s/templates/default.svg' % HERE, 'r') as f:
    default_tags = f.read().decode('utf-8')


def get_tags(text, ntags=50):
    t = Hannanum()
    nouns = t.nouns(text)
    count = Counter(nouns)
    multiplier = max(1, 100 / count.most_common(1)[0][1])
    tags = [{ 'text': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]
    return tags


def create_app():
    app = Flask(__name__)
    app.debug = SERVER_SETTINGS['debug']

    @app.route('/')
    def home():
        text = kolaw.open('constitution.txt').read()
        return render_template('home.html',\
               placeholder=text, tags=default_tags)

    @app.route('/_cloudify')
    def cloudify():
        text = request.args.get('text', '', type=unicode)
        return jsonify(tags=get_tags(text))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(SERVER_SETTINGS['host'], SERVER_SETTINGS['port'])
