# from ncatbot.core.helper.forward_constructor import ForwardConstructor
# from ncatbot.core.event.message_segment import Text, At, Node, Forward, PlainText
# from ncatbot.core.event.message_segment import MessageArray

# async def send_fake_msg(bot, group_id, user_id, msg):
#     text = ""
#     at_list = []
#     for i in msg.message:
#         if isinstance(i, Text):
#             if i.text == '' or i.text == ' ':
#                 continue
#             text = i.text
#         if isinstance(i, PlainText):
#             if i.text == '' or i.text == ' ':
#                 continue
#             text = i.text
#         if isinstance(i, At):
#             at_list.append(i.qq)
#     if text.startswith("构造合并转发"):
#         node1 = Node(user_id="1095216448", nickname="超级大冰猫", content=MessageArray(Text("你好")))
#         # node2 = Node(user_id=at_list[1], nickname="B", content=MessageArray(Text("你好")))
#         forward = Forward(content=[node1])
#         await bot.api.post_group_forward_msg(group_id, forward)

from ncatbot.core.helper.forward_constructor import ForwardConstructor
from ncatbot.core.event.message_segment import Text, At, Node, Forward, PlainText
from ncatbot.core.event.message_segment import MessageArray

async def send_fake_msg(bot, group_id, user_id, msg):
        # return  
    # cmdText = ""
    # # at_list = []
    # for i in msg.message:
    #     if isinstance(i, Text):
    #         if i.text == '' or i.text == ' ':
    #             continue
    #         cmdText = i.text
    #     if isinstance(i, PlainText):
    #         if i.text == '' or i.text == ' ':
    #             continue
    #         cmdText = i.text
    #     # if isinstance(i, At):
    #     #     at_list.append(i.qq)
    # if cmdText.startswith("构造合并转发"):
        fcr = ForwardConstructor(user_id="1095216448", nickname="超级大冰猫")
        fcr.attach_text("第一条文本")

        forward = fcr.to_forward()  # type: Forward
        await bot.api.post_group_forward_msg(group_id, forward)