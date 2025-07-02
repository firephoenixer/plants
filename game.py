# 游戏逻辑类


class PlantsVsZombies:
    def __init__(self):
        self.is_open = False
        self.is_active = False
        self.is_running = False
        self.is_paused = False
        self.is_game_won = False
        self.is_game_lost = False
        

        
    def start(self):
        print("游戏开始")
        
    def end(self):
        print("游戏结束")
        
    def update(self):
        print("游戏更新")