import mss
import os

def take_screenshot():
    """使用mss库截取全屏并保存为screen.png"""
    try:
        # 创建mss对象
        with mss.mss() as sct:
            # 获取所有显示器信息，monitor 0 是所有显示器的组合
            monitor = sct.monitors[0]  # 0 是所有显示器的组合
            
            # 截取屏幕
            screenshot = sct.grab(monitor)
            
            # 直接保存为PNG格式（mss默认支持）
            output_path = "screen.png"
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
            
            print(f"截图已成功保存到: {os.path.abspath(output_path)}")
            print(f"截图尺寸: {screenshot.size[0]} x {screenshot.size[1]}")
            
    except Exception as e:
        print(f"截图失败: {e}")

if __name__ == "__main__":
    print("开始全屏截图...")
    take_screenshot()
    print("截图完成！")
