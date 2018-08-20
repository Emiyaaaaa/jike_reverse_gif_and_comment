import jike
import pickle
from PIL import Image, ImageSequence
import urllib.request
import time

topic_id={
          '有趣的GIF动图':'5aa0c90f8e88bd00164daa3b',
          '不好笑便利店':'5701d10d5002b912000e588d'
          }


user_id_fn = 'id.list'
post_index = 0#动态下标，默认为0

c = jike.JikeClient()

for (topic,topic_id) in topic_id:
    try:
        topic_selected = c.get_topic_selected(topic_id = topic_id)
        #获取图片
        pictures = []
        for item in topic_selected[post_index].pictures:
            if item['format'] == 'gif':
                pictures.append(item['picUrl'])
        #图片数量
        pic_num = len(pictures)
    except BaseException:
        print('爬取出错！')
        continue


    def comment():
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
            msg = {}
            for i in range(pic_num):
                pic = pictures[i]
                #gif倒放
                try:
                    urllib.request.urlretrieve(pic, 'ani.gif')
                    with Image.open('ani.gif') as im:
                        if im.is_animated:
                            frames = [f.copy() for f in ImageSequence.Iterator(im)]
                    frames.reverse()
                    #保存
                    frames[0].save('out.gif', save_all=True, append_images=frames[1:])
                    #评论
                    if i != 0:
                        time.sleep(6)
                        if topic_id == topic_id['不好笑便利店']:
                            #同时转发
                            c.comment_it('',topic_selected[post_index],pictures='out.gif')
                            msg['result'+str(i)] = 'succeed'
                            msg['personal_updates'+str(i)] = 'true'
                            msg['comment_time'+str(i)] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        else:
                            #不转发
                            c.comment_it('',topic_selected[post_index],pictures='out.gif',sync2personal_updates=False)
                            msg['result' + str(i)] = 'succeed'
                            msg['personal_updates' + str(i)] = 'false'
                            msg['comment_time'+str(i)] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                except:
                    msg['result' + str(i)] = 'failed'
                    msg['comment_time' + str(i)] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    continue
                #成功评论，将此消息id加入文件中
                used_id.append(id)
                msg['id'] = str[id]
                with open(user_id_fn, 'wb') as file:
                    pickle.dump(used_id, file)

            return msg


    if pic_num != 0 and pic_num <= 3:
        msg = comment()
        #记录日志
        with open('log.txt', 'a', encoding="utf-8") as fileobject:
            fileobject.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            li = [
                  topic_selected[post_index].topic['content'],
                  topic_selected[post_index].id,
                  topic_selected[post_index].createdAt[:10]+' '+topic_selected[post_index].createdAt[11:19]
                  ]
            fileobject.write('\n\nTopic: {}\nID: {}\nRelease Time: {}'.format(*li))
            for i in range[pic_num]:
                if i == 0:
                    fileobject.write('\nGif: '+pictures[i])
                else:
                    fileobject.write('\n\t '+pictures[i])

            for i in range[pic_num]:
                if i == 0:
                    fileobject.write('\nComment Time: '+msg['result'+str(i)]+'  '+msg['comment_time'+str(i)])
                else:
                    fileobject.write('\n\t\t\t  '+msg['result'+str(i)]+'  '+msg['comment_time'+str(i)])

    time.sleep(1)