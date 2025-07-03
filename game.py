# 游戏逻辑类
import my_mss
import my_opencv
import res
import numpy as np
import cv2
import pyautogui
import time

class PlantsVsZombies:
    def __init__(self):
        self.resource = res.Resource()
        self.mss = my_mss.ScreenCapture()
        self.opencv = my_opencv.ImageProcessor()
        self.is_open = False
        self.start_x = -1  # 游戏的特征图片的左上角坐标
        self.start_y = -1  # 游戏的特征图片的左上角坐标
        self.game_width = 795
        self.game_height = 620
        self.game_screenshot = None
        self.is_active = False
        self.is_running = False
        self.is_paused = False
        self.is_game_won = False
        self.is_game_lost = False

        # 定义窗口激活状态的特征区域
        self.active_region = {
            "x": 19,
            "y": 1,
            "width": 104,
            "height": 19
        }

        # 定义“继续游戏”按钮的特征区域
        self.continue_button_region = {
            "x": 216,
            "y": 432,
            "width": 354,
            "height": 82
        }


    # 查找游戏特征图片，找到则保存其坐标，找不到则提示用户核查原因，并返回False
    def find_game_feature(self):
        try:
            print("正在查找游戏特征图片...")
            
            # 截取全屏
            with self.mss as capture:
                screenshot = capture.take_full_screenshot("screen.png")
                
                if screenshot is None:
                    print("❌ 截图失败")
                    return False
                
                # 将截图转换为OpenCV格式
                screenshot_array = capture.screenshot_to_array(screenshot)
                if screenshot_array is None:
                    print("❌ 截图转换数组失败")
                    return False
                
                # 转换颜色格式从BGRA到BGR, A通道丢弃,对于计算机视觉来说，忽略A通道
                screenshot_bgr = self.opencv.bgra_to_bgr(screenshot_array)
                if screenshot_bgr is None:
                    print("❌ 颜色格式转换失败")
                    return False
                
                # 创建模板匹配器
                matcher = my_opencv.TemplateMatcher(threshold=0.8)
                
                # 进行模板匹配
                matches = matcher.match_template(screenshot_bgr, self.resource.featured_path)
                
                if matches and len(matches) > 0:
                    # 保存第一个匹配项的坐标
                    self.start_x = matches[0]['x']
                    self.start_y = matches[0]['y']
                    # 设置游戏状态
                    self.is_open = True
                    self.get_game_screenshot(screenshot_bgr)
                    return True
                else:
                    print("❌ 未找到游戏特征图片")
                    print("💡 请检查:")
                    print(f"   - 图片路径是否正确: {self.resource.featured_path}")
                    print("   - 植物大战僵尸游戏是否在当前屏幕上可见")
                    print("   - 游戏窗口是否被其他窗口遮挡")
                    print("   - 可能需要调整匹配阈值")
                    
                    # 重置坐标和状态
                    self.start_x = -1
                    self.start_y = -1
                    self.is_open = False
                    
                    return False
                    
        except Exception as e:
            print(f"❌ 查找游戏特征图片时发生错误: {e}")
            self.start_x = -1
            self.start_y = -1
            self.is_open = False
            return False

    # 传入全屏截图，截取self.start_x, self.start_y, self.game_width, self.game_height的区域，并返回该区域的截图，并保存在self.game_screenshot中
    def get_game_screenshot(self, screenshot_bgr):
        try:
            if self.start_x == -1 or self.start_y == -1:
                print("❌ 游戏坐标未初始化，无法截取游戏区域")
                return None
            
            # 使用图像处理器裁剪游戏区域
            self.game_screenshot = self.opencv.crop_image(
                screenshot_bgr,
                self.start_x,
                self.start_y, 
                self.game_width,
                self.game_height
            )
            
            if self.game_screenshot is not None:
                # 保存游戏截图到文件
                success = self.opencv.save_image(self.game_screenshot, "game.png")
                
                if success:
                    print(f"🎮 游戏区域截图已保存: {self.game_width}x{self.game_height}")
                    print(f"📍 起始坐标: ({self.start_x}, {self.start_y})")
                else:
                    print("❌ 保存游戏截图失败")
                
                return self.game_screenshot
            else:
                print("❌ 截取游戏区域失败")
                return None
                
        except Exception as e:
            print(f"❌ 获取游戏截图时发生错误: {e}")
            self.game_screenshot = None
            return None

    # 在指定区域获得指定颜色的像素点数量，返回该区域中指定颜色的像素点数量
    def get_pixel_count(self, game_screenshot_bgr, region, color, tolerance=(0, 0, 10)):
        """
        统计指定区域中特定颜色的像素点数量
        
        Args:
            game_screenshot_bgr: BGR格式的游戏截图
            region (dict): 区域字典，包含x, y, width, height
            color (tuple): HSV颜色值，如(120, 255, 255)代表绿色
            tolerance (tuple): HSV各通道的容差，默认为(10, 50, 50)，分别对应H、S、V的容差
            
        Returns:
            int: 匹配颜色的像素点数量，失败时返回-1
        """
        try:
            if game_screenshot_bgr is None:
                print("❌ 游戏截图为空")
                return -1
            
            # 验证区域参数
            if not all(key in region for key in ['x', 'y', 'width', 'height']):
                print("❌ 区域参数不完整")
                return -1
            
            # 获取图像尺寸
            img_height, img_width = game_screenshot_bgr.shape[:2]
            
            # 计算实际的区域边界，确保不越界
            x = max(0, region['x'])
            y = max(0, region['y'])
            end_x = min(x + region['width'], img_width)
            end_y = min(y + region['height'], img_height)
            
            # 截取指定区域
            roi_bgr = game_screenshot_bgr[y:end_y, x:end_x]
            
            if roi_bgr.size == 0:
                print("❌ 截取的区域为空")
                return -1
            
            # 将截取的区域保存到文件
            cv2.imwrite("working.png", roi_bgr)
            
            # 将BGR转换为HSV
            roi_hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
            
            # 将颜色值和容差转换为numpy数组
            target_color = np.array(color, dtype=np.uint8)
            tolerance_array = np.array(tolerance, dtype=np.uint8)
            
            # 计算HSV颜色范围
            lower_bound = np.maximum(target_color - tolerance_array, [0, 0, 0])
            upper_bound = np.minimum(target_color + tolerance_array, [179, 255, 255])
            
            # 特殊处理色相(H)通道的环形特性
            if color[0] - tolerance[0] < 0:
                # 色相跨越0度的情况（如红色）
                mask1 = cv2.inRange(roi_hsv, 
                                  np.array([0, lower_bound[1], lower_bound[2]]),
                                  np.array([color[0] + tolerance[0], upper_bound[1], upper_bound[2]]))
                mask2 = cv2.inRange(roi_hsv,
                                  np.array([180 + color[0] - tolerance[0], lower_bound[1], lower_bound[2]]),
                                  np.array([179, upper_bound[1], upper_bound[2]]))
                mask = cv2.bitwise_or(mask1, mask2)
            elif color[0] + tolerance[0] > 179:
                # 色相跨越179度的情况
                mask1 = cv2.inRange(roi_hsv,
                                  np.array([lower_bound[0], lower_bound[1], lower_bound[2]]),
                                  np.array([179, upper_bound[1], upper_bound[2]]))
                mask2 = cv2.inRange(roi_hsv,
                                  np.array([0, lower_bound[1], lower_bound[2]]),
                                  np.array([color[0] + tolerance[0] - 180, upper_bound[1], upper_bound[2]]))
                mask = cv2.bitwise_or(mask1, mask2)
            else:
                # 正常情况
                mask = cv2.inRange(roi_hsv, lower_bound, upper_bound)
            
            # 统计匹配的像素数量
            pixel_count = cv2.countNonZero(mask)
            
            # 输出调试信息
            actual_width = end_x - x
            actual_height = end_y - y
            total_pixels = actual_width * actual_height
            percentage = (pixel_count / total_pixels * 100) if total_pixels > 0 else 0
            
            print(f"🔍 区域({x},{y}) {actual_width}x{actual_height}, HSV颜色{color}, 容差{tolerance}")
            print(f"📊 匹配像素: {pixel_count}/{total_pixels} ({percentage:.1f}%)")
            
            return int(pixel_count)
            
        except Exception as e:
            print(f"❌ 统计像素点数量时发生错误: {e}")
            return -1

    # 检查“继续游戏”按钮是否存在，存在则按空格键继续游戏，不存在则返回False
    def check_and_continue_button(self, if_continue=True):
        """
        检查游戏中的"继续"按钮是否存在，如果存在则按空格键
        
        Returns:
            bool: 找到按钮并成功按键返回True，否则返回False
        """
        try:
            if self.game_screenshot is None:
                print("❌ 游戏截图为空，无法检查继续按钮")
                return False
            
            if not hasattr(self, 'continue_button_region'):
                print("❌ 继续按钮区域未定义")
                return False
            
            print("🔍 正在检查继续按钮...")
            
            # 从游戏截图中裁剪继续按钮区域
            region = self.continue_button_region
            button_region = self.opencv.crop_image(
                self.game_screenshot,
                region['x'],
                region['y'],
                region['width'],
                region['height']
            )
            
            if button_region is None:
                print("❌ 裁剪继续按钮区域失败")
                return False
            
            # 创建模板匹配器
            matcher = my_opencv.TemplateMatcher(threshold=0.8)
            
            # 在裁剪的区域中查找继续按钮
            matches = matcher.match_template(button_region, self.resource.continue_button_path)
            
            if matches and len(matches) > 0:
                # 找到了继续按钮
                button_x = matches[0]['x']
                button_y = matches[0]['y']
                confidence = matches[0]['confidence']
                
                print(f"✅ 找到继续按钮！")
                print(f"📍 按钮在区域内坐标: ({button_x}, {button_y})")
                print(f"🎯 匹配置信度: {confidence:.3f}")
                
                if if_continue:
                    # 按空格键继续游戏
                    pyautogui.press('space')
                    print("⌨️ 已按下空格键继续游戏")
                
                return True  # 表示刚才游戏处于暂停状态
            else:
                print("❌ 未找到继续按钮")
                return False  # 表示刚才游戏未发现暂停特征
                
        except Exception as e:
            print(f"❌ 检查继续按钮时发生错误: {e}")
            return False

    # 全屏匹配self.resource.sun_path，如果找到，则分别全部点击，以完成收集阳光
    def collect_sun(self):
        """
        在游戏截图中查找所有阳光并点击收集
        """
        try:
            if self.game_screenshot is None:
                print("❌ 游戏截图为空，无法收集阳光")
                return
            
            print("🌞 正在查找阳光...")
            
            # 创建模板匹配器，降低阈值以提高检测率
            matcher = my_opencv.TemplateMatcher(threshold=0.9)
            
            # 在游戏截图中查找所有阳光
            matches = matcher.match_template(self.game_screenshot, self.resource.sun_path)
            
            if matches and len(matches) > 0:
                print(f"✅ 找到 {len(matches)} 个阳光！")
                
                # 遍历所有阳光并点击收集
                for i, match in enumerate(matches):
                    # 计算阳光中心点坐标（在游戏截图中的相对坐标）
                    sun_x = match['x'] + match['width'] // 2
                    sun_y = match['y'] + match['height'] // 2
                    
                    # 转换为屏幕绝对坐标
                    screen_x = self.start_x + sun_x
                    screen_y = self.start_y + sun_y
                    
                    print(f"🌞 收集第 {i+1} 个阳光: 游戏坐标({sun_x}, {sun_y}) → 屏幕坐标({screen_x}, {screen_y})")
                    
                    # 点击阳光
                    pyautogui.click(screen_x, screen_y)
                    
                    # 短暂延迟避免点击过快
                    time.sleep(0.1)
                
                print(f"💰 成功收集了 {len(matches)} 个阳光！")
                
            else:
                print("❌ 未找到阳光")
                
        except Exception as e:
            print(f"❌ 收集阳光时发生错误: {e}")










    def start(self):
        print("游戏开始")
        
    def end(self):
        print("游戏结束")
        
    def update(self):
        print("游戏更新")