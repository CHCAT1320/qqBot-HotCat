from ncatbot.core.helper.forward_constructor import ForwardConstructor
from ncatbot.core.event.message_segment import Text, At, Node, Forward, PlainText
from ncatbot.core.event.message_segment import MessageArray
import random

# 对话数据集（保持不变）
dialogue_data = [
    {
        "title": "病房前的对话",
        "roleCount": 3,
        "dialogues": [
            {"role": 1, "text": "都说了多少遍，我不是神经病！快放我出去！"},
            {"role": 1, "text": "老兄，你相信我的话吗？我没有得神经病，他们抓错人了。"},
            {"role": 2, "text": "哈哈哈，你说你没得神经病，那你为什么在神经病院里？一个神经病说自己不是神经病？哈哈哈……"},
            {"role": 1, "text": "说了这么半天，你不也是神经病吗。哪有一个正常人会和一个神经病说话还冲着他傻笑？"},
            {"role": 2, "text": "你听到了吗？他刚刚承认他是神经病了。哈哈哈，他刚才还说他不是神经病呢。哈哈哈，我们都是神经病，神经病万岁！"},
            {"role": 3, "text": "神经病。"}
        ]
    },
    {
        "title": "马路牙子谈判专家",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "我知道你守着金库，借我二百块，月底还你两袋猫粮！"},
            {"role": 1, "text": "不行！你上次借我的“过桥费”，拿泡泡糖抵账，我牙粘住三天没张开！"},
            {"role": 1, "text": "这次真的！我拿烤红薯抵押！给我个红薯，记它账上！"},
            {"role": 2, "text": "它上个月欠我仨红薯了，还拿你那破领带抵过账！"}
        ]
    },
    {
        "title": "冰箱里的秘密会议",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "说！是不是你把我妈藏的红烧肉偷啃了？"},
            {"role": 1, "text": "冤枉！我冰碴子都没化，怎么啃肉？你问它！它昨天晚上咕噜咕噜笑出声！"},
            {"role": 1, "text": "老实交代！"},
            {"role": 1, "text": "我那是发酵！发酵懂吗？是红烧肉自己跳冰箱里来的，它说外面太热，想跟我贴贴！"},
            {"role": 2, "text": "喵！"}
        ]
    },
    {
        "title": "路灯交友记",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "你说你天天亮着，累不累啊？"},
            {"role": 1, "text": "累！但我不敢灭，我一灭，那家伙就找不到回家的路了！"},
            {"role": 2, "text": "喵！"},
            {"role": 1, "text": "你看！它还挺给你面子！那你俩拜把子吧！我当见证人！"},
            {"role": 1, "text": "好！以后它负责抓老鼠，我负责照亮老鼠洞！"}
        ]
    },
    {
        "title": "公交站牌算命师",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "我看你印堂发黑，今日必有一劫！"},
            {"role": 1, "text": "别装沉默！你是不是知道下趟公交不来了？"},
            {"role": 2, "text": "师傅，这是块铁牌子，它不会说话的。"},
            {"role": 1, "text": "它不说话就是默认！你看，它上面的字都歪了，是在给我递暗号！"}
        ]
    },
    {
        "title": "垃圾桶的晚餐邀约",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "喂，今天的晚餐够丰盛啊，有半块面包和一根香肠。"},
            {"role": 1, "text": "我就知道你够意思，特意给我留的吧？"},
            {"role": 2, "text": "那是我刚扔的，麻烦你离远点行不行？"},
            {"role": 1, "text": "你看你，客气什么！我们都做了三年邻居了，分什么你我！"}
        ]
    },
    {
        "title": "枕头的悄悄话",
        "roleCount": 2,
        "dialogues": [
            {"role": 1, "text": "你昨晚又偷偷哭了，我都听见了，你的眼泪把我弄湿了一大片。"},
            {"role": 1, "text": "别不承认！你还说梦话，说你不想当这个，想当那个能飞的。"},
            {"role": 2, "text": "大半夜的，你对着这个自言自语，不觉得吓人吗？"},
            {"role": 1, "text": "它都跟我说话了！它说它想飞，我明天就带它去楼顶放飞！"}
        ]
    },
    {
        "title": "公园石凳茶话会",
        "roleCount": 3,
        "dialogues": [
            {"role": 1, "text": "今日阳光正好，咱俩喝一杯？我带了树叶泡的茶。"},
            {"role": 2, "text": "你怎么不问我？我辈分比它大！"},
            {"role": 1, "text": "你别闹，你腿太多，坐不稳当，喝茶容易洒。"},
            {"role": 3, "text": "你们嘀咕啥呢？我也要喝！不给我我今晚就不亮！"},
            {"role": 1, "text": "好好好，分你一口，别咬我，你太烫。"}
        ]
    },
    {
        "title": "楼道声控灯聊天记",
        "roleCount": 3,
        "dialogues": [
            {"role": 1, "text": "喂！你昨晚为啥老灭？我还没爬完楼梯呢！"},
            {"role": 2, "text": "怪我？是你脚步声太轻！我还以为没人了呢！"},
            {"role": 3, "text": "别吵了别吵了！我天天被人跺脚震得头疼！"},
            {"role": 1, "text": "就是！有人故意跺脚，吵死了！我都想罢工了！"},
            {"role": 2, "text": "罢工+1！今晚咱们都别亮，让他们摸黑！"}
        ]
    }
]

