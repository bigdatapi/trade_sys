#!/usr/bin/env python
# -*- encoding:utf-8 -*-


from __future__ import print_function
from __future__ import division
import sys
import MySQLdb



def _validate():
    global conn
    sql="select open_num,high_num,low_num,close_num,ohlc_time, percent,diff from tb_ohlc_hour order by ohlc_time"
    cursor=conn.cursor()
    cursor.execute(sql)
    #print(cursor.fetchone())
    #return 0
    last_close_num=None
    for row in cursor.fetchall():
        open,high,low,close,ohlc, per, diff=row
        #print(open,high,low,close,ohlc, per,diff)
        if not last_close_num:
            last_close_num=close
            continue

        new_diff=close - last_close_num
        if new_diff != diff:
            print("%s diff not match:new_diff=%d diff=%d"%(ohlc,new_diff,diff))
            last_close_num=close
            continue
        new_per=new_diff/last_close_num
        last_close_num=close
        if per and (new_per-per)/per>0.01:
            print("%s per not match:new_per=%f per=%f"%(ohlc,new_per, per))
            continue

    cursor.close()
    return 0

if __name__ == '__main__':
    conn=MySQLdb.connect(host="localhost",user="harry",passwd="harry",db="test_trade_sys",charset="utf8")
    if _validate():
        print("validate fail")
    else:
        print("validate ok")
    conn.close()
    sys.exit(0)
