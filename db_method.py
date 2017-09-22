#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by shimeng on 17-9-20

import random


class DB(object):
    def __init__(self, collection):
        self.collection = collection

    def get_one(self):
        _ips = []
        for _ in self.collection.find():
            _ips.append(_.get('ip'))
        return random.choice(_ips)

    def get_all(self):
        _ips = []
        for _ in self.collection.find():
            _ips.append(_.get('ip'))
        return _ips

    def delete_one(self, ip):
        self.collection.delete_one({'_id': ip})

    def total(self):
        return self.collection.count()
