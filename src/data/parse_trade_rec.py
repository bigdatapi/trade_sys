#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
def parse_trade_rec1(line,sep=None):
    res={}
    fields=[]
    if sep:
        fields=line.split(sep)
    else:
        fields=line.split("\t")

    """
    方向 代码 名称 订单价格 订单数量 交易状态 已成交 下单时间 订单类型
    """
    res["direction"]=fields[0]
    res["code"]=fields[1]
    res["name"]=fields[2]
    res["price"]=float(fields[3])
    res["num"]=int(fields[6].replace(",",""))
    res["amount"]=res["price"]*res["num"]
    res["time"]=fields[7]

    return res


