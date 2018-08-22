#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2018/8/21 18:03
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2018/8/21 13:13

import jike
import time
import os

c = jike.JikeClient()
i = 300
while True:
    try:
        topic_selected = c.get_topic_selected(topic_id='5701d10d5002b912000e588d')
        print('\nsucceed  '+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        os._exit(0)
    except BaseException as e:
        print('\nfailed:  '+str(e)+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        print('time: '+str(i))
        time.sleep(i)
        i = i + 30