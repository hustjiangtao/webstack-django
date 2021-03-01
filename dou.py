#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""douyin video fetch"""


import traceback
import time
import random
import logging
import requests
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict


# 需要爬取的用户信息(用户ID:(帖子标签，需要添加的版区，用户昵称))
USER_INFO = {
    # 58653085886: (u'绝地求生', u'吃鸡游戏', u'浩轩（搞笑吃鸡）', 6294866920528534200, 20),  # 浩轩（搞笑吃鸡）
    # 62955603441: (u'绝地求生', u'吃鸡游戏', u'吃鸡搞笑视频（绝地求生）', 6294866920528534200, 20),  # 吃鸡搞笑视频（绝地求生）
    # 98459103206: (u'绝地求生', u'吃鸡游戏', u'绝地求生吃鸡搞笑视频', 6294866920528534200, 20),  # 绝地求生吃鸡搞笑视频
    # 97543940715: (u'绝地求生', u'吃鸡游戏', u'叮当（搞笑游戏）', 6294866920528534200, 20),  # 叮当（搞笑游戏）
    # 58197423146: (u'王者荣耀', u'王者荣耀', u'周斌玩游戏', 6294866920528534227, 20),  # 周斌玩游戏
    # 83096184229: (u'王者荣耀', u'王者荣耀', u'王者荣耀', 6294866920528534227, 20),  # 王者荣耀
    # 59359411419: (u'王者荣耀', u'王者荣耀', u'王者荣耀林颜', 6294866920528534227, 20),  # 王者荣耀林颜
    # 72877898406: (u'王者荣耀', u'王者荣耀', u'王者荣耀创意君', 6294866920528534227, 20),  # 王者荣耀创意君
    # 76324608011: (u'手机游戏', u'手机游戏', u'剑侠世界2', 6294866920528534430, 20),  # 剑侠世界2
    # 97523645652: (u'逆水寒', u'游戏', u'逆水寒', 6294866920528534430, 20),  # 逆水寒
    # 96540684488: (u'英雄联盟', u'游戏', u'英雄联盟 陈不奶', 6294866920528535261, 20),  # 英雄联盟 陈不奶
    # 97392049171: (u'英雄联盟', u'游戏', u'英雄联盟皮肤', 6294866920528535261, 20),  # 英雄联盟皮肤
    # 99684495739: (u'游戏推荐', u'游戏', u'游戏大坑', 6294866920528535466, 20),  # 游戏大坑
    # 96752247209: (u'手机游戏', u'手机游戏', u'十三叔说游戏', 6294866920528535466, 20),  # 十三叔说游戏
    # 95910596570: (u'高能时刻', u'游戏', u'高能游戏君', 6294866920528535466, 20),  # 高能游戏君
    # 95174729341: (u'手游推荐', u'手机游戏', u'转角遇到游戏姬', 6294866920528535466, 20),  # 转角遇到游戏姬
    # 84572362452: (u'绝地求生', u'吃鸡游戏', u'娱游游戏', 6294866920528535641, 20),  # 娱游游戏
    # 65097903853: (u'绝地求生', u'吃鸡游戏', u'AK游戏解说', 6294866920528535641, 20),  # AK游戏解说
    # 95437437303: (u'绝地求生', u'吃鸡游戏', u'大吉大利今晚吃鸡', 6294866920528535641, 20),  # 大吉大利今晚吃鸡
    # 105217695785: (u'绝地求生', u'吃鸡游戏', u'小信吃鸡', 6294866920528535641, 20),  # 小信吃鸡
    # 94781593931: (u'绝地求生', u'吃鸡游戏', u'老赫晨_绝地求生搞笑吃鸡', 6294866920528535641, 20),  # 老赫晨_绝地求生搞笑吃鸡
    # 6288405877: (u'游戏介绍', u'游戏', u'EA', 6294866920528535585, 20),  # EA
    # 99820405469: (u'手游推荐', u'手机游戏', u'正经游戏', 6294866920528535585, 20),  # 正经游戏
    # 87926964055: (u'游戏CG', u'游戏', u'游戏CG君', 6294866920528535585, 20),  # 游戏CG君
    # 66311136939: (u'搞笑手游', u'手机游戏', u'游戏圈狼狗君', 6294866920528535585, 20),  # 游戏圈狼狗君
    # 101393968552: (u'手游推荐', u'手机游戏', u'闲人游戏', 6294866920528535585, 20),  # 闲人游戏
    # 98719394652: (u'各类游戏', u'0', u'4399游戏盒', 6294866920528535729, 19),  # 4399游戏盒
    # 91502407717: (u'游戏推荐', u'0', u'游戏机', 6294866920528535712, 19),  # 游戏机
    # 76789228590: (u'单机游戏', u'0', u'大型单机游戏', 6294866920528535699, 19),  # 单机游戏
    # 96752602693: (u'游戏推荐', u'0', u'7K小游戏', 6294866920528535679, 19),  # 7K小游戏
    # 97916235496: (u'游戏推荐', u'0', u'游戏咸鱼王', 6294866920528535662, 19),  # 游戏咸鱼王
    # 2018-12-11 新增12个抖音爬虫账号
    # 95353703889: (u'电影收藏馆', u'0', u'电影收藏馆', 6294866920528535017, 18),  # 电影收藏馆
    # 105589079309: (u'影视助手', u'0', u'影视助手', 6294866920528535005, 18),  # 影视助手
    # 79618345540: (u'影视先锋', u'0', u'影视先锋', 6294866920528534996, 18),  # 影视先锋
    # 98915166653: (u'影视推荐', u'0', u'影视推荐', 6294866920528534986, 18),  # 影视推荐
    # 92358919437: (u'影视集结', u'0', u'影视集结', 6294866920528534978, 18),  # 影视集结
    # 76744816914: (u'妖姬影视', u'0', u'妖姬影视', 6294866920528534971, 18),  # 妖姬影视
    # 99188838110: (u'爱泰剧爱不期', u'0', u'爱泰剧爱不期', 6294866920528534959, 18),  # 爱泰剧爱不期
    # 100581046992: (u'影视日语', u'0', u'影视日语', 6294866920528535017, 18),  # 影视日语
    # 60684729568: (u'喵妹说电影', u'0', u'喵妹说电影', 6294866920528535005, 18),  # 喵妹说电影
    # 95428519188: (u'学韩语看剧', u'0', u'学韩语看剧', 6294866920528534996, 18),  # 学韩语看剧
    # 82236995747: (u'影视推荐鸽', u'0', u'影视推荐鸽', 6294866920528534986, 18),  # 影视推荐鸽
    87131391378: (u'何小白', u'0', u'何小白', 6294866920528534978, 18),  # 何小白
}
USER_INFO = OrderedDict(sorted(USER_INFO.items(), key=lambda t: t[1][4]))

