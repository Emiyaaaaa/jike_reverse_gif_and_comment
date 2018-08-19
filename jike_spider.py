import jike
import pickle
from PIL import Image, ImageSequence
import urllib.request
import os

topic_id={
          '有趣的GIF动图':'5aa0c90f8e88bd00164daa3b',
          '不好笑便利店':'5701d10d5002b912000e588d'
          }
user_id_fn = 'id.list'
post_index = 7#动态下标，默认为0

c = jike.JikeClient()
topic_selected = c.get_topic_selected(topic_id='5701d10d5002b912000e588d')
#获取图片
pictures = [item['picUrl'] for item in topic_selected[post_index].pictures]
print(pictures)
#图片数量
pic_num = len(pictures)
#获取id
id = topic_selected[post_index].id

try:
    with open(user_id_fn, 'rb') as file:
        used_id = pickle.load(file)
except:
    #记录文件不存在时创建
    used_id = ['0']
    with open(user_id_fn, 'wb') as file:
        pickle.dump(used_id, file)

if id not in used_id:
    for pic in pictures:
        #gif倒放
        try:
            if pic[-3:] == 'gif':
                urllib.request.urlretrieve(pic, 'ani.gif')
        except BaseException:
            continue
        with Image.open('ani.gif') as im:
            if im.is_animated:
                frames = [f.copy() for f in ImageSequence.Iterator(im)]
        frames.reverse()
        #保存
        frames[0].save('out.gif', save_all=True, append_images=frames[1:])
        #评论
        try:
            c.comment_it('',topic_selected[post_index],pictures='out.gif',sync2personal_updates=False)
        except:
            pass
        #成功评论，将此消息id加入文件中
        used_id.append(id)
        with open(user_id_fn, 'wb') as file:
            pickle.dump(used_id, file)
