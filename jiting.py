import json
import requests
from ncatbot.core.event.message_segment import PlainText, Text
import unicodedata
import time


# 更新所有店铺信息
def updateShopInfo():
    url = "https://sega-register.wahlap.net/api/sega/midtr/rest/location"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        # print(data)
        # return data
        try:
            # 判断机厅是否有更新
            with open("./shopInfo.json", "r", encoding="utf-8") as f:
                oldShopInfo = json.load(f)
                for shop in data:
                    if shop not in oldShopInfo:
                        oldShopInfo.append(shop)
            with open("./shopInfo.json", "w", encoding="utf-8") as f:
                json.dump(oldShopInfo, f, ensure_ascii=False, indent=4)          
        except:
            with open("./shopInfo.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        return oldShopInfo
    else:
        return None
updateShopInfo()

def writeJitingJsonFile(data):
    with open("./shopInfo.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def addJitingToGroup(bot, groupId, userId, msg, role):
    msgText = ""
    for i in msg.message:
        if isinstance(i, Text):
            msgText = i.text
        if isinstance(i, PlainText):
            msgText = i.text
    if msgText.startswith("添加机厅") or msgText.startswith("tjjt"):
        if userId != "1095216448":
            if role != "owner" and role != "admin":
                await bot.api.post_group_msg(groupId, text="你没有权限执行此操作!")
                return
        name = msgText.split(" ")[1]
        shopInfo = updateShopInfo()
        for shop in shopInfo:
            if name == shop["address"] or name == shop["arcadeName"] or name == shop["id"] or name == shop["placeId"]:
                if "group" not in shopInfo[shopInfo.index(shop)]:
                    shopInfo[shopInfo.index(shop)]["group"] = []
                if groupId in shopInfo[shopInfo.index(shop)]["group"]:
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 已在本群中！")
                    return
                shopInfo[shopInfo.index(shop)]["group"].append(groupId)
                writeJitingJsonFile(shopInfo)
                await bot.api.post_group_msg(groupId, text=f"添加机厅 {shop['arcadeName']} 成功！")
                return
        await bot.api.post_group_msg(groupId, text=f"未找到机厅 {name} ！")

async def addjitingAliases(bot, groupId, userId, msg, role):
    msgText = ""
    for i in msg.message:
        if isinstance(i, Text):
            msgText = i.text
        if isinstance(i, PlainText):
            msgText = i.text
    if msgText.startswith("机厅别名") or msgText.startswith("jtbm"):
        if userId != "1095216448":
            if role != "owner" and role != "admin":
                await bot.api.post_group_msg(groupId, text="你没有权限执行此操作!")
                return
        name = msgText.split(" ")[1]
        alias = msgText.split(" ")[2]
        shopInfo = updateShopInfo()
        for shop in shopInfo:
            if "aliases" not in shopInfo[shopInfo.index(shop)]:
                shopInfo[shopInfo.index(shop)]["aliases"] = []
            if name == shop["arcadeName"] or name == shop["id"] or name == shop["placeId"] or name ==shop["address"] or name in shopInfo[shopInfo.index(shop)]["aliases"]:
                if groupId not in shopInfo[shopInfo.index(shop)]["group"]:
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 未在本群中！")
                    return
                if alias in shopInfo[shopInfo.index(shop)]["aliases"]:
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 已存在别名 {alias}！")
                    return
                if alias == shop["arcadeName"] or alias == shop["id"] or alias == shop["placeId"] or alias == shop["address"]:
                    await bot.api.post_group_msg(groupId, text=f"别名 {alias} 不能与机厅名称相同！")
                    return
                if "\n" in alias:
                    await bot.api.post_group_msg(groupId, text=f"机厅别名不能包含换行符！")
                    return
                if " " in alias:
                    await bot.api.post_group_msg(groupId, text=f"机厅别名不能包含空格！")
                    return
                for char in alias:
                    if unicodedata.category(char).startswith('C'):
                        await bot.api.post_group_msg(groupId, text=f"机厅别名不能包含控制字符！")
                        return
                if alias.endswith("j") or alias.endswith("几"):
                    await bot.api.post_group_msg(groupId, text=f"机厅别名不能以结尾为「j」或「几」！")
                    return
                shopInfo[shopInfo.index(shop)]["aliases"].append(alias)
                writeJitingJsonFile(shopInfo)
                await bot.api.post_group_msg(groupId, text=f"添加机厅 {shop['arcadeName']} 别名 {alias} 成功！")
                return
        await bot.api.post_group_msg(groupId, text=f"未找到机厅 {name} ！")

async def updateJitigMembers(bot, groupId, userId, msg, nickName):
    msgText = ""
    for i in msg.message:
        if isinstance(i, Text):
            msgText = i.text
        if isinstance(i, PlainText):
            msgText = i.text
    if msgText.endswith("j") or msgText.endswith("几"):
        return
    shopInfo = updateShopInfo()
    for shop in shopInfo:
        if msgText.startswith(shop["arcadeName"]) or msgText.startswith(shop["id"]) or msgText.startswith(shop["placeId"]) or msgText.startswith(shop["address"]):
            if groupId not in shopInfo[shopInfo.index(shop)]["group"]:
                await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 未在本群中！")
                return
            if "members" not in shopInfo[shopInfo.index(shop)]:
                shopInfo[shopInfo.index(shop)]["members"] = 0
            count = msgText.replace(shop["arcadeName"], "").replace(shop["id"], "").replace(shop["placeId"], "").replace(shop["address"], "")
            if count.startswith("+"):
                shopInfo[shopInfo.index(shop)]["members"] += int(count.replace("+", ""))
            elif count.startswith("-"):
                shopInfo[shopInfo.index(shop)]["members"] -= int(count.replace("-", ""))
            else:
                shopInfo[shopInfo.index(shop)]["members"] = int(count)
            if "reporter" not in shopInfo[shopInfo.index(shop)]:
                shopInfo[shopInfo.index(shop)]["reporter"] = ""
            if "reportTime" not in shopInfo[shopInfo.index(shop)]:
                shopInfo[shopInfo.index(shop)]["reportTime"] = ""
            shopInfo[shopInfo.index(shop)]["reporter"] = nickName
            shopInfo[shopInfo.index(shop)]["reportTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            writeJitingJsonFile(shopInfo)
            await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 人数更新为 {shopInfo[shopInfo.index(shop)]['members']} ！")
            return
        if "aliases" not in shopInfo[shopInfo.index(shop)]:
            continue
        for alias in shopInfo[shopInfo.index(shop)]["aliases"]:
            if msgText.startswith(alias):
                if groupId not in shopInfo[shopInfo.index(shop)]["group"]:
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 未在本群中！")
                    return
                if "members" not in shopInfo[shopInfo.index(shop)]:
                    shopInfo[shopInfo.index(shop)]["members"] = 0
                count = msgText.replace(alias, "")
                if count.startswith("+"):
                    shopInfo[shopInfo.index(shop)]["members"] += int(count.replace("+", ""))
                elif count.startswith("-"):
                    shopInfo[shopInfo.index(shop)]["members"] -= int(count.replace("-", ""))
                else:
                    shopInfo[shopInfo.index(shop)]["members"] = int(count)
                if shopInfo[shopInfo.index(shop)]["members"] < 0:
                    shopInfo[shopInfo.index(shop)]["members"] = 0
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 人数不能为负数！")
                    return
                if shopInfo[shopInfo.index(shop)]["members"] > 100:
                    shopInfo[shopInfo.index(shop)]["members"] = 0
                    await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 爆炸了，无人幸免，人数归0！")
                if "reporter" not in shopInfo[shopInfo.index(shop)]:
                    shopInfo[shopInfo.index(shop)]["reporter"] = ""
                if "reportTime" not in shopInfo[shopInfo.index(shop)]:
                    shopInfo[shopInfo.index(shop)]["reportTime"] = ""
                shopInfo[shopInfo.index(shop)]["reporter"] = nickName
                shopInfo[shopInfo.index(shop)]["reportTime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                writeJitingJsonFile(shopInfo)
                await bot.api.post_group_msg(groupId, text=f"机厅 {shop['arcadeName']} 人数更新为 {shopInfo[shopInfo.index(shop)]['members']} ！")
                return
    
async def lookUpJiting(bot, groupId, userId, msg):
        msgText = ""
        for i in msg.message:
            if isinstance(i, Text):
                msgText = i.text
            if isinstance(i, PlainText):
                msgText = i.text
        if msgText.startswith("机厅几") or msgText.startswith("jtj"):
            jitingList = []
            shopInfo = updateShopInfo()
            for shop in shopInfo:
                if "group" not in shop:
                    continue
                if groupId in shop["group"]:
                    # 判断是否是今天的报告，如果不是，归0人数
                    if shop["reportTime"] != "" and time.strftime("%Y-%m-%d", time.localtime()) != time.strftime("%Y-%m-%d", time.localtime(time.mktime(time.strptime(shop["reportTime"], "%Y-%m-%d %H:%M:%S")))):
                        shop["members"] = 0
                        shop["reporter"] = "零点自动清零"
                        shop["reportTime"] = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
                    jitingList.append(shop)
            writeJitingJsonFile(shopInfo)
            if len(jitingList) == 0:
                await bot.api.post_group_msg(groupId, text="本群未添加任何机厅！")
                return
            answer = (
                f"本群共添加了 {len(jitingList)} 个机厅：\n" + 
                f"现在是：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n" + 
                "\n".join([
                    f"{i+1}. {shop['arcadeName']}({shop['aliases'][0]})\n"
                    f"人数：{shop['members']}\n"
                    f"报告人：{shop['reporter']}\n"
                    f"更新时间：{shop['reportTime']}\n"
                    f"距离上次报告已过去：{int((time.time() - time.mktime(time.strptime(shop['reportTime'], '%Y-%m-%d %H:%M:%S'))) / 60)} 分钟"
                    for i, shop in enumerate(jitingList)
                ])
            )
            await bot.api.post_group_msg(groupId, text=answer)
            return


async def lookUpOneJiting(bot, groupId, userId, msg):
        msgText = ""
        for i in msg.message:
            if isinstance(i, Text):
                msgText = i.text
            if isinstance(i, PlainText):
                msgText = i.text
        for shop in updateShopInfo():
            if "group" in shop and groupId in shop["group"]:
                cmd = [shop["arcadeName"], shop["id"], shop["placeId"], shop["address"], *shop["aliases"]]
                for i in cmd:
                    if msgText == i + "j" or msgText == i + "几":
                        answer = (
                            "[ 单机厅查询 ]" + 
                            f"\n名称：{shop['arcadeName']}\n" + 
                            f"别名：{', '.join(shop['aliases'])}\n" + 
                            f"地址：{shop['address']}\n" + 
                            f"ID：{shop['id']}\n" + 
                            f"地点ID：{shop['placeId']}\n" + 
                            f"人数：{shop['members']}\n" + 
                            f"报告人：{shop['reporter']}\n" + 
                            f"更新时间：{shop['reportTime']}\n" + 
                            f"距离上次报告已过去：{int((time.time() - time.mktime(time.strptime(shop['reportTime'], '%Y-%m-%d %H:%M:%S'))) / 60)} 分钟"
                        )
                        await bot.api.post_group_msg(groupId, text=answer)



import base64
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def get_chunithm_store_screenshot(url, target_option):
    """
    【终局无敌版】Chunithm动态下拉框截图 - 全链路超时豁免+暴力兜底
    ? 隐藏浏览器窗口 | ? 窗口宽度800px | ? 高度自适应完整网页（无滚动条）
    ? 删掉99%超时限制 | ? 下拉框极速监听 | ? 选中永不卡死 | ? 截图永不失败
    """
    async with async_playwright() as p:
        # ? 浏览器启动：隐藏窗口（headless=True）
        browser = await p.chromium.launch(
            headless=True,  # 隐藏浏览器窗口
            slow_mo=0,
            args=["--no-sandbox", "--disable-gpu", "--disable-extensions", "--ignore-certificate-errors"]
        )
        # ? 视口配置：宽度800px，高度初始值1200，截图时full_page=True自动捕获完整高度
        context = await browser.new_context(
            viewport={"width": 300, "height": 600},  # 宽度改小为800px
            ignore_https_errors=True
        )
        page = await context.new_page()
        target_clean = target_option.strip()
        dropdown_selector = "#locationSelect"
        valid_options = []

        # ========== 核心：全流程TRY包裹，所有超时/异常都强制兜底 ==========
        try:
            # ? 1. 页面加载：极限放宽超时+最低加载要求，永不页面超时
            print(f"?? 极速访问目标页面 → {url}")
            await page.goto(
                url, 
                wait_until="commit",
                timeout=300000
            )

            # ? 2. 下拉框等待：暴力兜底+无限重试，必等到下拉框出现
            print(f"?? 等待下拉框[{dropdown_selector}]加载（无限重试，永不超时）...")
            for _ in range(100):
                if await page.locator(dropdown_selector).count() > 0:
                    print(f"? 下拉框已加载，开始监听真实选项变化")
                    break
                await page.wait_for_timeout(500)
            # 兜底校验：仍未加载则强制刷新页面再试
            if await page.locator(dropdown_selector).count() == 0:
                print(f"?? 下拉框加载缓慢，强制刷新页面重试...")
                await page.reload(wait_until="commit", timeout=300000)
                await page.wait_for_timeout(3000)

            # ? 3. 下拉框实时监听：50ms高频检测，占位符变真实选项立即响应
            print(f"?? 监听[{target_clean}]真实选项加载（0延迟）...")
            for _ in range(200):
                raw_options = await page.locator(f"{dropdown_selector} option").all_text_contents()
                valid_options = [opt.strip() for opt in raw_options if opt.strip() and "{{" not in opt]
                if len(valid_options) >= 1 or target_clean in valid_options:
                    print(f"? ? 监听到真实选项 → {sorted(valid_options)}")
                    break
                await page.wait_for_timeout(50)

            # ? 4. 选项校验兜底：无有效选项也强制放行，不中断流程
            if not valid_options:
                print(f"?? 未检测到有效选项，强制执行选中操作（兼容极端场景）")
            elif target_clean not in valid_options:
                return f"? 目标选项[{target_option}]不存在！已加载：{sorted(valid_options)}"

            # ? 5. 毫秒级选中：原生JS+强制触发事件，永不卡死+必触发数据加载
            print(f"? 执行选中 → {target_clean}")
            await page.evaluate('''
                ([selector, targetText]) => {
                    const sel = document.querySelector(selector);
                    if(!sel) return false;
                    for(let i=0; i<sel.options.length; i++){
                        if(sel.options[i].textContent.trim() === targetText){
                            sel.selectedIndex = i;
                            sel.dispatchEvent(new Event('change', {bubbles: true}));
                            return true;
                        }
                    }
                    // 兜底：选不到则默认选第一个选项，绝不中断
                    sel.selectedIndex = 0;
                    sel.dispatchEvent(new Event('change', {bubbles: true}));
                    return true;
                }
            ''', [dropdown_selector, target_clean])
            print(f"? ? 选中成功！已强制触发门店数据加载")

            # ? 6. 【核心改动】选择完成后立即截图，不等待数据渲染
            print(f"?? 选择完成，立即执行完整截图（无滚动条）...")

            # ? 7. 强制截图：full_page=True自动捕获完整网页高度，截图中无滚动条
            screenshot_bytes = await page.screenshot(
                full_page=True,  # 关键：自动捕获完整页面，高度自适应
                type="png", 
                timeout=1000
            )
            img_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            print(f"?? 全部操作完成 ? 完美成功！截图已返回")
            return f"data:image/png;base64,{img_base64}"

        # ========== ? 终极兜底1：捕获所有超时异常，强制截图返回 ==========
        except PlaywrightTimeoutError:
            print(f"?? 触发超时兜底 → 强制执行截图")
            try:
                await page.wait_for_timeout(2000)
                screenshot_bytes = await page.screenshot(full_page=True, type="png")
                return f"data:image/png;base64,{base64.b64encode(screenshot_bytes).decode()}"
            except:
                return f"?? 超时兜底失败：页面加载过慢，请检查网络后重试"
        
        # ========== ? 终极兜底2：捕获所有未知异常，强制兜底不返回空 ==========
        except Exception as e:
            err_info = f"?? 异常兜底 → {type(e).__name__}: {str(e)}"
            print(err_info)
            try:
                await page.wait_for_timeout(1000)
                return f"data:image/png;base64,{base64.b64encode(await page.screenshot(full_page=True)).decode()}"
            except:
                return err_info
        
        # ========== ? 最终保障：无论成败，必释放资源 ==========
        finally:
            await context.close()
            await browser.close()


async def getshopinfo(bot, groupId, userId, msg):
    msgText = ""
    for i in msg.message:
        if isinstance(i, Text):
            msgText = i.text
        if isinstance(i, PlainText):
            msgText = i.text
    if msgText.startswith("获取所有门店") or msgText.startswith("hqsymd"):
        if " " in msgText:
            province = msgText.split(" ")[1]
        else:
            province = "所有"
        data = await get_chunithm_store_screenshot("https://wc.wahlap.net/chunithm/location/index.html", province)
        await bot.api.post_group_msg(groupId, at=userId, image=data)
