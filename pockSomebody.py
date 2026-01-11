async def pockSomebody(msg, group_id, user_id, bot):
    if msg.startswith("戳我"):
        if "次" in msg:
            msg = msg[:-1]
        times = msg[2:]
        if times == "":
            times = 1
        else:
            times = int(times)
        if times > 0:
            for i in range(times):
                await bot.api.send_poke(group_id=group_id, user_id=user_id)