import numpy as np
import pygame

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
        self.against_link.set_no_slow()
        self.against_link.set_speed(0.0625)

        self.frame_count = 0
        self.frame_limit = 240

        self.font = pygame.font.Font("resource/font/HYPixel11pxU-2.ttf", 18)

        self.access_speed = 0.0625

        self.dt = 1

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((18, 13, 15))

        self.agent_link.draw(self.screen)
        self.against_link.draw(self.screen)
        self.mtrx.draw(self.screen)

        self.agent_link.set_direction_auto(self.mtrx)

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

        # flip() the display to put your work on screen

        if self.mtrx.crash(self.agent_link.get_head_agent()):
            self.agent_link.add_agent_count()
        if self.mtrx.crash(self.against_link.get_head_agent()):
            self.against_link.add_agent_count()

        dt = self.clock.tick(self.frame_limit) / 1000
        self.agent_link.update(dt)

        self.against_link.set_direction_auto(self.mtrx)
        self.against_link.update(dt)

        self.mtrx.update(dt)
        if self.frame_count >= self.frame_limit:
            self.frame_count = 0
        else:
            self.frame_count += 1

        agent_length = self.font.render(f"Score: {self.agent_link.agent_count}", True, "white")
        length_rect = agent_length.get_rect()
        length_rect.topleft = (20, self.params.INFO_HEIGHT)
        self. screen.blit(agent_length, length_rect)

        agent_speed = self.font.render(f"Speed: {1 / self.agent_link.update_speed :.1f}", True, "white")
        speed_rect = agent_speed.get_rect()
        speed_rect.topleft = (20, speed_rect.height + length_rect.y)
        self.screen.blit(agent_speed, speed_rect)

        against_length = self.font.render(f"Ai Score: {self.against_link.agent_count}", True, "white")
        against_lengthrect = against_length.get_rect()
        against_lengthrect.topleft = (self.params.INFO_WIDTH // 2, self.params.INFO_HEIGHT)
        self.screen.blit(against_length, against_lengthrect)

        against_speed = self.font.render(f"Ai Speed: {1 / self.against_link.update_speed :.1f}", True, "white")
        against_speed_rect = against_speed.get_rect()
        against_speed_rect.topleft = (against_lengthrect.x, against_speed_rect.height + against_lengthrect.y)
        self.screen.blit(against_speed, against_speed_rect)

        pygame.display.set_caption(f"FPS：{self.clock.get_fps() :.1f}")

        pygame.display.flip()

    def trans_state(self):
        reward_map = self.mtrx.matrix
        agent_map = np.zeros_like(reward_map)
        position_map = np.zeros_like(reward_map)

        agent_group = self.against_link.agent_group
        for agent in agent_group:
            agent_map[agent.location] = 1

        head_agent = self.against_link.get_head_agent()
        position_map[head_agent.location] = 1

        return np.stack([reward_map, agent_map, position_map], axis=2)

if __name__ == "__main__":
    env = Environment()
    while env.running:
        env.run()
