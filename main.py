import os
from my_mss import ScreenCapture, take_screenshot
from my_opencv import ImageProcessor, TemplateMatcher

def main():
    """主程序入口"""
    print("开始全屏截图...")
    
    # 使用封装的截图功能
    screenshot = take_screenshot()
    
    if screenshot:
        print("截图完成！")
        
        # 查找指定图片
        template_path = r"pic\general\featured.png"
        print(f"\n开始在截图中查找图片: {template_path}")
        
        # 创建图像处理器和模板匹配器
        img_processor = ImageProcessor()
        matcher = TemplateMatcher(threshold=0.8)
        
        # 将截图转换为OpenCV格式
        with ScreenCapture() as capture:
            screenshot_array = capture.screenshot_to_array(screenshot)
            
        if screenshot_array is not None:
            # 转换颜色格式从BGRA到BGR
            screenshot_bgr = img_processor.bgra_to_bgr(screenshot_array)
            
            if screenshot_bgr is not None:
                # 进行模板匹配
                matches = matcher.match_template(screenshot_bgr, template_path)
                
                if matches:
                    # 保存匹配结果
                    matcher.save_match_results(matches, template_path)
                    
                    print(f"\n✅ 成功找到目标图片！")
                    print(f"📍 第一个匹配项坐标: ({matches[0]['x']}, {matches[0]['y']})")
                    print(f"📏 图片尺寸: {matches[0]['width']} x {matches[0]['height']}")
                    print(f"🎯 匹配置信度: {matches[0]['confidence']:.3f}")
                    
                    # 截取游戏区域
                    start_x = matches[0]['x']
                    start_y = matches[0]['y']
                    crop_width = 795
                    crop_height = 620
                    
                    # 使用图像处理器裁剪图像
                    cropped_image = img_processor.crop_image(
                        screenshot_bgr, start_x, start_y, crop_width, crop_height
                    )
                    
                    if cropped_image is not None:
                        # 保存裁剪后的游戏截图
                        success = img_processor.save_image(cropped_image, "game.png")
                        
                        if success:
                            print(f"🎮 已截取游戏区域")
                            print(f"💾 游戏截图已保存为: {os.path.abspath('game.png')}")
                        else:
                            print("❌ 保存游戏截图失败")
                    else:
                        print("❌ 裁剪图像失败")
                else:
                    print(f"\n❌ 未找到目标图片")
                    print("💡 请检查:")
                    print(f"   - 图片路径是否正确: {template_path}")
                    print("   - 图片是否在当前屏幕上可见")
                    print("   - 可能需要调整匹配阈值")
            else:
                print("❌ 颜色格式转换失败")
        else:
            print("❌ 截图转换数组失败")
    else:
        print("❌ 截图失败，无法进行图像匹配")

if __name__ == "__main__":
    main()
