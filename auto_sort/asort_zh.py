#!/usr/bin/env python3
# -*-coding: utf-8-*-
# Author : Christopher L
# Blog   : http://blog.chriscabin.com
# GitHub : https://www.github.com/chrisleegit
# File   : asort.py
# Date   : 2016/08/22 11:12
# Version: 0.1
# Description: A very simple python script that can sort items alphabetically.

from __future__ import print_function
import os
import shutil
import re


README_FILE = '../README_zh-CN.md'
TEMP_FILE = 'temp_zh.md'

# only works for those items between BEGIN and END.
BEGIN = '## 应用'
END = '## 设置'

regex = re.compile(r"[^[]*\[([^]]*)\]")

def main():
    global README_FILE

    # make sure the script can find file: README.md
    README_FILE = os.path.abspath(README_FILE)

    if not os.path.exists(README_FILE):
        print('Error: no such file or directory: {}'.format(README_FILE))
        exit(1)

    sort_enable = False
    items = list()

    print('Loading file: {}'.format(README_FILE))

    # read file: README.md
    with open(README_FILE) as infile, open(TEMP_FILE, 'w') as outfile:
        # process each line
        for line in infile:
            if not sort_enable and BEGIN in line:
                sort_enable = True

            # if sort_enable and END in line:
            #     sort_enable = False

            if sort_enable:
                # each item starts with a character '-'
                if line.startswith(('-')):
                    line = line.strip()
                    items.append(line)
                # When no more items, blank line or new header
                elif line is '\n':
                    # when we meet the next header, we should stop adding new item to the list.
                    for item in sorted(items, key=lambda x: regex.findall(x.upper())[len(regex.findall(x.upper()))-1]):
                        # write the ordered list to the temporary file.
                        print(item, file=outfile)
                    items.clear()

                    # remember to put the next header in the temporary file.
                    print(line, end='', file=outfile)
                elif line.startswith('#'):
                    sort_enable = False if END in line else True
                    print(line, end='', file=outfile)
                else:
                    print(line, end='', file=outfile)
            else:
                print(line, end='', file=outfile)

    print('Replace the original file: README_zh-CN.md')
    shutil.move(TEMP_FILE, README_FILE)


if __name__ == '__main__':
    main()

