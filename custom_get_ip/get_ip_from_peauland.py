#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-9-21

import json
import base64

# 因为这个网站是post方法, 所以这里需要有post_data
# 如果你确定要提交数据, 那么请定义该值为列表类型
def peauland_format_post_data():
    post_datas = []

    base_post_data = {
            'country_code': '',
            'is_clusters': '',
            'is_https': '',
            'level_type': '',
            'search_type': 'all',
            'type': '',
        }
    for i in range(1,6):
        base_post_data['page'] = i
        post_datas.append(base_post_data)

    return post_datas

# 根据网站的特殊性, 构建自定义header, 非必须.
# 如果你的代理IP获取网站对请求头有特殊的要求,就可以自定义一个,然后在proxy_basic_config.py中对该代理网站的设置header字段并赋值即可
def peauland_header():
    cookie='peuland_id=649e2152bad01e29298950671635e44a; UM_distinctid=15ea23fc7b838f-096617276fe5c1-1c2f170b-1fa400-15ea23fc7b9752; CNZZDATA1253154494=2109729896-1505960642-%7C1505960642; peuland_md5=9b941affd9b676f62ab93081f6cc9a1b; w_h=1080; w_w=1920; w_cd=24; w_a_h=1056; w_a_w=1855; PHPSESSID=mv893pclb2qhc6etu4hvbl8067; php_id=916419018'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':cookie,
        'Host': 'proxy.peuland.com',
        'Referer': 'https://proxy.peuland.com/proxy_list_by_category.htm',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

# 这里就是根据网站的特殊性自定义的解析方法, 有固定的四个参数
# 跟默认的解析方法一样, 需要将获得的ips和website_name作为参数, 然后调用SpiderMain的start_check方法
def peauland_parser(value, html_content, parse_type, website_name):
    # 获取ips , 和website_name 作为参数传到开始检测的函数中
    from get_proxies_base_spider import SpiderMain
    spider_main = SpiderMain()
    ips = []
    content = json.loads(html_content)
    datas = content.get('data')
    for data in datas:
        ip = base64.b64decode(data.get('ip'))
        port = base64.b64decode(data.get('port'))
        proxy = ip+':'+port
        ips.append(proxy)
    if ips:
        spider_main.start_check(ips, website_name)
