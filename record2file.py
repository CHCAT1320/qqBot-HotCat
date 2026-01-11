from ncatbot.core.event.message_segment import Record, Reply
import requests
import asyncio
import aiohttp
import base64
import os
from asyncio.subprocess import PIPE

boti = None
group_idi = None

async def record2file(bot, group_id, user_id, msg):
    url = ""
    for i in msg.message:
        if isinstance(i, Reply):
            replyMsg = await bot.api.get_msg(i.id)
            for j in replyMsg.message:
                if isinstance(j, Record):
                    url = j.url
                    global boti
                    boti = bot
                    global group_idi
                    group_idi = group_id
                    try:
                        await bot.api.post_group_msg(group_id, text=f"收到！正在下载语音文件{url}", at=user_id)
                        await bot.api.send_group_file(group_id, await record2wav(await downloadRecord(url)), name=f"{replyMsg.message_id}.wav")
                    except Exception as e:
                        # await bot.api.post_group_msg(group_id, text=f"下载语音文件失败:{await record2wav(await downloadRecord(url))}", at=user_id)
                        await bot.api.post_group_msg(group_id, text=f"下载语音文件失败:{e}", at=user_id)
                    boti = None
                    group_idi = None

import aiohttp
import asyncio
import base64
import os
import sys
from io import BytesIO

# 全局变量（请根据实际情况赋值）
# group_idi = None  # 你的群ID
# boti = None       # 你的机器人实例

# ==================== 核心配置：ffmpeg 路径 ====================
def get_ffmpeg_path():
    """获取 ffmpeg 绝对路径并校验"""
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    ffmpeg_path = os.path.join(script_dir, "napcat", "ffmpeg", "ffmpeg.exe")
    # 校验文件是否存在
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg 不存在：{ffmpeg_path}")
    return ffmpeg_path

FFMPEG_ABS_PATH = get_ffmpeg_path()

# ==================== 1. 异步下载 ARM 音频 ====================
async def downloadRecord(url):
    """异步下载ARM音频二进制数据"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=30),
                # headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            ) as response:
                response.raise_for_status()
                return await response.read()
    except (aiohttp.ClientError, asyncio.TimeoutError, Exception) as e:
        if boti and group_idi:
            await boti.api.post_group_msg(group_id=group_idi, text=f"下载语音文件失败:{e}")
        # return None

# ==================== 2. ARM 转 WAV 生成 DataURL ====================
async def record2wav(audio_data):
    """
    ARM音频转WAV格式，不生成临时文件，返回DataURL
    :param audio_data: ARM 音频二进制数据
    :return: WAV DataURL / None
    """
    # 1. 校验输入数据
    if not audio_data:
        if boti and group_idi:
            await boti.api.post_group_msg(group_id=group_idi, text="ARM音频数据为空，无法转换")
        return None

    # 2. 校验 ffmpeg 路径
    if not os.path.exists(FFMPEG_ABS_PATH):
        err_msg = f"ffmpeg 文件不存在：{FFMPEG_ABS_PATH}"
        if boti and group_idi:
            await boti.api.post_group_msg(group_id=group_idi, text=err_msg)
        return None

    try:
        # 3. 构造 ffmpeg 命令（纯内存流转码，无临时文件）
        cmd = [
            FFMPEG_ABS_PATH,
            "-i", "pipe:0",          # 从标准输入读取 ARM 数据
            "-f", "wav",             # 输出格式为 WAV
            "-acodec", "pcm_s16le",  # WAV 编码格式
            "-ar", "8000",           # 采样率 8000Hz（匹配 ARM 标准）
            "-ac", "1",              # 单声道
            "-y",                    # 强制覆盖（无文件，仅占位）
            "pipe:1"                 # 输出到标准输出
        ]

        # 4. 异步执行 ffmpeg 命令
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate(input=audio_data)

        # 5. 校验转码结果
        if proc.returncode != 0:
            err_msg = f"ffmpeg 转码失败：{stderr.decode('utf-8')}"
            if boti and group_idi:
                await boti.api.post_group_msg(group_id=group_idi, text=err_msg)
            return None

        # 6. 生成 DataURL
        wav_base64 = base64.b64encode(stdout).decode("utf-8")
        return f"data:audio/wav;base64,{wav_base64}"

    except Exception as e:
        err_msg = f"ARM转WAV异常：{str(e)}"
        if boti and group_idi:
            await boti.api.post_group_msg(group_id=group_idi, text=err_msg)
        return None