#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-9-20

"""
验证函数
 若请求成功,则返回响应时间, ip
若错误, 则返回None, None, 请求框架将不对这一结果进行处理

"""
import requests
import urlparse

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


def valid(_args, dont_filter):
    url = _args.get('url')
    header['Host'] = urlparse.urlparse(url).netloc
    time_out = _args.get('time_out')
    _ip = _args.get('ip')
    diy_header = _args.get('diy_header') if _args.get('diy_header') else header

    try:
        proxy = {
            'http': 'http://%s' % _ip,
            'https': 'http://%s' % _ip
        }
        con = requests.get(url, headers=diy_header, proxies=proxy, timeout=time_out)
    except Exception,e:
        # print e
        return None, None
    else:
        if con.status_code == 200:
            return con.elapsed.microseconds/1000000.,  _ip