async def send_fake_msg(bot, group_id, user_id, msg, nickname):
    text = ""
    at_list = []
    # 解析消息中的文本和@对象（去重，避免重复@同一人导致人数误判）
    at_set = set()  # 用集合去重
    for i in msg.message:
        if isinstance(i, Text) and i.text.strip():
            text = i.text
        elif isinstance(i, PlainText) and i.text.strip():
            text = i.text
        elif isinstance(i, At):
            at_set.add(i.qq)
    at_list = list(at_set)  # 转列表，保证顺序
    at_count = len(at_list)

    # 触发条件：文本以“构造合并转发”开头，且有@对象
    if not text.startswith("生成小故事") or at_count == 0:
        return

    # ========== 核心修复：严格匹配对话角色数和@人数 ==========
    # 规则1：@1人 → 仅匹配2角色对话
    # 规则2：@2人 → 可匹配2/3角色对话（优先3角色）
    # 规则3：@3人 → 仅匹配3角色对话
    # 规则4：@>3人 → 取前3人，匹配3角色对话
    target_role_count = None
    if at_count == 1:
        target_role_count = 2  # 1人→强制2角色
    elif at_count == 2:
        # 2人→优先3角色，无则选2角色
        has_3role = any(d["roleCount"] == 3 for d in dialogue_data)
        target_role_count = 3 if has_3role else 2
    elif at_count >= 3:
        target_role_count = 3  # ≥3人→强制3角色，仅取前3个@的人
        at_list = at_list[:3]  # 截断，只保留前3人
    else:
        return  # 无@，直接返回

    # 筛选符合角色数的对话
    matched_dialogues = [d for d in dialogue_data if d["roleCount"] == target_role_count]
    if not matched_dialogues:
        # 兜底：若没有目标角色数的对话，降级到可用的
        matched_dialogues = dialogue_data
        if not matched_dialogues:
            return
    selected_dialogue = random.choice(matched_dialogues)
    dialogue_list = selected_dialogue["dialogues"]

    # 初始化转发节点列表
    forward_nodes = []

    # 精准角色→@用户映射（严格按顺序）
    # key=对话角色，value=@列表索引（1→0, 2→1, 3→2）
    role_at_map = {
        1: 0,  # 角色1 → 第1个@的人
        2: 1,  # 角色2 → 第2个@的人
        3: 2   # 角色3 → 第3个@的人
    }

    # 遍历所有对话条目，按顺序生成节点
    for dialogue_item in dialogue_list:
        role = dialogue_item["role"]
        dialogue_text = dialogue_item["text"]

        # 获取映射的@索引，若索引越界则兜底到最后一个@的人
        at_index = role_at_map.get(role, at_count - 1)
        at_index = min(at_index, len(at_list) - 1)  # 防越界
        target_user_id = at_list[at_index]

        # 获取用户昵称
        try:
            info = await bot.api.get_stranger_info(target_user_id)
            target_nickname = info.get("nickname", "未知用户")
        except Exception:
            target_nickname = "未知用户"  # 容错：获取昵称失败

        # 构建节点并追加
        node = Node(
            user_id=target_user_id,
            nickname=target_nickname,
            content=MessageArray(Text(dialogue_text))
        )
        forward_nodes.append(node)

    # 发送合并转发
    if forward_nodes:
        forward = Forward(content=forward_nodes)
        await bot.api.post_group_forward_msg(group_id, forward)