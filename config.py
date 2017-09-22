#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-8-17


# 爬虫名称
spider_name = 'get_ip'

# 日志设置
log_folder_name = '%s_logs' % spider_name
delete_existed_logs = True

# 请求参数设置
thread_num = 50
sleep_time = 0.5
retry_times = 10
time_out = 5
# 当use_proxy为True时，必须在请求的args中或者在配置文件中定义ip, eg: ip="120.52.72.58:80", 否则程序将报错
use_proxy = False
ip = None

# 移动端设置为 ua_type = 'mobile'
ua_type = 'pc'

# 队列顺序
FIFO = 0
# 默认提供的浏览器头包括user_agent  host, 若需要更丰富的header,可自行定定义新的header,并赋值给diy_header

diy_header = None

# 定义状态码,不在其中的均视为请求错误或异常
status_code = [200, 304, 404]

# 保存设置
# 当你定义好了host,port,database_name之后再将connect改为True
connect = True

host = 'localhost'

port = 27017

database_name = 'free_ip'
