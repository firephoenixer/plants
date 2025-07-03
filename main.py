import os
import time
import game
import pyautogui

def main():
    """主程序入口"""
    pvz_game = game.PlantsVsZombies()  # 创建游戏实例
    times = 0  # 循环次数
    print("开始逻辑循环...")
    while True:
        time.sleep(1)
        times += 1
        print("当前第{}次循环".format(times))
        pvz_game.find_game_feature()
        if pvz_game.is_open:
            print("游戏已打开, 起点坐标: ({}, {})".format(pvz_game.start_x, pvz_game.start_y))
        else:
            print("游戏未打开，程序结束，请核查原因...")
            break

        # 现在开始查找游戏的active_region区域的灰色像素点，返回其数量
        # 注意：HSV中V值范围是0-255，所以百分比需要转换
        # 检测浅灰色像素 (V:80% = 204)
        light_gray_count = pvz_game.get_pixel_count(pvz_game.game_screenshot, pvz_game.active_region, (0, 0, 204))
        print("浅灰色像素点数量: {}".format(light_gray_count))
        if light_gray_count > 0:
            print("游戏未激活，移动鼠标点击标题区域，激活游戏...")
            pvz_game.is_active = False
            # 移动鼠标点击标题区域，激活游戏
            pyautogui.moveTo(pvz_game.start_x + 60, pvz_game.start_y + 10)
            pyautogui.click()
            continue
        else:
            pvz_game.is_active = True
            print("游戏窗口处于激活状态...")

        # 检查“继续游戏”按钮是否存在，存在则按空格键继续游戏，不存在则返回False
        if_paused = pvz_game.check_and_continue_button(if_continue=False)
        if if_paused: continue  # 如果游戏暂停，则继续循环, 不执行下面的代码

        # 收集阳光
        pvz_game.collect_sun()







if __name__ == "__main__":
    main()
