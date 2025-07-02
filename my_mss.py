import mss
import os
import numpy as np

class ScreenCapture:
    """封装mss库的屏幕截图功能"""
    
    def __init__(self):
        """初始化屏幕截图对象"""
        self.sct = None
    
    def __enter__(self):
        """上下文管理器入口"""
        self.sct = mss.mss()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.sct:
            self.sct.close()
    
    def take_full_screenshot(self, output_path="screen.png"):
        """
        截取全屏并保存为PNG格式
        
        Args:
            output_path (str): 输出文件路径，默认为"screen.png"
            
        Returns:
            screenshot: mss截图对象，失败时返回None
        """
        try:
            if not self.sct:
                self.sct = mss.mss()
            
            # 获取所有显示器信息，monitor 0 是所有显示器的组合
            monitor = self.sct.monitors[0]
            
            # 截取屏幕
            screenshot = self.sct.grab(monitor)
            
            # 直接保存为PNG格式
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
            
            print(f"截图已成功保存到: {os.path.abspath(output_path)}")
            print(f"截图尺寸: {screenshot.size[0]} x {screenshot.size[1]}")
            
            return screenshot
            
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def take_region_screenshot(self, x, y, width, height, output_path="region.png"):
        """
        截取指定区域并保存
        
        Args:
            x (int): 起始x坐标
            y (int): 起始y坐标
            width (int): 宽度
            height (int): 高度
            output_path (str): 输出文件路径
            
        Returns:
            screenshot: mss截图对象，失败时返回None
        """
        try:
            if not self.sct:
                self.sct = mss.mss()
            
            # 定义截取区域
            monitor = {
                "top": y,
                "left": x,
                "width": width,
                "height": height
            }
            
            # 截取指定区域
            screenshot = self.sct.grab(monitor)
            
            # 保存为PNG格式
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
            
            print(f"区域截图已保存到: {os.path.abspath(output_path)}")
            print(f"截图区域: ({x}, {y}) - {width} x {height}")
            
            return screenshot
            
        except Exception as e:
            print(f"区域截图失败: {e}")
            return None
    
    def screenshot_to_array(self, screenshot):
        """
        将mss截图对象转换为numpy数组
        
        Args:
            screenshot: mss截图对象
            
        Returns:
            numpy.ndarray: 图像数组，格式为BGRA
        """
        try:
            return np.array(screenshot)
        except Exception as e:
            print(f"截图转换数组失败: {e}")
            return None
    
    def get_monitor_info(self):
        """
        获取所有显示器信息
        
        Returns:
            list: 显示器信息列表
        """
        try:
            if not self.sct:
                self.sct = mss.mss()
            return self.sct.monitors
        except Exception as e:
            print(f"获取显示器信息失败: {e}")
            return []

def take_screenshot(output_path="screen.png"):
    """
    快速截取全屏的便捷函数
    
    Args:
        output_path (str): 输出文件路径
        
    Returns:
        screenshot: mss截图对象
    """
    with ScreenCapture() as capture:
        return capture.take_full_screenshot(output_path) 