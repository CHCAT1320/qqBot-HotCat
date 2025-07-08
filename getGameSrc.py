import requests
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class getWaterFishingSrc:
    def __init__(self):
        pass
    
    async def get_src(self, bot, group_id, user_id, text:str):
        if text.startswith("查询游戏记录"):
            data = text.split(" ")
            username = data[1]
            gameType = data[2]
            b = data[3]
            if b == "b50":
                b = True
            else:
                b = False
            
            await self.get_player_summary(username, gameType, b)
            await bot.api.post_group_msg(group_id, at=user_id)
            await bot.api.post_group_file(group_id, file="game_records.xlsx")
            import os
            file_path = "game_records.xlsx"
            os.unlink(file_path)
        else:
            return
        return


    async def get_player_summary(self, username, gameType, b50=False):
        """
        获取用户的简略成绩信息（b40 或 b50）。
        
        :param username: 用户名
        :param gameType: 游戏类型，如舞萌、中二节奏等
        :param b50: 是否获取b50数据，默认为False（即b40）
        :return: 用户的简略成绩信息
        """

        if gameType == "舞萌" or gameType == "maimai" or gameType == "maimaidx":
            url = "https://www.diving-fish.com/api/maimaidxprober/query/player"
        elif gameType == "中二节奏" or gameType == "中二" or gameType == "chunithm":
            url = "https://www.diving-fish.com/api/chunithmprober/query/player"
        else:
            return
        data = {
            "username": username,
        }
        
        if b50:
            data["b50"] = "1"  # 添加b50参数以获取b50数据
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # 检查请求是否成功
            print(f"请求成功: {response.json()}")
            json_to_table(response.json())
            return   # 返回JSON数据
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None


import pandas as pd
import json

def json_to_table(json_data):
    # 提取玩家信息
    username = json_data.get('username', '')
    nickname = json_data.get('nickname', '')
    rating = json_data.get('rating', '')

    # 处理b30和r10记录
    b30_records = json_data.get('records', {}).get('b30', [])
    r10_records = json_data.get('records', {}).get('r10', [])

    # 将b30和r10记录合并到一个列表中
    all_records = b30_records + r10_records

    # 创建一个空列表来存储处理后的记录
    processed_records = []

    # 遍历所有记录并提取需要的信息
    for record in all_records:
        processed_record = {
            'title': record.get('title', ''),
            'ds': record.get('ds', ''),
            'ra': record.get('ra', ''),
            'level': record.get('level', ''),
            'score': record.get('score', ''),
            'username': username,
            'nickname': nickname,
            'rating': rating
        }
        processed_records.append(processed_record)

    # 创建一个DataFrame
    df = pd.DataFrame(processed_records)

    # 将DataFrame保存为Excel文件
    df.to_excel('game_records.xlsx', index=False)
    print("表格已保存为 game_records.xlsx")


# import pandas as pd
# from openpyxl import load_workbook
# from openpyxl.styles import Font, PatternFill, Alignment

# def json_to_styled_excel(json_data, excel_filename='styled_records.xlsx'):
#     """
#     将 JSON 数据转换为带样式的 Excel 文件
    
#     Args:
#         json_data (dict): 包含玩家记录的 JSON 数据
#         excel_filename (str, optional): 输出的 Excel 文件名，默认为 'styled_records.xlsx'
#     """
#     try:
#         # 检查基本信息
#         nickname = json_data.get('nickname', '')
#         rating = json_data.get('rating', '')
#         username = json_data.get('username', '')
        
#         # 检查记录数据
#         b30_records = json_data.get('records', {}).get('b30', [])
#         r10_records = json_data.get('records', {}).get('r10', [])
        
#         # 将 JSON 数据转换为 DataFrame
#         b30_df = pd.DataFrame(b30_records)
#         r10_df = pd.DataFrame(r10_records)
        
#         # 创建基本信息 DataFrame
#         info_df = pd.DataFrame({
#             '昵称': [nickname],
#             'rating': [rating],
#             '用户名': [username]
#         })
        
#         # 打印调试信息
#         print("基本信息 DataFrame:")
#         print(info_df)
#         print("\nB30 记录:")
#         print(b30_df.head())
#         print("\nR10 记录:")
#         print(r10_df.head())
        
#         # 创建 Excel 写入器
#         with pd.ExcelWriter(excel_filename) as writer:
#             # 写入基本信息
#             info_df.to_excel(writer, sheet_name='基本信息', index=False)
            
#             # 写入 B30 记录（如果存在数据）
#             if not b30_df.empty:
#                 b30_df.to_excel(writer, sheet_name='B30 记录', index=False)
#             else:
#                 print("警告：B30 记录为空，未写入 B30 记录工作表")
            
#             # 写入 R10 记录（如果存在数据）
#             if not r10_df.empty:
#                 r10_df.to_excel(writer, sheet_name='R10 记录', index=False)
#             else:
#                 print("警告：R10 记录为空，未写入 R10 记录工作表")
        
#         # 加载工作簿并添加样式
#         wb = load_workbook(excel_filename)
        
#         # 为所有工作表添加样式
#         for sheet_name in wb.sheetnames:
#             ws = wb[sheet_name]
            
#             # 设置列宽
#             for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
#                 ws.column_dimensions[col].width = 15
            
#             # 设置标题样式
#             for cell in ws[1]:
#                 cell.font = Font(bold=True, color="000000", size=12)
#                 cell.alignment = Alignment(horizontal="center", vertical="center")
#                 cell.fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
        
#         # 保存工作簿
#         wb.save(excel_filename)
        
#         print(f"已成功将 JSON 数据转换为带样式 Excel 文件: {excel_filename}")
#         return info_df, b30_df, r10_df
    
#     except Exception as e:
#         print(f"发生错误: {e}")
#         return None, None, None

# # # 示例 JSON 数据
# # json_data = {
# #     'nickname': 'BingCat',
# #     'rating': 14.316249999999997,
# #     'records': {
# #         'b30': [],
# #         'r10': []
# #     },
# #     'username': 'chcat1320'
# # }

# # # 调用函数
# # info_df, b30_df, r10_df = json_to_styled_excel(json_data)

# # 使用示例
# # json_data = {...}  # 这里替换成您的 JSON 数据
# # json_to_styled_excel(json_data)