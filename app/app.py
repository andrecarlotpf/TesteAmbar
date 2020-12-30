#!/usr/bin/env python
# -*- coding: utf-8 -*-
import database as db
import requests as rq
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

token = None
with open('keys','r') as f:
    token = f.readline()

base = 'http://apiadvisor.climatempo.com.br/api/v1'


def url_maker(id: int):
    params = '/forecast/locale/%d/days/15?token=%s' % (id, token)
    return base+params

@app.route('/start_database')
def init_database():
    if db.create_database():
        return jsonify({'status':'200'})


@app.route('/api/cidade/<int:id>/', methods=['POST', 'GET'])
def sync_forecast(id: int=None):
    if request.method == 'POST':
        r = rq.get(url_maker(id))
        if db.insert_into_db(r.json()):
            return jsonify({'status':200})
    else:
        abort(501, description='Url only receive POST')

@app.route('/api/analise/', methods=['POST','GET'])
def analise():
    if request.method == 'GET':
        data_inicial = request.args.get('data_inicial')
        data_final = request.args.get('data_final')
        return jsonify({"result":db.analise(data_inicial, data_final)})
     

if __name__ == '__main__':
    app.run(debug=True)
