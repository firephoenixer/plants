# 游戏逻辑类
import my_mss
import my_opencv
import res

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
        self.is_active = False
        self.is_running = False
        self.is_paused = False
        self.is_game_won = False
        self.is_game_lost = False


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
                
                # 转换颜色格式从BGRA到BGR
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
        
    def start(self):
        print("游戏开始")
        
    def end(self):
        print("游戏结束")
        
    def update(self):
        print("游戏更新")