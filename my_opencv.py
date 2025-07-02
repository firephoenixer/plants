import cv2
import numpy as np
import os

class ImageProcessor:
    """封装OpenCV库的图像处理功能"""
    
    def __init__(self):
        """初始化图像处理器"""
        pass
    
    def convert_color(self, image, conversion_code):
        """
        转换图像颜色空间
        
        Args:
            image: 输入图像
            conversion_code: 转换代码 (如cv2.COLOR_BGRA2BGR)
            
        Returns:
            转换后的图像，失败时返回None
        """
        try:
            return cv2.cvtColor(image, conversion_code)
        except Exception as e:
            print(f"颜色空间转换失败: {e}")
            return None
    
    def bgra_to_bgr(self, image):
        """
        将BGRA格式转换为BGR格式
        
        Args:
            image: BGRA格式的图像
            
        Returns:
            BGR格式的图像
        """
        return self.convert_color(image, cv2.COLOR_BGRA2BGR)
    
    def read_image(self, image_path, mode=cv2.IMREAD_COLOR):
        """
        读取图片文件
        
        Args:
            image_path (str): 图片文件路径
            mode: 读取模式，默认为彩色模式
            
        Returns:
            图像数组，失败时返回None
        """
        try:
            if not os.path.exists(image_path):
                print(f"错误：图片文件不存在: {image_path}")
                return None
                
            image = cv2.imread(image_path, mode)
            if image is None:
                print(f"错误：无法读取图片文件: {image_path}")
                return None
                
            return image
        except Exception as e:
            print(f"读取图片失败: {e}")
            return None
    
    def save_image(self, image, output_path):
        """
        保存图像到文件
        
        Args:
            image: 要保存的图像
            output_path (str): 输出文件路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            success = cv2.imwrite(output_path, image)
            if success:
                print(f"图像已保存到: {os.path.abspath(output_path)}")
                return True
            else:
                print(f"保存图像失败: {output_path}")
                return False
        except Exception as e:
            print(f"保存图像失败: {e}")
            return False
    
    def crop_image(self, image, x, y, width, height):
        """
        裁剪图像
        
        Args:
            image: 输入图像
            x (int): 起始x坐标
            y (int): 起始y坐标
            width (int): 裁剪宽度
            height (int): 裁剪高度
            
        Returns:
            裁剪后的图像
        """
        try:
            img_height, img_width = image.shape[:2]
            
            # 确保坐标不越界
            end_x = min(x + width, img_width)
            end_y = min(y + height, img_height)
            
            cropped = image[y:end_y, x:end_x]
            
            actual_width = end_x - x
            actual_height = end_y - y
            print(f"图像已裁剪: {actual_width} x {actual_height}")
            
            return cropped
        except Exception as e:
            print(f"裁剪图像失败: {e}")
            return None

class TemplateMatcher:
    """封装模板匹配功能"""
    
    def __init__(self, threshold=0.8):
        """
        初始化模板匹配器
        
        Args:
            threshold (float): 匹配阈值，默认0.8
        """
        self.threshold = threshold
    
    def match_template(self, screenshot, template_path, method=cv2.TM_CCOEFF_NORMED):
        """
        在截图中查找模板图片
        
        Args:
            screenshot: 截图图像数组
            template_path (str): 模板图片路径
            method: 匹配方法，默认为TM_CCOEFF_NORMED
            
        Returns:
            list: 匹配结果列表，包含坐标、尺寸和置信度信息
        """
        try:
            # 检查模板图片是否存在
            if not os.path.exists(template_path):
                print(f"错误：模板图片不存在: {template_path}")
                return None
            
            # 读取模板图片
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"错误：无法读取模板图片: {template_path}")
                return None
            
            # 获取模板图片的尺寸
            template_height, template_width = template.shape[:2]
            
            # 使用模板匹配
            result = cv2.matchTemplate(screenshot, template, method)
            
            # 找到所有匹配位置
            locations = np.where(result >= self.threshold)
            
            matches = []
            for pt in zip(*locations[::-1]):  # 切换x和y坐标
                matches.append({
                    'x': int(pt[0]),
                    'y': int(pt[1]),
                    'width': template_width,
                    'height': template_height,
                    'confidence': float(result[pt[1], pt[0]])
                })
            
            if matches:
                print(f"找到 {len(matches)} 个匹配项:")
                return matches
            else:
                print(f"未找到匹配的图片 (阈值: {self.threshold})")
                
                # 获取最高匹配度用于调试
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                print(f"最高匹配度: {max_val:.3f} (位置: {max_loc})")
                
                return None
                
        except Exception as e:
            print(f"模板匹配失败: {e}")
            return None
    
    def save_match_results(self, matches, template_path, output_file="found_coordinates.txt"):
        """
        保存匹配结果到文件
        
        Args:
            matches (list): 匹配结果列表
            template_path (str): 模板图片路径
            output_file (str): 输出文件路径
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"模板图片: {template_path}\n")
                f.write(f"匹配阈值: {self.threshold}\n")
                f.write("=" * 50 + "\n")
                
                for i, match in enumerate(matches, 1):
                    coord_info = f"匹配 {i}: 坐标({match['x']}, {match['y']}), 尺寸({match['width']}x{match['height']}), 置信度: {match['confidence']:.3f}"
                    print(f"  {coord_info}")
                    f.write(coord_info + "\n")
                    
            print(f"坐标信息已保存到: {os.path.abspath(output_file)}")
        except Exception as e:
            print(f"保存匹配结果失败: {e}")
    
    def set_threshold(self, threshold):
        """
        设置匹配阈值
        
        Args:
            threshold (float): 新的匹配阈值
        """
        self.threshold = threshold
        print(f"匹配阈值已设置为: {threshold}")

def find_image_in_screenshot(screenshot_array, template_path, threshold=0.8):
    """
    在截图中查找指定图片的便捷函数
    
    Args:
        screenshot_array: 截图数组
        template_path (str): 模板图片路径
        threshold (float): 匹配阈值
        
    Returns:
        list: 匹配结果列表
    """
    matcher = TemplateMatcher(threshold)
    return matcher.match_template(screenshot_array, template_path) 