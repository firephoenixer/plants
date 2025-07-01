import mss
import os
import cv2
import numpy as np

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
            
            return screenshot
            
    except Exception as e:
        print(f"截图失败: {e}")
        return None

def find_image_in_screenshot(screenshot, template_path):
    """在截图中查找指定图片并返回坐标"""
    try:
        # 检查模板图片是否存在
        if not os.path.exists(template_path):
            print(f"错误：模板图片不存在: {template_path}")
            return None
            
        # 将mss截图转换为OpenCV格式
        # mss返回的是BGRA格式，需要转换为BGR
        img_array = np.array(screenshot)
        screenshot_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
        
        # 读取模板图片
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"错误：无法读取模板图片: {template_path}")
            return None
            
        # 获取模板图片的尺寸
        template_height, template_width = template.shape[:2]
        
        # 使用模板匹配
        result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
        
        # 设置匹配阈值
        threshold = 0.8
        locations = np.where(result >= threshold)
        
        # 找到所有匹配位置
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
            coordinates_file = "found_coordinates.txt"
            with open(coordinates_file, 'w', encoding='utf-8') as f:
                f.write(f"模板图片: {template_path}\n")
                f.write(f"匹配阈值: {threshold}\n")
                f.write("=" * 50 + "\n")
                
                for i, match in enumerate(matches, 1):
                    coord_info = f"匹配 {i}: 坐标({match['x']}, {match['y']}), 尺寸({match['width']}x{match['height']}), 置信度: {match['confidence']:.3f}"
                    print(f"  {coord_info}")
                    f.write(coord_info + "\n")
                    
            print(f"坐标信息已保存到: {os.path.abspath(coordinates_file)}")
            return matches
        else:
            print(f"未找到匹配的图片 (阈值: {threshold})")
            
            # 获取最高匹配度用于调试
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print(f"最高匹配度: {max_val:.3f} (位置: {max_loc})")
            
            return None
            
    except Exception as e:
        print(f"图像匹配失败: {e}")
        return None

if __name__ == "__main__":
    print("开始全屏截图...")
    screenshot = take_screenshot()
    
    if screenshot:
        print("截图完成！")
        
        # 查找指定图片
        template_path = r"pic\general\featured.png"
        print(f"\n开始在截图中查找图片: {template_path}")
        
        matches = find_image_in_screenshot(screenshot, template_path)
        
        if matches:
            print(f"\n✅ 成功找到目标图片！")
            print(f"📍 第一个匹配项坐标: ({matches[0]['x']}, {matches[0]['y']})")
            print(f"📏 图片尺寸: {matches[0]['width']} x {matches[0]['height']}")
            print(f"🎯 匹配置信度: {matches[0]['confidence']:.3f}")
            
            # 截取807x631区域
            start_x = matches[0]['x']
            start_y = matches[0]['y']
            crop_width = 795
            crop_height = 620
            
            # 将截图转换为OpenCV格式
            img_array = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            # 获取截图尺寸以确保不越界
            img_height, img_width = screenshot_bgr.shape[:2]
            end_x = min(start_x + crop_width, img_width)
            end_y = min(start_y + crop_height, img_height)
            
            # 截取指定区域
            cropped_image = screenshot_bgr[start_y:end_y, start_x:end_x]
            
            # 保存为game.png
            cv2.imwrite("game.png", cropped_image)
            
            actual_width = end_x - start_x
            actual_height = end_y - start_y
            print(f"🎮 已截取游戏区域: {actual_width} x {actual_height}")
            print(f"💾 游戏截图已保存为: {os.path.abspath('game.png')}")
        else:
            print(f"\n❌ 未找到目标图片")
            print("💡 请检查:")
            print(f"   - 图片路径是否正确: {template_path}")
            print("   - 图片是否在当前屏幕上可见")
            print("   - 可能需要调整匹配阈值")
    else:
        print("❌ 截图失败，无法进行图像匹配")
