#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(SERVER_SETTINGS['host'], SERVER_SETTINGS['port'])
