import pygame

from entity.agent import Agent
from entity.matrix import Mtrx
from entity.params import Params
from entity.agent_link import AgentLink

# pygame setup
pygame.init()
params = Params()
screen = pygame.display.set_mode(params.get_window_size())
clock = pygame.time.Clock()
running = True

width, height = params.MATRIX_SIZE
mtrx = Mtrx(params, width, height)

# agent = Agent(params, location=(width // 2, height // 2))
agent_link = AgentLink(params, location=(width // 2, height // 2))
agent = Agent(params, (30, 10))

frame_count = 0
frame_limit = 120

dt = 1

player_pos = pygame.Vector2(80, 45)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "gray", player_pos, 40)

    # screen.blit(agent.image, agent.rect)
    agent_link.draw(screen)
    mtrx.draw(screen)

    press_keys = pygame.key.get_pressed()

    if press_keys[pygame.K_w]:
        player_pos.y -= 300 * dt
        agent_link.set_direction(0)
    if press_keys[pygame.K_s]:
        player_pos.y += 300 * dt
        agent_link.set_direction(2)
    if press_keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        agent_link.set_direction(3)
    if press_keys[pygame.K_d]:
        player_pos.x += 300 * dt
        agent_link.set_direction(1)

    if press_keys[pygame.K_SPACE]:
        agent_link.access_speed()

    # flip() the display to put your work on screen

    if mtrx.crash(agent_link.get_head_agent()):
        agent_link.add_agent_count()

    dt = clock.tick(frame_limit) / 1000
    agent_link.update(dt)
    mtrx.update(dt)
    if frame_count >= frame_limit:
        frame_count = 0
    else:
        frame_count += 1

    pygame.display.flip()

pygame.quit()
