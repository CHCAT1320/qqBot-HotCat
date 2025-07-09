from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
from ncatbot.plugin import BasePlugin
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import random
import time
import json
import os
import unicodedata
import help
import littleFunctions
import jiting
import getGameSrc

_log = get_log()

# 设置机器人QQ号
BOT_QQ = "703263936"
config.set_bot_uin(BOT_QQ)
config.set_root("1095216448")  # 超级管理员账号
config.set_ws_uri("ws://localhost:8082")  # websocket地址
config.set_token("chcat13201145")  # token

bot = BotClient()

# 群聊消息处理
@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)

    if msg.user_id == BOT_QQ:
        return

    littleFunctionsI = littleFunctions.funcs(msg.group_id, msg.user_id)
    await bot.api.post_group_msg(msg.group_id, text=littleFunctionsI.numberAddOne(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=littleFunctionsI.bracketPair(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=littleFunctionsI.openOrCloseFuncs(msg.raw_message))
    await littleFunctionsI.why(bot, msg.raw_message)
    
    jitingI = jiting.jiting(msg.group_id, msg.user_id, msg.sender.nickname)
    await bot.api.post_group_msg(msg.group_id, text=jitingI.addJiting(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=jitingI.getJitingList(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=jitingI.setJiTingName1(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=jitingI.updateJitingMembers(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=jitingI.lookUpJiting(msg.raw_message))
    await bot.api.post_group_msg(msg.group_id, text=jitingI.deleteJiting(msg.raw_message))
    
    await bot.api.post_group_msg(msg.group_id, text=help.help(msg.raw_message))

    gameSrc = getGameSrc.getWaterFishingSrc()
    await gameSrc.get_src(bot, msg.group_id, msg.user_id, msg.raw_message)

@bot.notice_event
async def on_notice(notice):
    _log.info(notice)
    # 戳一戳回复消息列表
    pokeText = [
        "别戳我啦~", "再戳我就要生气了！", "戳我干嘛？", 
        "别戳了，你是不是喜欢我？", "我烫猫是你能戳的？",
        "你是不是想让我生气？", "你是不是在逗我？",
        "你是不是想让我开心一下？", "你是不是在找茬？",
        "你是不是在找事？","我喜欢你"
    ]

    if notice.get("sub_type") == "poke" and str(notice.get("target_id")) == BOT_QQ:
        reply_text = random.choice(pokeText)
        sender_id = notice.get("user_id")
        if "group_id" in notice:
            group_id = notice["group_id"]
            await bot.api.post_group_msg(group_id=group_id, at=sender_id, text=reply_text)
            
            if reply_text == "我烫猫是你能戳的？":
                await bot.api.set_group_ban(group_id=group_id, user_id=sender_id, duration=1*60)
            if reply_text == "别戳了，你是不是喜欢我？":
                await bot.api.send_poke(group_id=group_id, user_id=sender_id)
                await bot.api.send_like(user_id=sender_id, times=50)
            if reply_text == "我喜欢你":
                await bot.api.send_poke(group_id=group_id, user_id=sender_id)
                await bot.api.send_like(user_id=sender_id, times=50)
        else:
            await bot.api.post_private_msg(user_id=sender_id, text=reply_text)


if __name__ == "__main__":
    bot.run()