import pygetwindow as gw
import pyautogui

windowTitle = ""

def getScreenshot():
    # 获取当前最前面的窗口
    active_window = gw.getActiveWindow()

    if active_window:
        # 获取窗口的左上角和右下角坐标
        left = active_window.left
        top = active_window.top
        width = active_window.width
        height = active_window.height

        # 截图
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save("outPut\screenshot\screenshot.png")
        print("截图已保存为 screenshot.png")
        global windowTitle
        windowTitle = active_window.title
    else:
        print("未找到当前活跃窗口")