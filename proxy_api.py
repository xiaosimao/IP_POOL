#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-9-20
"""

API

"""

import sys

sys.path.append('/home/shimeng/code/spider_framework_github_responsity')
from spider.data_save import pipeline
from db_method import DB
from flask import Flask, jsonify, request

db = DB(pipeline.db['proxy'])

app = Flask(__name__)

api_list = {
    'count': u'get the count of proxy',
    'get_one': u'get a random proxy',
    'get_all': u'get all proxy from proxy pool',
    'delete?ip=127.0.0.1:8080&target_url=https://www.baidu.com': u'delete the proxy which is unavailable',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/count/')
def count():
    num = db.total()
    msg = 'the total number is [%d]' % num
    return msg


@app.route('/get_one/')
def get():
    proxy = db.get_one()
    print proxy
    return proxy


@app.route('/get_all/')
def get_all():
    proxies = db.get_all()

    return jsonify([proxy.decode('utf8') for proxy in proxies])


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('ip')
    target_url = request.args.get('target_url')
    _id = proxy + '_' + target_url
    db.delete_one(_id)
    return 'Delete Successfully'


def run():
    app.run(host='0.0.0.0', port=22555, debug=True)


if __name__ == '__main__':
    run()
