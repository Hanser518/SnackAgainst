from collections import deque
import pygame.sprite
from model.params import Params

class Agent(pygame.sprite.Sprite):

    NORMAL_AGENT = "agent"
    REWARD_AGENT = "reward"
    BUFF_AGENT = "buff"
    PREDICT_AGENT = "predict"

    def __init__(self, params: Params, location):
        super().__init__()
        self.params = params
        self.location = location

        # 初始化尺寸参数
        self.w_size, self.h_size = self.params.get_window_size()
        self.w_limit, self.h_limit = self.params.get_matrix_size()
        self.size = self.params.BLOCK_SIZE

        # 预加载所有动画帧
        self.load_animation_frames()

        # 初始化动画状态
        self.frame_index = 0
        self.animation_speed = 0.2  # 每帧动画变化速度
        self.animation_timer = 0

        # 初始化位置
        self.rect = self.image.get_rect()
        self.rect.x = self.location[0] * self.size
        self.rect.y = self.location[1] * self.size

        self.label = "agent"
        self.alive = True

    def load_animation_frames(self):
        """预加载所有动画帧到内存"""
        # 静态帧
        self.static_frame = pygame.image.load("resource/agent/agent_static.png").convert_alpha()
        self.head_frame = pygame.image.load("resource/agent/agent_head.png").convert_alpha()
        self.reward_frame = pygame.image.load("resource/agent/agent_reward.png").convert_alpha()
        self.predict_frame = pygame.image.load("resource/agent/agent_predict.png").convert_alpha()

        # 动态帧序列
        self.animation_frames = {}

        self.frame_state = "light"
        self.animation_frames["light"] = []
        self.animation_frames["extinct"] = []
        self.animation_frames["reward"] = []

        for i in range(6):
            frame = pygame.image.load(f"resource/agent/agent_light_{i}.png").convert_alpha()
            self.animation_frames["light"].append(frame)

            frame = pygame.image.load(f"resource/agent/agent_extinct_{i}.png").convert_alpha()
            self.animation_frames["extinct"].append(frame)

            frame = pygame.image.load(f"resource/agent/agent_reward_{i}.png").convert_alpha()
            self.animation_frames["reward"].append(frame)

        # 当前显示图像（初始为静态帧）
        self.image = pygame.transform.smoothscale(self.animation_frames["light"][0], (self.size, self.size))

    def update(self, dt):
        """更新动画状态"""
        self.animation_timer += dt

        if self.frame_state == "static":
            self.image = pygame.transform.smoothscale(self.static_frame, (self.size, self.size))
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.frame_state == "head":
            self.image = pygame.transform.smoothscale(self.head_frame, (self.size, self.size))
            self.rect = self.image.get_rect(center=self.rect.center)
            self.frame_state = "static"

        elif self.frame_state == "reward_finish":
            self.image = pygame.transform.smoothscale(self.reward_frame, (self.size, self.size))
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.frame_state == "predict":
            self.image = pygame.transform.smoothscale(self.predict_frame, (self.size, self.size))
            self.rect = self.image.get_rect(center=self.rect.center)

        elif self.frame_state == "light" or self.frame_state == "extinct" or self.frame_state == "reward":
            # 控制动画更新频率
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                # 更新帧索引
                if self.frame_index > len(self.animation_frames[self.frame_state]) - 1:
                    if self.frame_state == "light":
                        self.set_state("head")
                    elif self.frame_state == "extinct":
                        self.kill()
                        self.alive = False
                    elif self.frame_state == "reward":
                        self.set_state("reward_finish")
                    return

                # 更新显示图像
                current_frame = self.animation_frames[self.frame_state][self.frame_index]
                self.image = pygame.transform.smoothscale(current_frame, (self.size, self.size))
                self.rect = self.image.get_rect(center=self.rect.center)

                self.frame_index += 1

    def set_state(self, state: str):
        self.frame_index = 0
        self.frame_state = state

    def set_speed(self, interval):
        self.animation_speed = interval / 6

    def set_location(self, locatin):
        self.rect.x = locatin[0] * self.size
        self.rect.y = locatin[1] * self.size

    def set_agent_label(self, label):
        self.label = label

    def get_agent_label(self):
        return self.label

    def confirm_state(self, state: str):
        if self.frame_state == state:
            return True

    def reset_size(self):
        """重置尺寸"""
        self.size = self.w_size // self.w_limit
        self.image = pygame.transform.smoothscale(self.static_frame, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.location[0] * self.size
        self.rect.y = self.location[1] * self.size

    def is_alive(self):
        return self.alive

    def is_dynamic(self):
        # if self.confirm_state("static"):
        #     return True
        # else:
        #     return self.confirm_state("light") or self.confirm_state("extinct") or self.confirm_state("reward")
        return True
