# -*- coding:utf-8 -*-
"""
@author: ZCHENG
@file: move.py
@time: 14:55
@decs: 该脚本用于归档指定的文件夹至移动硬盘
python autocopy.py --src D:\ --dst F:\20221219
"""
import os
import shutil
import argparse
import csv

def argv_parse():
    parser = argparse.ArgumentParser(description='该脚本用于归档文件夹')
    parser.add_argument('--src', help="source directory.", default=False, required=True)
    parser.add_argument('--dst', help="source directory.", default=False, required=True)
    return parser.parse_args()

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    with open(r'D:\\flist.csv', 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        for row in reader:
            shutil.copytree(os.path.join(src, row[0]), os.path.join(dst, row[0]))

if __name__ == "__main__":
    args = argv_parse()
    copy_directory(args.src, args.dst)
