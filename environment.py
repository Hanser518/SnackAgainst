import numpy as np
import pygame
from mpmath import scorergi

from model.agent_link import AgentLink
from model.matrix import Mtrx
from model.params import Params


class Environment:
    def __init__(self):
        pygame.init()
        self.params = Params()
        self.screen = pygame.display.set_mode(self.params.get_window_size())
        self.clock = pygame.time.Clock()
        self.running = True

        width, height = self.params.MATRIX_SIZE
        self.mtrx = Mtrx(self.params, width, height)

        # agent = Agent(params, location=(width // 2, height // 2))
        self.agent_link = AgentLink(self.params, location=(width // 2, height // 2))
        self.against_link = AgentLink(self.params, location=(0, 0))
        # self.against_link.set_no_slow()
        # self.against_link.set_speed(0.0625)

        self.frame_count = 0
        self.frame_limit = 240

        self.font = pygame.font.Font("resource/font/HYPixel11pxU-2.ttf", 18)

        self.access_speed = 0.0625

        self.dt = 1
        self.update_frame = False
        self.dt_record = 0

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((18, 13, 15))

        self.agent_link.draw(self.screen)
        self.against_link.draw(self.screen)
        self.mtrx.draw(self.screen)

        # self.agent_link.set_direction_auto(self.mtrx)

        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_w]:
            self.agent_link.set_direction(0)
        if press_keys[pygame.K_s]:
            self.agent_link.set_direction(2)
        if press_keys[pygame.K_a]:
            self.agent_link.set_direction(3)
        if press_keys[pygame.K_d]:
            self.agent_link.set_direction(1)

        if press_keys[pygame.K_SPACE]:
            self.agent_link.access_speed(self.access_speed)

        if self.mtrx.crash(self.agent_link.get_head_agent()):
            self.agent_link.add_agent_count()
        if self.mtrx.crash(self.against_link.get_head_agent()):
            self.against_link.add_agent_count()

        dt = self.clock.tick(self.frame_limit) / 1000
        self.dt_record += dt
        if self.dt_record > self.agent_link.update_speed:
            self.update_frame = True
            self.dt_record = 0
        else:
            self.update_frame = False

        self.against_link.set_direction_auto(self.mtrx)
        self.agent_link.update(dt)
        self.against_link.update(dt)

        self.mtrx.update(dt)
        if self.frame_count >= self.frame_limit:
            self.frame_count = 0
        else:
            self.frame_count += 1

        values = {"player 1": self.agent_link, "ai player": self.against_link}
        self.show_agent_info(values)

        pygame.display.set_caption(f"FPS：{self.clock.get_fps() :.1f}")

        pygame.display.flip()

    def show_agent_info(self, values):
        count = len(values)
        index = 0
        for name, agent in values.items():
            agent_score = self.font.render(f"{name} score: {agent.score_record}", True, "white")
            score_rect = agent_score.get_rect()
            score_rect.topleft = (index / count * self.params.INFO_WIDTH, self.params.INFO_HEIGHT)
            self.screen.blit(agent_score, score_rect)

            agent_speed = self.font.render(f"Speed: {1 / agent.update_speed :.1f}", True, "white")
            speed_rect = agent_speed.get_rect()
            speed_rect.topleft = (score_rect.x, speed_rect.height + score_rect.y)
            self.screen.blit(agent_speed, speed_rect)

            agent_length = self.font.render(f"Length: {agent.agent_count}", True, "white")
            length_rect = agent_length.get_rect()
            length_rect.topleft = (index / count * self.params.INFO_WIDTH, length_rect.height + speed_rect.y)
            self.screen.blit(agent_length, length_rect)

            index += 1

    def get_agent_state(self, agent: AgentLink):
        reward_map = self.mtrx.matrix
        agent_map = np.zeros_like(reward_map, dtype=np.float32)
        position_map = np.zeros_like(reward_map, dtype=np.float32)

        agent_group = agent.agent_group
        for agent_sub in agent_group:
            agent_map[agent_sub.location] = 1.0

        head_agent = agent.get_head_agent()
        position_map[head_agent.location] = 1.0

        return np.stack([position_map, agent_map, reward_map], axis=2)

    def get_state_shape(self):
        return self.mtrx.matrix.shape + (3,)

    def set_action(self, agent: AgentLink, action: int):
        agent.set_direction(action)

    def get_agent_score(self, agent: AgentLink):
        return agent.score_record

    def get_agent_length(self, agent: AgentLink):
        return agent.agent_count

    def get_agent_action(self, agent: AgentLink):
        return agent.direction


if __name__ == "__main__":
    env = Environment()
    while env.running:
        env.run()
