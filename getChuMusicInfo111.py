import requests
import sys
import io
import os
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class ChuMusicInfo:
    def __init__(self):
        self.cover = None

    async def getMusicInfo(self, text:str , group_id, user_id, bot):
        if text.startswith("搜歌"):
            data = text[3:]
            musicName = data
            # return self.getJson(musicName)
            answer = self.getJson(musicName)
            await bot.api.post_group_msg(group_id, image=self.cover, text=answer)
            
    def getJson(self, name):
        # 发送 HTTP GET 请求
        url = 'https://chunithm.sega.jp/storage/json/music.json'
        response = requests.get(url)
        if response.status_code == 200:
            musicJson =  response.json()
            for music in musicJson:
                if music['title'] == name:
                    answer = f"id：{music['id']}\n名称：{music['title']}\n分类：{music['catname']}\n难度绿：{music['lev_bas']}\n难度橙：{music['lev_adv']}\n难度红：{music['lev_exp']}\n难度紫：{music['lev_mas']}\n难度彩：{music['lev_ult']}"
                    self.cover = 'https://new.chunithm-net.com/chuni-mobile/html/mobile/img/' + music['image']
                    return answer
                if os.path.exists("musicOtherName.json"):
                    with open("musicOtherName.json", "r", encoding="utf-8") as f:
                        musicOtherNameJson = json.load(f)
                        for fullName in musicOtherNameJson:
                            for otherName in musicOtherNameJson[fullName]["otherName"]:
                                if otherName == name:
                                    if musicOtherNameJson[fullName]["id"] == music['id']:
                                        answer = f"id：{musicOtherNameJson[fullName]['id']}\n名称：{fullName}\n分类：{music['catname']}\n难度绿：{music['lev_bas']}\n难度橙：{music['lev_adv']}\n难度红：{music['lev_exp']}\n难度紫：{music['lev_mas']}\n难度彩：{music['lev_ult']}"
                                        self.cover = 'https://new.chunithm-net.com/chuni-mobile/html/mobile/img/' + music['image']
                                        return answer
            return "未找到歌曲:" + name
        else:
            return "获取失败"
        
    def writeMusicOtherName(self, text:str):
        if text.startswith("别名设置"):
            data = text[5:].split("  ")
            name = data[0]
            otherName = data[1]
            url = 'https://chunithm.sega.jp/storage/json/music.json'
            response = requests.get(url)
            if response.status_code == 200:
                musicJson =  response.json()
                for music in musicJson:
                    if music['title'] == name:
                        if os.path.exists("musicOtherName.json"):
                            with open("musicOtherName.json", "r", encoding="utf-8") as f:
                                musicOtherNameJson = json.load(f)
                                if name in musicOtherNameJson:
                                    musicOtherNameJson[name]["otherName"].append(otherName)
                                else:
                                    musicOtherNameJson[name] = {}
                                    musicOtherNameJson[name]["otherName"] = []
                                    musicOtherNameJson[name]["otherName"].append(otherName)
                                    musicOtherNameJson[name]["id"] = music['id']
                                with open("musicOtherName.json", "w", encoding="utf-8") as f:
                                    json.dump(musicOtherNameJson, f, ensure_ascii=False, indent=4)
                        else:
                            with open("musicOtherName.json", "w", encoding="utf-8") as f:
                                musicOtherNameJson = {}
                                musicOtherNameJson[name] = {}
                                musicOtherNameJson[name]["otherName"] = []
                                musicOtherNameJson[name]["otherName"].append(otherName)
                                musicOtherNameJson[name]["id"] = music['id']
                                json.dump(musicOtherNameJson, f, ensure_ascii=False, indent=4)
                        return "别名设置成功"
                return "歌曲全名错误"

        