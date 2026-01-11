import requests
import json
import time  # 新增：用于计算耗时

# import sys
# import io

# # 强制标准流使用 UTF-8 编码
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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

# 全局变量调整：存储所有匹配结果和耗时
matched_songs = []
search_time = 0.0

def searchChunithmSong(query):
    global matched_songs, search_time
    matched_songs = []
    start_time = time.time()  # 记录开始时间
    
    try:
        # 获取歌曲和别名数据
        songData = getChunithmSongs()["songs"]
        songAliasData = getChunithmSongAliasNameList()["aliases"]
    except Exception as e:
        search_time = time.time() - start_time
        return f"数据获取失败：{str(e)}"

    query_clean = query.lower().replace(" ", "")
    
    # 1. 检查ID搜索格式 (id+数字)
    import re
    id_match = re.match(r'^id(\d+)$', query_clean)
    if id_match:
        target_id = int(id_match.group(1))
        for song in songData:
            if song["id"] == target_id:
                matched_songs.append(song)
                search_time = time.time() - start_time
                return format_song_detail(song)
    
    # 2. 精确匹配曲名
    for song in songData:
        if song["title"].lower().replace(" ", "") == query_clean:
            matched_songs.append(song)
            search_time = time.time() - start_time
            return format_song_detail(song)
    
    # 3. 匹配别名
    for alias in songAliasData:
        if query_clean in [item.replace(" ", "").lower() for item in alias.get("aliases", [])]:
            for song in songData:
                if song["id"] == alias["song_id"] and song not in matched_songs:
                    matched_songs.append(song)
                    search_time = time.time() - start_time
                    return format_song_detail(song)
    
    # 4. 模糊匹配（如果前面没有精确匹配到，返回多结果）
    for song in songData:
        if query_clean in song["title"].lower().replace(" ", ""):
            if song not in matched_songs:
                matched_songs.append(song)
    
    for alias in songAliasData:
        if any(query_clean in item.replace(" ", "").lower() for item in alias.get("aliases", [])):
            for song in songData:
                if song["id"] == alias["song_id"] and song not in matched_songs:
                    matched_songs.append(song)
    
    search_time = time.time() - start_time
    
    # 处理多结果
    if len(matched_songs) > 0:
        results = []
        for i, song in enumerate(matched_songs, 1):
            results.append(f"{i}. {song['title']} - {song['artist']} (ID: {song['id']})")
        return (
            "[ 中二节奏 ] 搜索结果列表\n"
            + "\n".join(results)
            + f"\n\n共找到 {len(matched_songs)} 条匹配结果"
            + "\n\n💡 提示：使用 ID 搜索可直接获取详细信息（格式：id[歌曲ID]是什么歌）"
        )
    
    # 无结果
    return f"未找到歌曲：{query}\nTips: 支持的查找方式有: 曲名、别名"

def format_song_detail(song):
    """格式化单首歌曲的详细信息"""
    difficulty = ""
    charter = ""
    detailedDifficulty = ""
    for d in song["difficulties"]:
        difficulty += f"{d['level']} / "
        charter += f"{d['note_designer']} / "
        detailedDifficulty += f"{d['level_value']} / "
    difficulty = difficulty[:-2] if difficulty else "无数据"
    charter = charter[:-2] if charter else "无数据"
    detailedDifficulty = detailedDifficulty[:-2] if detailedDifficulty else "无数据"
    
    return (
        "\n[ 中二节奏 ] 曲目详情\n"
        f"\n曲名：{song['title']}"
        f"\n曲目id：{song['id']}"
        f"\n艺术家：{song['artist']}"
        f"\n分类：{song['genre']}"
        f"\nBPM：{song['bpm']}"
        f"\n定数：{difficulty}"
        f"\n详细定数：{detailedDifficulty}"
        f"\n谱师：{charter}"
    )

async def sedMusicInfoByName(msg, group_id, user_id, bot, MessageArray, Record):
    global matched_songs, search_time
    if msg.endswith("是什么歌"):
        query = msg[:-4]
        answer = searchChunithmSong(query)
        
        # 添加耗时信息
        time_info = f"\n\n搜索耗时：{search_time:.2f}秒"
        final_answer = answer + time_info
        
        if len(matched_songs) == 1:
            # 单结果：发送信息+图片+音频+语音
            song = matched_songs[0]
            song_id = song["id"]
            song_title = song["title"]
            
            # 1. 发送信息+图片（合并发送）
            await bot.api.post_group_msg(
                group_id,
                rtf=MessageArray()
                    .add_text(final_answer)
                    .add_image(f"https://assets2.lxns.net/chunithm/jacket/{song_id}.png"),
                at=user_id
            )
            
            # 2. 发送音频文件
            await bot.api.send_group_file(
                group_id,
                f"https://assets2.lxns.net/chunithm/music/{song_id}.mp3",
                name=f"{song_title}.mp3"  # 使用歌曲名作为文件名
            )
            
            # 3. 发送语音消息
            record = Record(f"https://assets2.lxns.net/chunithm/music/{song_id}.mp3")
            await bot.api.post_group_msg(
                group_id,
                rtf=MessageArray().add_by_segment(record)
            )
            
        elif len(matched_songs) > 1:
            # 多结果：只发送文字列表
            await bot.api.post_group_msg(
                group_id,
                text=final_answer,
                at=user_id
            )
            
        else:
            # 无结果：发送提示信息
            await bot.api.post_group_msg(
                group_id,
                text=final_answer + "\n如果有需要提交的别名，请到https://maimai.lxns.net/alias/vote 提交",
                at=user_id
            )
        
        # 重置全局变量
        matched_songs = []
        search_time = 0.0