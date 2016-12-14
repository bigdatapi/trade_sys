#!/usr/bin/env python
# -*- encoding:utf-8 -*-


from __future__ import print_function
import sys
import xlrd
import MySQLdb
import traceback
import datetime



def _store_db(*args):
    global conn
    global update_counter
    #print(args)
    sql="insert into tb_trade_rec(code,name,direction,num,price,amount,op_num,trade_time) values(%s, %s, %s, %s, %s, %s, %s, %s)"
    #print(sql)
    #return 1
    cursor=conn.cursor()
    n=cursor.execute(sql, args)
    #print(n)
    if not n:
        print("dup time : %s" % args[7])
    else:
        update_counter += 1
    cursor.close()
    return 0

def _usage(arg):
    print(arg)
    sys.exit(1)

def _load_hsi(input_path):
    with open(input_path, "r") as input_f:
        while True:
            line=input_f.readline()
            if not line:
                break
            line=line.strip()
            fields=line.split("\t")
            if len(fields)!=8:
                print("fields format changed",sys.stderr)
                return 1
            code,name,direction,num,price,amount,op_num,trade_time=fields
            try:
                trade_time=datetime.datetime.strptime(trade_time, "%Y/%m/%d %H:%M").strftime("%Y-%m-%d %H:%M:%S")
                num=int(num.replace(",",""))
                amount=float(amount.replace(",",""))

            except Exception, e:
                #print("trade_time : ", trade_time)
                #traceback.print_exc()
                print("filtered : ",line)
                continue

            if _store_db(
                    code,
                    name,
                    direction,
                    num,
                    price,
                    amount,
                    op_num,
                    trade_time
                ):
                print("store db for row_num=%d failed" % row_num, sys.stderr)
                return 1
        print("insert totally %d rows" % update_counter)

    return 0


if __name__ == '__main__':
    if len(sys.argv)!=2:
        _usage("usage : %s %s" % (sys.argv[0],
            "path_of_input.txt"))

    conn=MySQLdb.connect(host="localhost",user="harry",passwd="harry",db="test_trade_sys",charset="utf8")
    update_counter=0
    if not _load_hsi(sys.argv[1]):
        print('load hsi is successful')
        conn.commit()
        conn.close()
        sys.exit(0)
    print('load hsi failed')
    conn.close()
    sys.exit(1)
