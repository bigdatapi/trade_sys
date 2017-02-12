#!/usr/bin/env python
# -*- encoding:utf-8 -*-


from __future__ import print_function
import sys
import xlrd
import MySQLdb
import traceback
import datetime



def _stat():
    global conn
    stat_dict={}
    sql="select id, code, name, direction, num, price, amount, trade_time from tb_trade_rec where amount>0 and name like '%恒指%' order by trade_time;"
    #print(sql)
    #return 1
    cursor=conn.cursor()
    ret_code=0
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        for row in res:
            id=row[0]
            code=row[1]
            name=row[2]
            direction=row[3]
            num=int(row[4])
            price=float(row[5])
            amount=int(row[6])
            trade_time=row[7]
            kk=code
            if kk in stat_dict:
                if direction==u'买入':
                    stat_dict[kk][2]+=num
                    stat_dict[kk][3]+=amount
                elif direction==u'卖出':
                    stat_dict[kk][2]-=num
                    stat_dict[kk][3]-=amount
                    if stat_dict[kk][2]==0:
                        stat_dict[kk][5]=trade_time
                        stat_dict[kk][7]=-stat_dict[kk][3]
                    elif stat_dict[kk][2]<0:
                        print("err num: %s %s"%(id,code),sys.stderr)
                        ret_code=-3
                        break
                else:
                    print("err direction: %s %s"%(id,code),sys.stderr)
                    ret_code=-2
                    break
            else:
                if direction!=u'买入':
                    print("err: buy first, then can sell %s %s"%(id,code), sys.stderr)
                    ret_code=-1
                    break
                bull_or_bear=''
                start_time=trade_time
                end_time=''
                win_or_lose=amount

                if u'牛' in name:
                    bull_or_bear='bull'
                elif u'熊' in name:
                    bull_or_bear='bear'
                stat_dict[kk]=[id,name,num,amount,start_time,end_time,bull_or_bear,win_or_lose]

    except Exception,e:
        traceback.print_exc()

    cursor.close()
    _print_stat(stat_dict)
    return ret_code

def _print_stat(stat_dict):
    dd=[]
    for k in stat_dict:
        dd.append(stat_dict[k])
    print("total len for stat_dict : %d"%len(dd))
    xx=sorted(dd,key=lambda dd:dd[7])
    print("++++++++++最大亏损前10++++++++++")
    for ii in xx[:10]:
        print("%d %s %d %d %s [%s] %s %s"%(ii[0],ii[1],ii[2],ii[3],ii[4],ii[5],ii[6],ii[7]))


    print("++++++++++最大赚钱前5++++++++++")
    for ii in xx[-5:]:
        print("%d %s %d %d %s [%s] %s %s"%(ii[0],ii[1],ii[2],ii[3],ii[4],ii[5],ii[6],ii[7]))

    w_bear_count,w_bull_count,l_bear_count,l_bull_count=0,0,0,0
    for ii in xx:
        if ii[7]<0:
            #print("xxxxxx:%s"%(ii[6]))
            if ii[6]=='bear':
                l_bear_count+=1
            elif ii[6]=='bull':
                l_bull_count+=1
        elif ii[7]>0:
            #print("yyyyyyy:%s"%(ii[6]))
            if ii[6]=='bear':
                w_bear_count+=1
            elif ii[6]=='bull':
                w_bull_count+=1

    print("++++++++++亏损中牛/熊占比++++++++++")
    print("亏损的牛证数量：%d 熊证数量：%d"%(l_bull_count,l_bear_count))
    print("++++++++++赚钱中牛/熊占比++++++++++")
    print("赚钱的牛证数量：%d 熊证数量：%d"%(w_bull_count,w_bear_count))


if __name__ == '__main__':
    conn=MySQLdb.connect(host="localhost",user="harry",passwd="harry",db="test_trade_sys",charset="utf8")
    update_counter=0
    if not _stat():
        print('stat is successful')
        conn.commit()
        conn.close()
        sys.exit(0)
    print('stat failed')
    conn.close()
    sys.exit(1)
