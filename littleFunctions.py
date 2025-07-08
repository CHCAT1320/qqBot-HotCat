import json

class funcs:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id
        self.file_path = f"group/{group_id}.json"
        self.groupInfo = self.readGroupJsonFile()

    def readGroupJsonFile(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                groupInfo = json.load(f)
                if "littleFunctions" not in groupInfo:
                    groupInfo["littleFunctions"] = {}
                    groupInfo["littleFunctions"]["numberAddOne"] = True
                    groupInfo["littleFunctions"]["bracketPair"] = True
                    groupInfo["littleFunctions"]["why"] = True
        except:
            groupInfo = {}
            self.writeGroupJsonFile(groupInfo)
        return groupInfo

    def writeGroupJsonFile(self, groupInfo:dict):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(groupInfo, f, ensure_ascii=False, indent=4)

    def openOrCloseFuncs(self, func_name:str):
        try:
            if func_name[2:] not in self.groupInfo["littleFunctions"]:
                return
            if func_name.startswith("开启"):
                self.groupInfo["littleFunctions"][func_name[2:]] = True
                self.writeGroupJsonFile(self.groupInfo)
                return f"开启{func_name[2:]}成功"
            elif func_name.startswith("关闭"):
                self.groupInfo["littleFunctions"][func_name[2:]] = False
                self.writeGroupJsonFile(self.groupInfo)
                return f"关闭{func_name[2:]}成功"
        except:
            return "未找到功能"


    # def is_number(self, s):
    #     pattern = r'^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)([eE][+-]?[0-9]+)?$'
    #     if re.match(pattern, s) is not None:
    #         self.numberAddOne(s)

    def numberAddOne(self, number:str):
        if not self.groupInfo["littleFunctions"]["numberAddOne"]:
            return
        try:
            if float(number).is_integer():
                return str(int(number) + 1)
            return str(float(number) + 1)
        except:
            # return "请输入数字"
            pass

    
    def bracketPair(self, text:str):
        try:
            if not self.groupInfo["littleFunctions"]["bracketPair"]:
                return
            leftBrackets = ['(', '[', '{', '<', '〔', '【', '《', '〖', '「', '（', '｛', '〘', '〚', '『', '〟', '〈']
            rightBrackets = [')', ']', '}', '>', '〕', '】', '》', '〗', '」', '）', '｝', '〙', '〛', '』', '〞', '〉']

            for i in leftBrackets:
                if i in text and rightBrackets[leftBrackets.index(i)] not in text:
                    return rightBrackets[leftBrackets.index(i)]
        except:
            pass
    
    async def why(self, bot, text:str):
        if not self.groupInfo["littleFunctions"]["why"]:
            return
        if "为什么" in text:
            await bot.api.post_group_msg(self.group_id, text="因为")
            await bot.api.post_group_msg(self.group_id, image="img/nimeixiazaixiguashipin.jpg")