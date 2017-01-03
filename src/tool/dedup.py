#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
from os import listdir
from os.path import isfile, join
import os
import sys
import md5tool

def dedup(mypath):
    filter=set()
    for f in listdir(mypath):
        if not isfile(join(mypath, f)):
            continue
        f_path=join(mypath, f)
        #print(f_path)
        #continue
        md5str=md5tool.md5(f_path)
        if md5str in filter:
            print("filter : %s %s" % (f, md5str))
            continue
        print("%s"%f_path)
        filter.add(md5str)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage : %s MYPATH" % sys.argv[0], sys.stderr)
        sys.exit(1)
    dedup(sys.argv[1])
    sys.exit(0)
