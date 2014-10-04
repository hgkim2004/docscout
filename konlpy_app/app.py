#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, redirect, request, url_for
from konlpy.corpus import kolaw

from wordcloud import draw_cloud
from settings import SERVER_SETTINGS


def create_app():
    app = Flask(__name__)
    app.debug = SERVER_SETTINGS['debug']

    @app.route('/')
    def home():
        text = kolaw.open('constitution.txt').read()
        return render_template('home.html',\
               placeholder=text,
               wordcloud=draw_cloud(text))

    @app.route('/_cloudify')
    def cloudify():
        text = request.args.get('text', '', type=unicode)
        tags = draw_cloud(text)
        return jsonify(tags=tags)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(SERVER_SETTINGS['host'], SERVER_SETTINGS['port'])
