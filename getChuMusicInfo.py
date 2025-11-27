import requests
import json
import sys
import io

# 强制标准流使用 UTF-8 编码
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def getChunithmSongs():
    # API地址
    url = "https://maimai.lxns.net/api/v0/chunithm/song/list"
    # 添加参数 notes=true
    params = {"notes": "true"}
    
    try:
        # 发送GET请求（通过params传递查询参数）
        response = requests.get(url, params=params, timeout=30)  # 超时时间延长至30秒（可能返回数据更大）
        # 检查响应状态码
        response.raise_for_status()
        
        # 解析JSON数据
        songData = response.json()
        
        return songData
    
    except requests.exceptions.RequestException as e:
        return f"请求失败：{e}"
    except json.JSONDecodeError:
        return "JSON解析失败"
    except Exception as e:
        return f"未知错误：{e}"

def getChunithmSongAliasNameList():
    # api地址
    url = "https://maimai.lxns.net/api/v0/chunithm/alias/list"
    try:
        # 发送GET请求
        response = requests.get(url, timeout=30)
        # 检查响应状态码
        response.raise_for_status()
        
        # 解析JSON数据
        aliasData = response.json()
        
        return aliasData
    
    except requests.exceptions.RequestException as e:
        return f"请求失败：{e}"
    except json.JSONDecodeError:
        return "JSON解析失败"
    except Exception as e:
        return f"未知错误：{e}"

songId = ""

def searchChunithmSong(name):
    try:
        # 调用getChunithmSongs()函数获取所有歌曲信息
        songData = getChunithmSongs()["songs"]
        # 调用getChunithmSongAliasNameList()函数获取所有别名信息
        songAliasData = getChunithmSongAliasNameList()["aliases"]
    except:
        return songData

    global songId

    for song in songData:
        if song["title"] == name:
            songId = song["id"]
            # 难度解析
            difficulty = ""
            charter = ""
            detailedDifficulty = ""
            for d in song["difficulties"]:
                difficulty += f"{d['level']}/"
                charter += f"{d['note_designer']}/"
                detailedDifficulty += f"{d['level_value']}/"
            difficulty = difficulty[:-1]
            charter = charter[:-1]
            detailedDifficulty = detailedDifficulty[:-1]
            songInfo =  (
                f"\n曲名：{song['title']}"
                f"\nid：{song['id']}"
                f"\n艺术家：{song['artist']}"
                f"\n分类：{song['genre']}"
                f"\nbpm：{song['bpm']}"
                f"\n定数：{difficulty}"
                f"\n详细定数：{detailedDifficulty}"
                f"\n谱师：{charter}"
            )
            return  songInfo
    for alias in songAliasData:
        if name in alias["aliases"]:
            for song in songData:
                if song["id"] == alias["song_id"]:
                    songId = song["id"]
                    # 难度解析
                    difficulty = ""
                    charter = ""
                    detailedDifficulty = ""
                    for d in song["difficulties"]:
                        difficulty += f"{d['level']}/"
                        charter += f"{d['note_designer']}/"
                        detailedDifficulty += f"{d['level_value']}/"
                    difficulty = difficulty[:-1]
                    charter = charter[:-1]
                    detailedDifficulty = detailedDifficulty[:-1]
                    songInfo =  (
                        f"\n曲名：{song['title']}"
                        f"\nid：{song['id']}"
                        f"\n艺术家：{song['artist']}"
                        f"\n分类：{song['genre']}"
                        f"\nbpm：{song['bpm']}"
                        f"\n定数：{difficulty}"
                        f"\n详细定数：{detailedDifficulty}"
                        f"\n谱师：{charter}\n"
                    )
                    return  songInfo
    return "未找到歌曲：" + name

async def sedMusicInfoByName(msg, group_id, user_id, bot, MessageArray, Record):
    global songId
    if msg.endswith("是什么歌"):
        musicName = msg[:-4]
        answer = searchChunithmSong(musicName)
        if songId == "":
            await bot.api.post_group_msg(group_id, text="\n未搜索到歌曲：" + msg[:-4], at=user_id)
            return
        await bot.api.post_group_msg(group_id, rtf=MessageArray().add_text(answer).add_image(f"https://assets2.lxns.net/chunithm/jacket/{songId}.png"), at=user_id)
        # await bot.api.post_group_msg(group_id,rtf=MessageArray().add_record(f"https://assets2.lxns.net/chunithm/music/{songId}.mp3"))
        await bot.api.send_group_file(group_id, f"https://assets2.lxns.net/chunithm/music/{songId}.mp3", name=f"{songId}.mp3")
        record = Record(f"https://assets2.lxns.net/chunithm/music/{songId}.mp3")
        await bot.api.post_group_msg(group_id, rtf=MessageArray().add_by_segment(record))
        # await bot.api.send_group_image(group_id, f"https://assets2.lxns.net/chunithm/jacket/{songId}.png")
        # await bot.api.post_group_msg(group_id, rtf=MessageArray().add_image(f"https://assets2.lxns.net/chunithm/jacket/{songId}.png"))
        # await bot.api.post_group_record(group_id, f"https://assets2.lxns.net/chunithm/music/{songId}.mp3")
        # print(answer)
        songId = ""