POST_TIME_CHOICE = [(25200, 36000), (43200, 86400)]
HEADERS = {
    "user-agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}


def get_all_user_videos():
    """
    逐个对用户进行视频抓取
    """
    for uid in USER_INFO.keys():
        logging.info("start for user %s" % uid)

        has_more = 1
        max_cursor = 0
        while has_more:
            content = None
            user_url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/'
            params = {
                "iid": 51054222669,
                "device_type": 'iPhone10,3',
                "user_id": uid,
                "count": 12,
                "max_cursor": max_cursor,
                "aid": 1128,
            }
            try:
                response = requests.get(url=user_url, params=params, headers=HEADERS)
                if response.status_code != 200:
                    break
                content = response.json()
                print(content)
            except Exception as e:
                logging.error(traceback.format_exc())

            if not content:
                break
            if content.get("aweme_list") and isinstance(content["aweme_list"], list):
                aweme_list = content.get('aweme_list')
                print(len(aweme_list))
                for aweme in aweme_list:
                    video = aweme.get('video')
                    if not video:
                        continue
                    video_id=aweme.get('aweme_id')
                    video_url=video.get('play_addr').get('url_list')[0]
                    video_image_url=video.get('cover').get('url_list')[0]
                    video_duration=video.get('duration')
                    video_desc = aweme.get('desc')
                    video_timestamp=aweme.get('create_time')
                    # print 'get video+++', video_id, video_url, video_image_url, video_timestamp
                    get_video_details_and_save(uid, video_id, video_url, video_image_url, video_timestamp, video_duration, video_desc)
            has_more = content.get("has_more", 0)
            max_cursor = content.get("max_cursor", 0)


def get_video_details_and_save(kuaishou_user_id, video_id, video_url, video_image_url, video_timestamp, video_duration, video_desc):
    """
    获取视频信息，并上传评论
    :param kuaishou_user_id: 快手用户ID
    :param video_id: 快手videoID
    :param video_url: 快手videoURL
    :param video_image_url: 快手图片地址
    :param video_timestamp: 视频发布时间戳
    :return:
    """
    # return
    url = video_url
    if Utils.check_video_fetch_record_exist(url):
        # print url
        logging.info("this video has been fetched, initial_video_url = %s" % url)
        return None

    # 获取视频总时间，如果视频总时间超过300秒，则不进行抓取
    if video_duration > 300 * 1000:
        return None
    video_introduction = video_desc
    video_introduction = Utils.replace_emoji(video_introduction)
    video_introduction = video_introduction or u''

    # 上传视频封面到七牛
    image_url = Utils.upload_image(video_image_url)
    # print '+++++image url', image_url
    if not image_url:
        logging.info("failed to upload video image to qiniu")
        return None
    logging.info("success save video image, image_url = %s" % image_url)

    # 上传视频到七牛
    logging.info("kuaishou video url : %s" % video_url)
    music_url, music_id = Utils.upload_video_to_qiniu('', video_url, image_url, music_type='sh-vd')
    # print '+++++video url', music_url
    if not music_url or not music_id:
        logging.info("failed to upload video to qiniu")
        return None
    logging.info("success save music, music_id = %s" % music_id)

    # 随机取得一个内部号作为发帖人,随机时间作为发帖时间
    post_user_id = USER_INFO[kuaishou_user_id][3]
    b = random.choice(POST_TIME_CHOICE)
    initial_post_datetime = datetime.fromtimestamp(video_timestamp / 1000.0)
    begin_post_datetime = datetime(2018, 8, 1, 0, 0)
    if initial_post_datetime > begin_post_datetime:
        between_days = (initial_post_datetime - begin_post_datetime).days + 1
    else:
        between_days = 0
    if between_days <= 87:
        post_time = begin_post_datetime + timedelta(days=random.randint(between_days, 87)) + timedelta(seconds=random.randint(b[0], b[1]))
    else:
        post_time = initial_post_datetime
    # 帖子标签即为抓取用户基本信息中的标签
    tag_name = USER_INFO[kuaishou_user_id][0]
    pt_tag_id = [Utils.get_tag_id_by_name(tag_name)]
    # 发往版区
    subarea_list = [120060]
    if USER_INFO[kuaishou_user_id][1] in SUBAREA_ID_FOR_DIFFERENT_TAG.keys():
        subarea_list.append(SUBAREA_ID_FOR_DIFFERENT_TAG[USER_INFO[kuaishou_user_id][1]])
    # 设置视频标题，如果有简介，取简介做标题（最多30字）
    if len(video_introduction) < 31:
        post_title = video_introduction
    else:
        post_title = video_introduction[:30] + '...'
    post_title = post_title or '%s的%s日常-%s' % (USER_INFO[kuaishou_user_id][2], tag_name, time.strftime("%Y%m%d", time.localtime(video_timestamp)))

    # 生成帖子
    post_id = Utils.convert_fetchted_info_to_post(comic_title=post_title, content=video_introduction,
                                                  user_id=post_user_id, tag=tag_name, tag_id_list=pt_tag_id,
                                                  subarea_list=subarea_list, img_links=None, music_id=music_id,
                                                  post_time=post_time, post_media_type=104, post_status=101)
    # print '+++++post id', post_id
    if not post_id:
        logging.info("failed to save post info")
        return None
    logging.info("success save post info, post_id = %s" % post_id)

    # 保存抓取记录
    Utils.add_video_fetched_record(platform=VideoFetchConst.VIDEO_FETCH_PLATFORM_DOUYIN, initial_video_url=url, initial_user_id=kuaishou_user_id, post_id=post_id)
    # 将视频添加到去水印队列
    task = {
        'music_id': music_id,
        'music_url': music_url,
        'music_image_url': image_url,
        'user_virname': INTERNAL_USER_ID_LIST[post_user_id],
        'logo_name_list': [u'抖音1', u'抖音4']
    }
    Utils.add_video_delogo_task_info(task)

    logging.info("fetch comment for post : %s" % post_id)
    has_more = 1
    cursor = 0
    comment_count = 0
    comment_time = post_time
    now_time = datetime.now()
    while has_more:
        comment_message = None
        per_page = 20
        try:
            comment_url = 'https://api.amemv.com/aweme/v2/comment/list/'
            params = {
                "aweme_id": video_id,
                "count": per_page,
                "cursor": cursor,
            }
            response = requests.get(url=comment_url, params=params, headers=HEADERS)
            time.sleep(2)
            if response.status_code != 200:
                break
            comment_message = response.json()
        except Exception as e:
            logging.error(traceback.format_exc())

        if not comment_message:
            break
        has_more = comment_message.get("has_more", 0)
        cursor = comment_message.get("cursor", cursor+per_page)
        comment_list = comment_message.get("comments")
        if not comment_list or not isinstance(comment_list, list):
            break

        msg_data_list = []
        for comment in comment_list:
            comment_content = comment.get("text", '')
            comment_content = Utils.replace_emoji(comment_content)
            if not comment_content:
                continue
            if comment_content.isdigit():
                continue
            if 'www' in comment_content or 'http' in comment_content:
                continue
            comment_user_id = random.choice(list(set(COMMENT_INTERNAL_USER_ID_LIST.keys()) - {post_user_id}))
            # 前180条评论时间保证在发帖之后3天内，其余评论时间距前一条评论时间相差2小时内的一个随机数
            # 保证评论插进去的时候按照时间递增插入
            if comment_count < 180:
                comment_time = comment_time + timedelta(seconds=random.randint(0, 1440))
            else:
                comment_time = comment_time + timedelta(seconds=random.randint(0, 7200))
            if comment_time > now_time:
                has_more = 0
                break
            comment_count += 1
            comment_id = Utils.convert_fetched_comment_to_diyidan(post_id, comment_user_id, content=comment_content,
                                                                  img_links=None, music_id=None, post_time=comment_time,
                                                                  comment_status=100, comment_audit=101,
                                                                  comment_floor_num=comment_count)
            # print '+++++comment id', comment_id
    if comment_count:
        Utils.increase_post_comment_count(post_id, comment_count)
    # 抓取每个视频之间间隔 2 秒
    time.sleep(2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("job start...")
    get_all_user_videos()
    logging.info('done.')
