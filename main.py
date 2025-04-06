import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Circle with Trail")

# Clock
clock = pygame.time.Clock()

# Circle settings
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 350
TRAIL_RADIUS = 10

# Ball settings
ball_pos = [CENTER[0], CENTER[1] - 100]
ball_vel = [4, 0]  # initial velocity
ball_radius = 20
gravity = 0.03

# Trail
trail = []
max_trail_length = 20000

def reflect(pos, vel):
    # Vector from center to ball
    cx, cy = CENTER
    dx = pos[0] - cx
    dy = pos[1] - cy
    dist = math.hypot(dx, dy)

    if dist >= RADIUS - ball_radius:
        # Normal vector
        nx = dx / dist
        ny = dy / dist

        # Dot product of velocity and normal
        dot = vel[0] * nx + vel[1] * ny

        # Reflect velocity
        vel[0] -= 2 * dot * nx
        vel[1] -= 2 * dot * ny

        # Pull ball just inside circle
        pos[0] = cx + (RADIUS - ball_radius - 1) * nx
        pos[1] = cy + (RADIUS - ball_radius - 1) * ny

running = True
while running:
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (30, 30, 30), CENTER, RADIUS, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    reflect(ball_pos, ball_vel)

    # Add to trail
    trail.append((ball_pos[0], ball_pos[1], pygame.time.get_ticks()))
    if len(trail) > max_trail_length:
        trail.pop(0)

    # Draw trail with rainbow colors
    for i, (x, y, t) in enumerate(trail):
        hue = (t * 0.1) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)
        pygame.draw.circle(screen, color, (int(x), int(y)), TRAIL_RADIUS)

    # Draw ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
