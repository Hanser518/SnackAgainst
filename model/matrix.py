import numpy as np

from model.agent import Agent


class Mtrx:
    def __init__(self, params, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.matrix(np.zeros((rows, cols)))
        self.params = params

        self.reward_list = []
        self.reward_remove_list = []

        self.update_timer = 0
        self.update_speed = 1

    def visualize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.matrix[i, j], end=" ")
            print()

    def update(self, dt):
        self.update_timer += dt
        if self.update_timer > self.update_speed and len(self.reward_list) < 20:
            self.update_timer = 0

            # 获取所有为0的位置
            zero_locations = np.argwhere(self.matrix == 0)

            if len(zero_locations) > 0:
                # 随机选择一个空位置
                x, y = zero_locations[np.random.randint(0, len(zero_locations))]
                self.matrix[x, y] = 1

                # 创建奖励agent
                agent = Agent(self.params, (x, y))
                agent.set_state("reward")
                agent.set_agent_label(Agent.REWARD_AGENT)
                agent.alive = True
                self.reward_list.append(agent)

        for agent in self.reward_list:
            agent.update(dt)

    def draw(self, screen):
        for agent in self.reward_list:
            screen.blit(agent.image, agent.rect)

    def crash(self, agent):
        for reward in self.reward_list:
            if reward.rect.colliderect(agent.rect):
                self.reward_list.remove(reward)
                return True
        return False
