import os
from my_mss import ScreenCapture, take_screenshot
from my_opencv import ImageProcessor, TemplateMatcher
import time

def main():
    """主程序入口"""
    times = 0  # 循环次数
    print("开始逻辑循环...")
    while True:
        time.sleep(1)
        print("当前第{}次循环".format(times))
        times += 1
        

    

if __name__ == "__main__":
    main()
