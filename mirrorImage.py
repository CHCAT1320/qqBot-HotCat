import requests
from PIL import Image
from io import BytesIO
import base64

def mirrorImage(imageUrl, mirrorSide="left"):
    """
    图片中间镜像处理，支持8个方向：left/right/top/down/topLeft/topRight/downLeft/downRight
    
    参数:
        imageUrl: 网络图片URL
        mirrorSide: 镜像方向（默认left）
            - left: 保留左侧，右侧用左侧镜像
            - right: 保留右侧，左侧用右侧镜像
            - top: 保留上侧，下侧用上侧镜像
            - down: 保留下侧，上侧用下侧镜像
            - topLeft: 保留左上，右下用左上镜像
            - topRight: 保留右上，左下用右上镜像
            - downLeft: 保留左下，右上用左下镜像
            - downRight: 保留右下，左上用右下镜像
    
    返回:
        镜像后的图片DataURL（Base64编码）
    """
    # 1. 读取网络图片（添加异常处理）
    try:
        response = requests.get(imageUrl, timeout=10)
        response.raise_for_status()  # 抛出 HTTP 错误
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        raise ValueError(f"读取图片失败：{str(e)}")
    
    # 2. 获取图片尺寸和中心点
    width, height = img.size
    midX = width // 2    # 水平中点
    midY = height // 2   # 垂直中点
    
    # 3. 定义各区域的裁剪范围（按象限划分）
    regions = {
        "left": (0, 0, midX, height),          # 左半区（垂直分割）
        "right": (midX, 0, width, height),     # 右半区（垂直分割）
        "top": (0, 0, width, midY),            # 上半区（水平分割）
        "down": (0, midY, width, height),      # 下半区（水平分割，原bottom改为down）
        "topLeft": (0, 0, midX, midY),         # 左上象限（小驼峰）
        "topRight": (midX, 0, width, midY),    # 右上象限（小驼峰）
        "downLeft": (0, midY, midX, height),   # 左下象限（小驼峰，原bottomLeft改为downLeft）
        "downRight": (midX, midY, width, height)# 右下象限（小驼峰，原bottomRight改为downRight）
    }
    
    # 验证镜像方向是否合法
    if mirrorSide not in regions:
        validSides = ", ".join(regions.keys())
        raise ValueError(f"无效的镜像方向！支持的方向：{validSides}")
    
    # 4. 根据镜像方向执行对应的镜像逻辑
    newImg = Image.new("RGB", (width, height))
    targetRegion = regions[mirrorSide]
    originalPart = img.crop(targetRegion)  # 保留的原始区域
    
    if mirrorSide in ["left", "right"]:
        # 水平方向镜像（左右分割）
        if mirrorSide == "left":
            # 保留左侧，右侧用左侧水平翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT)
            newImg.paste(originalPart, (0, 0))          # 左侧粘贴原图
            newImg.paste(mirroredPart, (midX, 0))      # 右侧粘贴镜像图
        else:
            # 保留右侧，左侧用右侧水平翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT)
            newImg.paste(mirroredPart, (0, 0))          # 左侧粘贴镜像图
            newImg.paste(originalPart, (midX, 0))      # 右侧粘贴原图
    
    elif mirrorSide in ["top", "down"]:
        # 垂直方向镜像（上下分割）
        if mirrorSide == "top":
            # 保留上侧，下侧用上侧垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(originalPart, (0, 0))          # 上侧粘贴原图
            newImg.paste(mirroredPart, (0, midY))      # 下侧粘贴镜像图
        else:
            # 保留下侧，上侧用下侧垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(mirroredPart, (0, 0))          # 上侧粘贴镜像图
            newImg.paste(originalPart, (0, midY))      # 下侧粘贴原图
    
    elif mirrorSide in ["topLeft", "topRight", "downLeft", "downRight"]:
        # 象限镜像（同时进行水平+垂直翻转）
        if mirrorSide == "topLeft":
            # 保留左上，右下用左上水平+垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(originalPart, (0, 0))              # 左上粘贴原图
            newImg.paste(mirroredPart, (midX, midY))      # 右下粘贴镜像图
            # 补全右上和左下（用镜像后的对应区域）
            newImg.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (midX, 0))  # 右上
            newImg.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (0, midY))  # 左下
        
        elif mirrorSide == "topRight":
            # 保留右上，左下用右上水平+垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(originalPart, (midX, 0))          # 右上粘贴原图
            newImg.paste(mirroredPart, (0, midY))          # 左下粘贴镜像图
            # 补全左上和右下
            newImg.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))      # 左上
            newImg.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (midX, midY))# 右下
        
        elif mirrorSide == "downLeft":
            # 保留左下，右上用左下水平+垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(originalPart, (0, midY))          # 左下粘贴原图
            newImg.paste(mirroredPart, (midX, 0))          # 右上粘贴镜像图
            # 补全左上和右下
            newImg.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (0, 0))      # 左上
            newImg.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (midX, midY))# 右下
        
        elif mirrorSide == "downRight":
            # 保留右下，左上用右下水平+垂直翻转
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            newImg.paste(originalPart, (midX, midY))      # 右下粘贴原图
            newImg.paste(mirroredPart, (0, 0))              # 左上粘贴镜像图
            # 补全右上和左下
            newImg.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (midX, 0))  # 右上
            newImg.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (0, midY))  # 左下
    
    # 5. 将镜像图片转换为 DataURL（Base64 编码）
    buffer = BytesIO()
    newImg.save(buffer, format="PNG", quality=95)
    buffer.seek(0)  # 重置文件指针到开头
    
    # 编码为 Base64 字符串并拼接 DataURL
    base64Str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    dataUrl = f"data:image/jpeg;base64,{base64Str}"
    
    return dataUrl

# # 调用示例（替换成你的图片链接，指定left/right）
# img_url = "https://example.com/your-image.jpg"
# mirrored_img = mirror_image(img_url, mirror_side="right")
# mirrored_img.save("mirrored_image.jpg")  # 保存镜像后的图
async def send_mirrored_image(bot, group_id, user_id, msg, Reply, Image, Text):
    d = "right"
    msgText = msg.raw_message
    for i in msg.message:
        if isinstance(i, Text):
            msgText = i.text
    if msgText.startswith("镜像"):
        text = msgText[2:]
        if text == "左":
            d = "left"
        if text == "右":
            d = "right"
        if text == "上":
            d = "top"
        if text == "下":
            d = "down"
        if text == "左上":
            d = "topLeft"
        if text == "右上":
            d = "topRight"
        if text == "左下":
            d = "downLeft"
        if text == "右下":
            d = "downRight"
    else:
        return
    for i in msg.message:
        if isinstance(i, Reply):
            # await bot.api.post_group_msg(group_id, text=i.id)
            imgMsg = await bot.api.get_msg(i.id)
            for j in imgMsg.message:
                if isinstance(j, Image):
                    img_url = j.url
                    mirrored_img = mirrorImage(img_url, mirrorSide=d)
                    await bot.api.post_group_msg(group_id, text=f"正在镜像{d}侧图片")
                    await bot.api.post_group_msg(group_id, image=mirrored_img, at=user_id)