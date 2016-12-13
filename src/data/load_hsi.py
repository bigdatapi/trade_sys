#!/usr/bin/env python
# -*- encoding:utf-8 -*-


from __future__ import print_function
import sys
import xlrd
import MySQLdb
import traceback



def _store_db(*args):
    global conn
    global update_counter
    #print(args)
    sql="insert ignore into tb_ohlc_hour(is_exchange, hsi_type_id, open_num, high_num, low_num, close_num, ohlc_time, percent, diff, vol, amount) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(sql)
    #return 1
    cursor=conn.cursor()
    n=cursor.execute(sql, args)
    #print(n)
    if not n:
        print("dup time : %s" % args[6])
    else:
        update_counter += 1
    cursor.close()
    return 0

def _update_db(*args):
    global conn
    global update_counter
    #print(args)
    sql="update tb_ohlc_hour(is_exchange, hsi_type_id, open_num, high_num, low_num, close_num, ohlc_time, percent, diff, vol, amount) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(sql)
    #return 1
    cursor=conn.cursor()
    n=cursor.execute(sql, args)
    #print(n)
    if not n:
        print("lost time for update : %s" % args[6])
    else:
        update_counter += 1
    cursor.close()
    return 0

def _usage(arg):
    print(arg)
    sys.exit(1)

def _load_hsi(input_path, sheet_index, op_type):
    data=xlrd.open_workbook(input_path)
    table=data.sheet_by_index(int(sheet_index))

    last_date_cell=None
    for row_num in xrange(1, table.nrows):
        row_list=[]
        for col_num in xrange(0, table.ncols):
            #print("row num : %d, col num : %d" % (
            #        row_num,
            #        col_num))
            row_list.append(table.cell(row_num, col_num))

        exchange_cell=row_list[0].value
        if not exchange_cell:
            exchange_cell=0
        elif exchange_cell=='Y' or exchange_cell=='y':
            exchange_cell=1

        date_cell=row_list[1].value
        if not date_cell:
            date_cell=last_date_cell
        else:
            last_date_cell=date_cell
        if not date_cell:
            print("invalid date_cell for cell (%d, %d)" %
                    (row_num, col_num), sys.stderr)
            return 1

        date_cell=xlrd.xldate.xldate_as_datetime(date_cell, 0)

        _, _, _, hour, min, sec=xlrd.xldate_as_tuple(row_list[2].value, 0)
        date_str="%s %.2d:%.2d:%.2d" % (date_cell.strftime("%Y-%m-%d"), hour, min, sec)
        try:
            open_cell=int(row_list[3].value)
            high_cell=int(row_list[4].value)
            low_cell=int(row_list[5].value)
            close_cell=int(row_list[6].value)
            per_cell=row_list[7].value
            diff_cell=int(row_list[8].value)
            vol_cell=int(row_list[9].value)
            amount_cell=int(row_list[10].value)
            if row_list[11].value:
                update_flag=int(row_list[11].value)
            else:
                update_flag=0
            if row_list[12].value:
                inserted_flag=int(row_list[12].value)
            else:
                inserted_flag=0

        except Exception, e:
            #print(row_num,date_str)
            #traceback.print_exc()
            break

        #print(row_num,
        #        exchange_cell,
        #        date_str,
        #        open_cell,
        #        high_cell,
        #        low_cell,
        #        close_cell,
        #        per_cell,
        #        diff_cell,
        #        vol_cell,
        #        amount_cell)
        #break

        if not op_type and not inserted_flag:
            if _store_db(
                exchange_cell,
                1,
                open_cell,
                high_cell,
                low_cell,
                close_cell,
                date_str,
                per_cell,
                diff_cell,
                vol_cell,
                amount_cell):
                print("store db for row_num=%d failed" % row_num, sys.stderr)
                return 1
        elif op_type==1 and update_flag==1:
            if _update_db(exchange_cell,
                1,
                open_cell,
                high_cell,
                low_cell,
                close_cell,
                date_str,
                per_cell,
                diff_cell,
                vol_cell,
                amount_cell):
                print("update db for row_num=%d failed" % row_num, sys.stderr)
                return 2
    if not op_type:
        print("insert totally %d rows" % update_counter)
    elif op_type==1:
        print("update totally %d rows" % update_counter)

    return 0


if __name__ == '__main__':
    if len(sys.argv)!=4:
        _usage("usage : %s %s %s %s" % (sys.argv[0],
            "path_of_hsi.xls",
            "sheet_index[0 1 2...]",
            "op_type[0:insert|1:update]"))

    conn=MySQLdb.connect(host="localhost",user="harry",passwd="harry",db="test_trade_sys",charset="utf8")
    update_counter=0
    if not _load_hsi(sys.argv[1], sys.argv[2], int(sys.argv[3])):
        print('load hsi is successful')
        conn.commit()
        conn.close()
        sys.exit(0)
    print('load hsi failed')
    conn.close()
    sys.exit(1)
