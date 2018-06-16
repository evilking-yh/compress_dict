#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

# 打开一个文件
fo = open("../college_struct.dict", "w")


with open('../college.dict', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        # [一-龥]
        if len(line) <= 8 or re.search(r'[^一-龥]', line) is not None:
            # fo.write(line + '\n')
            pass
        else:
            start = line[:3]
            end = line[-4:]
            num = len(line) - 7
            fo.write(start + "#" + str(num) + ',' + str(num) + "#" + end + '\n')
            print(start + "#" + str(num) + ',' + str(num) + "#" + end)

# 关闭打开的文件
fo.close()

