import requests
import base64
import os
import json


class App:
    def __init__(self):
        print('版本：2022-02-09\n'
              '用于扫描当前目录及子目录下所有 .actors 文件夹中的演员图片并上传\n')
        self.emby_server = input('请输入emby服务器地址：(http://ip:8096)\n')
        self.api_key = input('请输入api密钥：\n')
        self.fail_list = []

    def get_actor_name(self):
        # 获取程序当前文件夹路径
        work_dir = os.getcwd()

        # 遍历当前文件夹
        print('遍历当前文件夹')
        for parent, dirnames, filenames in os.walk(work_dir):
            for dirname in dirnames:
                if dirname == '.actors':
                    work_dir = os.path.join(parent, dirname)
                    print('搜索到文件夹:', work_dir)

                    # 遍历.actors文件夹
                    for parent, dirnames, filenames in os.walk(work_dir):
                        for filename in filenames:
                            if filename[-4:] == '.jpg':
                                self.file_path = os.path.join(parent, filename)
                                print('处理文件：', self.file_path)

                                # 处理演员名称
                                self.actor_name = filename.replace('_', '%20', 1)[0:-4]

                                try:
                                    app.get_actor_id()
                                except:
                                    self.fail_list.append('未找到演员 ' + self.file_path)
                                    continue

                                try:
                                    app.post_actor_image()
                                except:
                                    self.fail_list.append('上传失败 ' + self.file_path)

        # 上传失败列表
        if len(self.fail_list) != 0:
            print('\n\n上传失败：\n')
            for name in self.fail_list:
                print(name)

        input('\n请按任意键退出。')

    def get_actor_id(self):
        # 获取演员ID
        r = requests.get(
            f'{self.emby_server}/emby/Persons/{self.actor_name}?api_key={self.api_key}')
        self.actor_id = json.loads(r.text)['Id']

    def post_actor_image(self):
        # 上传图片
        with open(self.file_path, 'rb') as f:
            # 转换图片为base64编码
            b6_pic = base64.b64encode(f.read())
        url = f'{self.emby_server}/emby/Items/{self.actor_id}/Images/Primary?api_key={self.api_key}'
        headers = {'Content-Type': 'image/jpg'}
        r = requests.post(url=url, data=b6_pic, headers=headers)
        if r.status_code == 204:
            print('上传成功')
        else:
            self.fail_list.append('上传失败 ' + self.file_path)


if __name__ == '__main__':
    app = App()
    app.get_actor_name()
