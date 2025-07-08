import json
import time
import unicodedata

class jiting:
    def __init__(self, group_id, user_id, sender_name):
        self.group_id = group_id
        self.user_id = user_id
        self.sender_name = sender_name
        self.file_path = f"group/{group_id}.json"
        self.groupInfo = self.readGroupJsonFile()

    def readGroupJsonFile(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                groupInfo = json.load(f)
                if "jitingList" not in groupInfo:
                    groupInfo["jitingList"] = []
                return groupInfo
        except:
            groupInfo = {}
            self.writeGroupJsonFile(groupInfo)
        return groupInfo

    def writeGroupJsonFile(self, groupInfo:dict):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(groupInfo, f, ensure_ascii=False, indent=4)

    def addJiting(self, text:str):
        try:
            if text.startswith("添加机厅") or text.startswith("tjjt"):
                name = text.split(" ")[1]
                if len(self.groupInfo["jitingList"]) >= 10:
                    return "机厅数量不能超过10个"
                if not name:
                    return "机厅名称不能为空"
                if len(name) > 20:
                    return "机厅名称长度不能超过20个字符"
                if "\n" in name:
                    return "机厅名称不能包含换行符"
                if " " in name:
                    return "机厅名称不能包含空格"
                for char in name:
                    if unicodedata.category(char).startswith('C'):
                        return "机厅名称不能包含控制字符"
                if name in [jiting["name"] for jiting in self.groupInfo["jitingList"]]:
                    return f"机厅 {name} 已存在"
                self.groupInfo["jitingList"].append({
                    "name": name,
                    "name1": "",
                    "members": 0,
                    "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "reporter": self.sender_name
                })
                self.writeGroupJsonFile(self.groupInfo)
                return f"添加机厅 {name} 成功"
        except:
            return
        
    def getJitingList(self, text:str):
        try:
            if text.startswith("机厅列表") or text.startswith("jtlb"):
                jitingList = self.groupInfo["jitingList"]
                if not jitingList:
                    return "当前群聊没有机厅"
                result = "机厅列表："
                for jiting in jitingList:
                    if jiting["name1"] != "":
                        result += f"\n{jiting['name']}({jiting['name1']})（{jiting['members']}人）\n更新时间：{jiting['update_time']} 报告人：{jiting['reporter']}"
                    else:
                        result += f"\n{jiting['name']}（{jiting['members']}人）\n更新时间：{jiting['update_time']} 报告人：{jiting['reporter']}"
                return result
        except:
            return "当前群聊没有机厅"
        
    def setJiTingName1(self, text:str):
        try:
            if text.startswith("机厅别名") or text.startswith("jtbm"):
                name = text.split(" ")[1]
                name1 = text.split(" ")[2]
                if not name:
                    return "机厅名称不能为空"
                if not name1:
                    return "机厅别名不能为空"
                if len(name1) > 20:
                    return "机厅别名长度不能超过20个字符"
                if "\n" in name1:
                    return "机厅别名不能包含换行符"
                if " " in name1:
                    return "机厅别名不能包含空格"
                for char in name1:
                    if unicodedata.category(char).startswith('C'):
                        return "机厅别名不能包含控制字符"
                for jiting in self.groupInfo["jitingList"]:
                    if jiting["name"] == name:
                        jiting["name1"] = name1
                        self.writeGroupJsonFile(self.groupInfo)
                        return f"机厅 {name} 的别名已设置为 {name1}"
                return f"机厅 {name} 不存在"
        except:
                return

    def updateJitingMembers(self, text: str):
        try:
            for jiting_info in self.groupInfo["jitingList"]:
                if text.startswith(jiting_info["name"]) or text.startswith(jiting_info["name1"]):
                    operation = text[len(jiting_info["name"]):]
                    if operation.isdigit():
                        jiting_info["members"] = int(operation)
                    elif operation.startswith("+") and operation[1:].isdigit():
                        jiting_info["members"] += int(operation[1:])
                    elif operation.startswith("-") and operation[1:].isdigit():
                        jiting_info["members"] = max(0, jiting_info["members"] - int(operation[1:]))
                    else:
                        return
                    
                    if jiting_info["members"] > 100:
                        jiting_info["members"] = 0
                        return f"机厅 {jiting_info['name']}({jiting_info['name1']}) 爆炸了，无人幸免, 人数已归零"

                    self.writeGroupJsonFile(self.groupInfo)
                    return f"机厅 {jiting_info['name']}({jiting_info['name1']}) 人数更新为 {jiting_info['members']}"

            return

        except:
            return
        
    def lookUpJiting(self, text:str):
        try:
            for jiting_info in self.groupInfo["jitingList"]:
                if text.endswith("几") or text.endswith("j"):
                    if text.startswith(jiting_info["name"]) or text.startswith(jiting_info["name1"]):
                        return f"机厅 {jiting_info['name']}({jiting_info['name1']}) 人数为 {jiting_info['members']}\n更新时间：{jiting_info['update_time']} \n报告人：{jiting_info['reporter']}"
                    else:
                        return
            return
        except:
            return