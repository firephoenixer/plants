import os
import time
import game

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

    

if __name__ == "__main__":
    main()
