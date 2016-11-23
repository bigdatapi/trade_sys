#!/usr/bin/env python
# -*- encoding:utf-8 -*-


from __future__ import print_function
import sys
import xlrd


def _usage(arg):
    print(arg)
    sys.exit(1)

def _load_hsi(input_path, sheet_index):
    data=xlrd.open_workbook(input_path)
    table=data.sheet_by_index(int(sheet_index))

    last_date_str=None
    for row_num in xrange(1, table.nrows):
        row_list=[]
        for col_num in xrange(0, table.ncols):
            #print("row num : %d, col num : %d" % (
            #        row_num,
            #        col_num))
            row_list.append(table.cell(row_num, col_num))

        exchange_cell=row_list[0]
        date_cell=row_list[1]
        if not date_cell:
            date_cell=last_date_str
        else:
            last_date_str=date_cell
        if not date_cell:
            print("invalid date_cell for cell (%d, %d)" %
                    (row_num, col_num), sys.stderr)
            return 1

        time_cell=row_list[2]
        open_cell=row_list[3]
        high_cell=row_list[4]
        low_cell=row_list[5]
        close_cell=row_list[6]
        per_cell=row_list[7]
        diff_cell=row_list[8]
        vol_cell=row_list[9]
        amount_cell=row_list[10]

        print(exchange_cell,
                date_cell,
                time_cell,
                open_cell,
                high_cell,
                low_cell,
                close_cell,
                per_cell,
                diff_cell,
                vol_cell,
                amount_cell)
        break

    return 0


if __name__ == '__main__':
    if len(sys.argv)!=3:
        _usage("usage : %s %s %s" % (sys.argv[0],
            "path_of_hsi.xls",
            "sheet_index[0 1 2...]"))

    if not _load_hsi(sys.argv[1], sys.argv[2]):
        print('load hsi is successful')
        sys.exit(0)
    print('load hsi failed')
    sys.exit(1)
