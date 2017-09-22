#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-9-20

import sys
import re
import os
import time

# 这里写你自己的框架保存地址
sys.path.append('/home/shimeng/code/spider_framework_github_responsity')

from spider.tools import format_put_data
from spider.data_save import pipeline
from spider.html_parser import parser
from spider.page_downloader import aispider
from spider.threads import start, work_queue, save_queue
from spider.log_format import logger
from proxy_basic_config import url_parse_dict, target_urls,collection_name
from _request import valid


# 定义主程序
class SpiderMain(object):
    def __init__(self, ):

        self.logger = logger
        self.parser = parser
        self.pipeline = pipeline
        self.target_urls = target_urls
        self.collection_name = collection_name


    def run(self):
        start()
        self.craw()

    def craw(self, request=aispider.request):

        for key, value in url_parse_dict.iteritems():
            if value.get('status') == 'active':
                # 网站名
                website_name = key
                # 网站url
                website_urls = value.get('url')
                # 请求方法
                method = value.get('request_method')
                # 请求需要提交的数据
                post_datas = value.get('submit_data')
                # 解析方法
                parse_func = value.get('parse_func', 'system')
                if parse_func == 'system':
                    parser = self.parse_to_get_ip
                else:
                    parser = parse_func

                # 自定义头
                diy_header = value.get('header')

                for url in website_urls:
                    # 调用format_put_data 构造放入队列中的数据
                    if post_datas:
                        for post_data in post_datas:
                            put_data = format_put_data(
                                args={"url": url, "method": method, 'submit_data': post_data, 'diy_header': diy_header},
                                work_func=request,
                                follow_func=self.get_and_check,
                                meta={'value': value, 'website_name': website_name, 'parser': parser})
                            # 放入队列
                            work_queue.put(put_data)

                    else:
                        put_data = format_put_data(args={"url": url, "method": method, 'data': post_datas},
                                                   work_func=request,
                                                   follow_func=self.get_and_check,
                                                   meta={'value': value, 'website_name': website_name,
                                                         'parser': parser})
                        # 放入队列
                        work_queue.put(put_data)

    def get_and_check(self, response):
        value = response.get('meta').get('value')
        html_content = response.get('content')
        # 网站名
        website_name = response.get('meta').get('website_name')
        # 解析类型: xpath, re
        parse_type = value.get('parse_type')
        # 解析函数
        parser = response.get('meta').get('parser')

        parser(value=value, html_content=html_content, parse_type=parse_type, website_name=website_name)

    def parse_to_get_ip(self, value, html_content, parse_type, website_name):
        ips = []

        if parse_type == 'xpath':
            # xpath
            # 端口与地址是否在一起
            ip_port_together = value.get('ip_port_together')
            if ip_port_together:
                ip_and_port_xpath = value.get('parse_method').get('ip_address_and_port')
                ip_and_port = self.parser.get_data_by_xpath(html_content, ip_and_port_xpath)
                ips.extend(ip_and_port)

            else:
                ip_address_xpath = value.get('parse_method').get('ip_address')
                ip_port_xpath = value.get('parse_method').get('ip_port')

                ip_address = self.parser.get_data_by_xpath(html_content, ip_address_xpath)
                ip_port = self.parser.get_data_by_xpath(html_content, ip_port_xpath)
                for index, value in enumerate(ip_address):
                    ips.append((ip_address[index] + ':' + ip_port[index]))

        elif parse_type == 're':
            # re
            ip_and_port_pattern = value.get('parse_method').get('_pattern')
            ip_and_port = parser.get_data_by_re(html_content, ip_and_port_pattern, flags=re.S)

            if ip_and_port:
                for data in ip_and_port:
                    proxy = ':'.join(data)
                    ips.append(proxy)

        # 调用检测程序
        self.start_check(ips, website_name)

    def start_check(self, ips, website_name):
        if ips:
            # 检测
            for _ip in ips:
                for target_url in self.target_urls:
                    url = target_url
                    # 调用format_put_data 构造放入队列中的数据
                    put_data = format_put_data(args={"url": url, 'ip': _ip, 'time_out': 5}, work_func=valid,
                                               need_save=True,
                                               save_func=self.save_ip,
                                               meta={'website_name': website_name, 'target_url': target_url})
                    # 放入队列
                    work_queue.put(put_data)
        else:
            msg = 'There Are No Available From [{website_name}] Can Be Used To Check, Please Check!!!!!!!'.format(
                website_name=website_name)
            logger.error(msg)

    # 上一步中定义的保存函数
    def save_ip(self, response):
        website_name = response.get('meta').get('website_name')
        response_time = response.get('content')
        target_url = response.get('meta').get('target_url')
        _ip = response.get('url')

        msg = '[{ip}] can visit the target url [{target_url}], source is [{source}]'.format(ip=_ip,
                                                                                            target_url=target_url,
                                                                                            source=website_name)
        logger.info(msg)
        # mongodb 集合名称

        insert_data = {}

        insert_data['_id'] = _ip+'_'+target_url
        insert_data['ip'] = _ip
        insert_data['source'] = website_name
        insert_data['response_time'] = response_time
        insert_data['target_url'] = target_url

        insert_data['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S')

        # 　保存数入库　
        self.pipeline.process_item(insert_data, self.collection_name)



if __name__ == '__main__':
    # 测试代码
    spidermain = SpiderMain()
    spidermain.run()

    # blocking
    work_queue.join()
    save_queue.join()

    # finishing crawl origin ip
    logger.info('available proxy has been saved in your database, please check!')
