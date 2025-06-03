import numpy as np

from entity.agent import Agent


class Mtrx:
    def __init__(self, params, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.matrix(np.zeros((rows, cols)))
        self.params = params

        self.reward_list = []
        self.reward_remove_list = []

        self.update_timer = 0
        self.update_speed = 3

    def visualize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.matrix[i, j], end=" ")
            print()

    def update(self, dt):
        self.update_timer += dt
        if self.update_timer > self.update_speed:
            self.update_timer = 0

            temple = 0
            agent = Agent(self.params, (0,0))
            agent.alive = False
            while True:
                x = np.random.randint(0, self.rows)
                y = np.random.randint(0, self.cols)
                temple += 1
                if self.matrix[x, y] == 0 or temple >= 10:
                    self.matrix[x, y] = 1
                    agent.set_location((x, y))
                    agent.set_state("reward")
                    agent.alive = True
                    break

            if agent.is_alive():
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







