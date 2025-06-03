from collections import deque

from entity.agent import Agent
from entity.params import Params


class AgentLink():
    def __init__(self, params: Params, location):
        self.update_timer = 0
        self.update_speed = 0.25
        self.direction = 1

        self.params = params
        self.w_limit, self.h_limit = params.get_matrix_size()
        self.agent_count = 3
        self.agent_deque = deque()
        self.add_agent(location)
        self.location = location

    def add_agent(self, location):
        agent = Agent(self.params, location)
        agent.set_state("light")
        agent.set_speed(self.update_speed)
        self.agent_deque.append(agent)

        remove_list = []
        for index, agent in enumerate(self.agent_deque):
            if index < len(self.agent_deque) - self.agent_count:
                if not agent.confirm_state("extinct"):
                    agent.set_state("extinct")
            if not agent.is_alive():
                remove_list.append(agent)

        for agent in remove_list:
            self.agent_deque.remove(agent)
        self.update_speed = 0.25

    def add_agent_count(self):
        self.agent_count += 1

    def set_direction(self, direction: int):
        anti_direction = (self.direction + 2) % 4
        if direction != anti_direction:
            self.direction = direction

    def reset_agent_count(self):
        self.agent_count = 3

    def move(self):
        while self.is_out_of_limit():
            self.direction = (self.direction + 1) % 4
        match self.direction:
            case 0:  # 上
                self.location = (self.location[0], max(0, self.location[1] - 1))
            case 1:  # 右
                self.location = (min(self.w_limit - 1, self.location[0] + 1), self.location[1])
            case 2:  # 下
                self.location = (self.location[0], min(self.h_limit - 1, self.location[1] + 1))
            case 3:  # 左
                self.location = (max(0, self.location[0] - 1), self.location[1])

        self.add_agent(self.location)
        crashed, index = self.is_self_crashed()
        if crashed:
            for i in range(index):
                self.agent_deque[i].set_state("extinct")
            self.agent_count -= index

    def update(self, dt):
        for agent in self.agent_deque:
            if agent.is_dynamic():
                agent.update(dt)
        self.update_timer += dt
        if self.update_timer > self.update_speed:
            self.update_timer = 0
            if self.direction >= 0:
                self.move()

    def draw(self, screen):
        for agent in self.agent_deque:
            screen.blit(agent.image, agent.rect)

    def get_head_agent(self):
        return self.agent_deque[-1]

    def get_next_pos(self, location, direction):
        match direction:
            case 0:  # 上
                return location[0], location[1] - 1
            case 1:  # 右
                return location[0] + 1, location[1]
            case 2:  # 下
                return location[0], location[1] + 1
            case 3:  # 左
                return location[0] - 1, location[1]

    def access_speed(self):
        self.update_speed = 0.124

    def is_out_of_limit(self):
        pos = self.get_next_pos(self.location, self.direction)
        if pos[0] < 0 or pos[0] >= self.w_limit or pos[1] < 0 or pos[1] >= self.h_limit:
            return True

    def is_self_crashed(self):
        head = self.get_head_agent()
        for index, agent in enumerate(self.agent_deque):
            if agent != head:
                if head.rect.colliderect(agent.rect):
                    return True, index
        return False, -1
