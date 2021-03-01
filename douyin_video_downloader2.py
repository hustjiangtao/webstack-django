import requests, json, re, os, sys, time
from urllib.parse import urlparse
from contextlib import closing


class DY(object):
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        self.domain = ['www.douyin.com', 'v.douyin.com', 'www.snssdk.com', 'www.amemv.com', 'www.iesdouyin.com',
                       'aweme.snssdk.com']

    def hello(self):
        print('*' * 60)
        print('\t\t抖音无水印视频下载')
        print('\t作者:hongfs(https://github.com/hongfs)')
        print('*' * 60)
        self.run()

    def run(self):
        self.share_url = input('请输入分享链接：')
        # self.share_url = 'http://v.douyin.com/7CDeV/'

        if not self.share_url:
            return self.run()

        self.share_url = self.getLocation()

        share_url_parse = urlparse(self.share_url)

        if not share_url_parse.scheme in ['http', 'https'] or not share_url_parse.netloc in self.domain:
            return self.run()

        uid = re.findall(r'\/share\/user\/(\d*)', share_url_parse.path)
        print(uid)
        if uid:
            self.uid = uid[0]
        else:
            vid = re.findall(r'\/share\/video\/(\d*)', share_url_parse.path)

            if vid:
                self.getUid(self.share_url)
            else:
                print('链接无法识别，请提交issues')
                return self.run()

        self.count = 0
        self.getUserData(self.uid)

    def getLocation(self):
        response = requests.get(self.share_url, headers=self.headers, allow_redirects=False)
        if 'Location' in response.headers.keys():
            return response.headers['Location']
        else:
            return self.share_url

    def getUid(self, url):
        response = requests.get(url, headers=self.headers)
        if not response.status_code == 200:
            return False

        uid = re.findall(r'uid?: \"(\d*)"', response.text)
        if uid:
            self.uid = uid[0]
        else:
            return False

    def getUserData(self, uid, cursor=0):
        url = 'https://www.douyin.com/aweme/v1/aweme/favorite/?user_id=%s&max_cursor=%s&count=35' % (uid, cursor)

        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        print(response.content)
        if not response.status_code == 200:
            return print('请求失败')

        data = response.json()

        if 'status_code' not in data.keys():
            return print('获取数据失败')

        if len(data['aweme_list']) == 0:
            return print('\n完成')

        self.nickname = data['aweme_list'][0]['author']['nickname']

        if cursor == 0 and self.nickname not in os.listdir():
            os.mkdir(self.nickname)

        for item in data['aweme_list']:
            if not 'video' in item.keys():
                continue

            if not self.nickname == item['author']['nickname']:
                return print('\n完成')

            video_id = item['video']['play_addr']['uri']
            video_name = item['desc'] if item['desc'] else video_id
            for c in r'\/:*?"<>|/':
                video_name = video_name.replace(c, '')
            path = os.path.join(self.nickname, video_name) + '.mp4'

            self.count = self.count + 1
            print('第' + str(self.count) + '个：')

            if os.path.isfile(path):
                print(video_name + ' -- 已存在')
                continue

            print(video_name + ' -- 下载中')
            self.download(video_id, path)

        self.getUserData(self.uid, data['max_cursor'])

    def download(self, vid, path):
        time.sleep(1)
        url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&line=0' % str(vid)
        with closing(requests.get(url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                print('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(r'' + path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        file.flush()


if __name__ == '__main__':
    dy = DY()
    dy.hello()