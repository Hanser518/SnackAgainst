import pygame

from model.agent import Agent
from model.matrix import Mtrx
from model.params import Params
from model.agent_link import AgentLink

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
against_link = AgentLink(params, location=(0, 0))

frame_count = 0
frame_limit = 240

font = pygame.font.Font("resource/font/HYPixel11pxU-2.ttf", 18)

access_speed = 0.0625

dt = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((18, 13, 15))

    agent_link.draw(screen)
    against_link.draw(screen)
    mtrx.draw(screen)

    press_keys = pygame.key.get_pressed()

    if press_keys[pygame.K_w]:
        agent_link.set_direction(0)
    if press_keys[pygame.K_s]:
        agent_link.set_direction(2)
    if press_keys[pygame.K_a]:
        agent_link.set_direction(3)
    if press_keys[pygame.K_d]:
        agent_link.set_direction(1)

    if press_keys[pygame.K_SPACE]:
        agent_link.access_speed(access_speed)

    # flip() the display to put your work on screen

    if mtrx.crash(agent_link.get_head_agent()):
        agent_link.add_agent_count()
    if mtrx.crash(against_link.get_head_agent()):
        against_link.add_agent_count()

    dt = clock.tick(frame_limit) / 1000

    agent_link.update(dt)

    against_link.set_direction_auto(mtrx)
    against_link.access_speed(0.0625)
    against_link.update(dt)

    mtrx.update(dt)
    if frame_count >= frame_limit:
        frame_count = 0
    else:
        frame_count += 1

    agent_length = font.render(f"Score: {agent_link.agent_count}", True, "white")
    length_rect = agent_length.get_rect()
    length_rect.topleft = (20, params.INFO_HEIGHT)
    screen.blit(agent_length, length_rect)

    agent_speed = font.render(f"Speed: {1 / agent_link.update_speed :.1f}", True, "white")
    speed_rect = agent_speed.get_rect()
    speed_rect.topleft = (20, speed_rect.height + length_rect.y)
    screen.blit(agent_speed, speed_rect)

    against_length = font.render(f"Ai Score: {against_link.agent_count}", True, "white")
    against_lengthrect = against_length.get_rect()
    against_lengthrect.topleft = (params.INFO_WIDTH // 2, params.INFO_HEIGHT)
    screen.blit(against_length, against_lengthrect)

    against_speed = font.render(f"Ai Speed: {1 / against_link.update_speed :.1f}", True, "white")
    against_speed_rect = against_speed.get_rect()
    against_speed_rect.topleft = (against_lengthrect.x, against_speed_rect.height + against_lengthrect.y)
    screen.blit(against_speed, against_speed_rect)

    rect_1 = (max(against_lengthrect.w,  against_speed_rect.w), max(against_lengthrect.h, against_speed_rect.h))

    pygame.display.set_caption(f"FPS：{clock.get_fps() :.1f}")

    pygame.display.flip()

pygame.quit()
