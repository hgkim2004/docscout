#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, redirect, request, url_for
from konlpy.corpus import kolaw

from wordcloud import get_tags
from settings import SERVER_SETTINGS


with open('templates/default.svg', 'r') as f:
    default_tags = f.read().decode('utf-8')

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
