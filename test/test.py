#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2018/8/21 13:13

import jike
import time
import os

c = jike.JikeClient()
j = 1
i = 15
time.sleep(600)
while True:
    try:
        topic_selected = c.get_topic_selected(topic_id='5701d10d5002b912000e588d')
        print('\nsucceed  '+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        print('NO.'+str(j) +'  time: '+str(i))
        j = j+1
        time.sleep(i)
    except BaseException as e:
        print('\nfailed:  '+str(e)+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        print('time: '+str(i))
        time.sleep(450)
        i = i + 1
        j = 0
        if i == 20:
            os._exit(1)



