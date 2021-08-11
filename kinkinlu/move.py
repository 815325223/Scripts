# -*- coding:utf-8 -*-
"""
@author: ZCHENG
@file: move.py
@time: 14:55
@decs: 该脚本用于匹配csv文件中的姓名来操作文件夹
"""
import os
import re
import shutil
import argparse

def argv_parse():
    parser = argparse.ArgumentParser(description='该脚本用于匹配csv文件中的姓名来操作文件夹')
    parser.add_argument('--src', help="source directory.", default=False, required=True)
    parser.add_argument('--dst', help="destination directory.", default=False, required=True)
    return parser.parse_args()

def move_directory(src, dst):
    if os.path.exists(src):
        try:
            with open(r'D:\\namelist.csv', 'r', encoding='gbk') as f:
                namelist = f.read().splitlines()
                for root, dirs, files in os.walk(src):
                    first_level_dir = dirs
                    break
                for x in namelist:
                    for folder in first_level_dir:
                        if re.search(x, folder):
                            shutil.copytree(os.path.join(src, folder), os.path.join(dst, folder))
                        else:
                            continue
        except OSError as ex:
            print("Failed to operation.")
    else:
        print('Path not exists: {}'.format(src))

if __name__ == "__main__":
    args = argv_parse()
    move_directory(args.src, args.dst)
