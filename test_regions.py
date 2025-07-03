#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试植物菜单区域和战线区域绘制
"""
import game
import cv2

def test_regions():
    """测试区域绘制功能"""
    print("=== 区域绘制测试 ===")
    
    # 创建游戏实例
    pvz_game = game.PlantsVsZombies()
    
    try:
        # 查找游戏窗口
        print("1. 查找游戏窗口...")
        pvz_game.find_game_feature()
        
        if not pvz_game.is_open:
            print("❌ 未找到游戏窗口，请确保游戏正在运行")
            return
        
        print(f"✅ 找到游戏窗口，起点坐标: ({pvz_game.start_x}, {pvz_game.start_y})")
        
        # 测试不同的绘制功能
        print("\n2. 测试植物菜单区域绘制（红色）...")
        pvz_game.draw_plant_menu_region()
        
        print("\n3. 测试战线区域绘制（蓝色）+ 种植位置（绿色）...")
        pvz_game.draw_line_region()
        
        print("\n4. 测试仅绘制种植位置（绿色）...")
        # 重置绘制状态
        pvz_game.reset_plant_menu_drawn()
        pvz_game.reset_line_drawn()
        
        # 仅绘制种植位置
        pvz_game.draw_plant_positions_only()
        
        print("\n5. 测试同时绘制所有区域...")
        # 重置绘制状态
        pvz_game.reset_plant_menu_drawn()
        pvz_game.reset_line_drawn()
        
        # 同时绘制所有区域
        pvz_game.draw_all_regions()
        
        print("\n✅ 所有测试完成！")
        print("\n生成的图像文件：")
        print("- game_with_plant_menu_regions.png: 植物菜单区域（红色）")
        print("- game_with_line_regions.png: 战线区域（蓝色）+ 种植位置（绿色）")
        print("- game_with_plant_positions.png: 仅种植位置（绿色）")
        print("- game_with_all_regions.png: 所有区域（红色+蓝色+绿色）")
        
        # 显示最终图像
        if pvz_game.game_screenshot is not None:
            cv2.imshow('All Regions', pvz_game.game_screenshot)
            print("\n按任意键关闭显示窗口...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    finally:
        # 清理资源
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_regions() 