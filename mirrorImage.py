import requests
from PIL import Image, ImageSequence
from io import BytesIO
import base64

def mirrorImage(imageUrl, mirrorSide="left"):
    """
    图片中间镜像处理，支持8个方向和多种图片格式（JPG、JPEG、PNG、GIF）
    
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
        img_bytes = BytesIO(response.content)
        img = Image.open(img_bytes)
    except Exception as e:
        raise ValueError(f"读取图片失败：{str(e)}")
    
    # 2. 判断图片格式
    img_format = img.format.lower() if img.format else 'png'
    supported_formats = ['jpg', 'jpeg', 'png', 'gif']
    if img_format not in supported_formats:
        raise ValueError(f"不支持的图片格式：{img_format}，支持格式：{supported_formats}")
    
    # 3. 获取图片尺寸和中心点
    width, height = img.size
    midX = width // 2    # 水平中点
    midY = height // 2   # 垂直中点
    
    # 4. 定义各区域的裁剪范围（按象限划分）
    regions = {
        "left": (0, 0, midX, height),          # 左半区（垂直分割）
        "right": (midX, 0, width, height),     # 右半区（垂直分割）
        "top": (0, 0, width, midY),            # 上半区（水平分割）
        "down": (0, midY, width, height),      # 下半区（水平分割）
        "topLeft": (0, 0, midX, midY),         # 左上象限
        "topRight": (midX, 0, width, midY),    # 右上象限
        "downLeft": (0, midY, midX, height),   # 左下象限
        "downRight": (midX, midY, width, height)# 右下象限
    }
    
    # 验证镜像方向是否合法
    if mirrorSide not in regions:
        validSides = ", ".join(regions.keys())
        raise ValueError(f"无效的镜像方向！支持的方向：{validSides}")
    
    # 5. 处理单帧/多帧（GIF）
    is_gif = img_format == 'gif'
    frames = []
    
    for frame in ImageSequence.Iterator(img):
        # 处理透明通道（保留PNG/GIF的Alpha通道）
        frame = frame.convert("RGBA") if img_format in ['png', 'gif'] else frame.convert("RGB")
        
        new_frame = Image.new(frame.mode, (width, height))
        targetRegion = regions[mirrorSide]
        originalPart = frame.crop(targetRegion)  # 保留的原始区域
        
        if mirrorSide in ["left", "right"]:
            # 水平方向镜像（左右分割）
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT)
            if mirrorSide == "left":
                new_frame.paste(originalPart, (0, 0))
                new_frame.paste(mirroredPart, (midX, 0))
            else:
                new_frame.paste(mirroredPart, (0, 0))
                new_frame.paste(originalPart, (midX, 0))
        
        elif mirrorSide in ["top", "down"]:
            # 垂直方向镜像（上下分割）
            mirroredPart = originalPart.transpose(Image.FLIP_TOP_BOTTOM)
            if mirrorSide == "top":
                new_frame.paste(originalPart, (0, 0))
                new_frame.paste(mirroredPart, (0, midY))
            else:
                new_frame.paste(mirroredPart, (0, 0))
                new_frame.paste(originalPart, (0, midY))
        
        elif mirrorSide in ["topLeft", "topRight", "downLeft", "downRight"]:
            # 象限镜像（同时进行水平+垂直翻转）
            mirroredPart = originalPart.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            if mirrorSide == "topLeft":
                new_frame.paste(originalPart, (0, 0))
                new_frame.paste(mirroredPart, (midX, midY))
                new_frame.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (midX, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (0, midY))
            elif mirrorSide == "topRight":
                new_frame.paste(originalPart, (midX, 0))
                new_frame.paste(mirroredPart, (0, midY))
                new_frame.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (midX, midY))
            elif mirrorSide == "downLeft":
                new_frame.paste(originalPart, (0, midY))
                new_frame.paste(mirroredPart, (midX, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (0, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (midX, midY))
            elif mirrorSide == "downRight":
                new_frame.paste(originalPart, (midX, midY))
                new_frame.paste(mirroredPart, (0, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_TOP_BOTTOM), (midX, 0))
                new_frame.paste(originalPart.transpose(Image.FLIP_LEFT_RIGHT), (0, midY))
        
        # 转换回适合保存的模式
        if img_format in ['jpg', 'jpeg']:
            new_frame = new_frame.convert("RGB")  # JPG不支持透明通道
        frames.append(new_frame)
    
    # 6. 保存处理后的图片
    buffer = BytesIO()
    if is_gif:
        # 保存GIF并保留动画参数
        frames[0].save(
            buffer,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            duration=img.info.get('duration', 100),
            loop=img.info.get('loop', 0),
            disposal=2
        )
    else:
        # 保存静态图片
        save_format = 'JPEG' if img_format in ['jpg', 'jpeg'] else img_format.upper()
        frames[0].save(
            buffer,
            format=save_format,
            quality=95,
            optimize=True
        )
    
    # 7. 生成DataURL
    buffer.seek(0)
    base64Str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    mime_type = f"image/{img_format}"
    dataUrl = f"data:{mime_type};base64,{base64Str}"
    
    return dataUrl

async def send_mirrored_image(bot, group_id, user_id, msg, Reply, Image, Text):
    d = "right"
    msgText = msg.raw_message
    # for i in msg.message:
        # if isinstance(i, Text):
            # msgText = i.text
    if msgText.startswith("镜像"):
        await bot.api.post_group_msg(group_id, text="测试")
        text = msgText[2:]
        direction_map = {
            "左": "left",
            "右": "right",
            "上": "top",
            "下": "down",
            "左上": "topLeft",
            "右上": "topRight",
            "左下": "downLeft",
            "右下": "downRight"
        }
        d = direction_map.get(text, "right")  # 使用字典更简洁
    else:
        return
    
    for i in msg.message:
        if isinstance(i, Reply):
            try:
                imgMsg = await bot.api.get_msg(i.id)
                for j in imgMsg.message:
                    if isinstance(j, Image):
                        await bot.api.post_group_msg(group_id, text=f"正在镜像{d}侧图片")
                        img_url = j.url
                        mirrored_img = mirrorImage(img_url, mirrorSide=d)
                        
                        await bot.api.post_group_msg(group_id, image=mirrored_img, at=user_id)
            except Exception as e:
                await bot.api.post_group_msg(group_id, text=f"处理失败：{str(e)}")