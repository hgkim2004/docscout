#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from konlpy_app.app import create_app
from werkzeug import DebuggedApplication

flask_app = create_app()

if flask_app.config['DEBUG']:
    flask_app.debug = True
    flask_app = DebuggedApplication(flask_app, evalex=True)

app = flask_app
