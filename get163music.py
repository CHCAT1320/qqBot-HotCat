import requests
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')
from django.http import FileResponse
from django.shortcuts import render

def downloadFile(url):
    # 定义保存文件的路径
    file_path = "outPut/music/music.mp3"
    
    try:
        # 发起网络请求，获取文件内容
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        
        # 以二进制写模式打开文件，保存内容
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(e)

def getMusic():
    url = "https://ilygfw-musicapi.voyage200.top/search?keywords=phigros"
    try:
        # 发送 GET 请求
        response = requests.get(url)
        response.raise_for_status()
        # 解析返回的 JSON 数据
        data = response.json()
        return data["result"]["songs"]
    except requests.exceptions.RequestException as e:
        return f"请求失败\n{e}"
def getMusicUrl(id):
    url = f"https://ilygfw-musicapi.voyage200.top/song/url?id={id}"
    try:
        # 发送 GET 请求
        response = requests.get(url)
        response.raise_for_status()
        # 解析返回的 JSON 数据
        data = response.json()
        return data["data"][0]["url"]
    except requests.exceptions.RequestException as e:
        return f"请求失败\n{e}"
    
def randomMusic():
    list = getMusic()
    data = random.choice(list)
    url = getMusicUrl(data["id"])
    downloadFile(url)
    returnData = {
        "id": data["id"],
        "name": data["name"],
        "url": url
    }
    return returnData
# print(randomMusic())