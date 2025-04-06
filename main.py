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

# Ball settings
ball_pos = [CENTER[0], CENTER[1] - 100]
ball_vel = [4, 0]  # initial velocity
ball_radius = 10
gravity = 0.3

# Trail
trail = []
max_trail_length = 200

# Spinning Circles with gaps
class SpinningCircle:
    def __init__(self, radius):
        self.radius = radius
        self.angle = random.uniform(0, 360)
        self.speed = random.uniform(-1, 1)
        self.gap_angle = random.uniform(30, 50)
        self.active = True

    def update(self):
        self.angle = (self.angle + self.speed) % 360

    def draw(self, surface):
        if not self.active:
            return
        start_angle = math.radians(self.angle)
        end_angle = math.radians((self.angle + 360 - self.gap_angle) % 360)
        if end_angle < start_angle:
            pygame.draw.arc(surface, (100, 100, 255),
                            (CENTER[0] - self.radius, CENTER[1] - self.radius, self.radius * 2, self.radius * 2),
                            start_angle, math.radians(360), 3)
            pygame.draw.arc(surface, (100, 100, 255),
                            (CENTER[0] - self.radius, CENTER[1] - self.radius, self.radius * 2, self.radius * 2),
                            math.radians(0), end_angle, 3)
        else:
            pygame.draw.arc(surface, (100, 100, 255),
                            (CENTER[0] - self.radius, CENTER[1] - self.radius, self.radius * 2, self.radius * 2),
                            start_angle, end_angle, 3)

    def is_inside_gap(self, pos):
        if not self.active:
            return False
        dx, dy = pos[0] - CENTER[0], pos[1] - CENTER[1]
        dist = math.hypot(dx, dy)
        if abs(dist - self.radius) > ball_radius:
            return False
        angle = math.degrees(math.atan2(dy, dx)) % 360
        gap_start = self.angle % 360
        gap_end = (self.angle + self.gap_angle) % 360
        if gap_start < gap_end:
            return gap_start <= angle <= gap_end
        else:
            return angle >= gap_start or angle <= gap_end

    def reflect(self, pos, vel):
        if not self.active:
            return
        dx, dy = pos[0] - CENTER[0], pos[1] - CENTER[1]
        dist = math.hypot(dx, dy)
        if abs(dist - self.radius) <= ball_radius:
            if self.is_inside_gap(pos):
                self.explode()
                return
            # Only bounce if not inside gap
            if not self.is_inside_gap(pos):
                nx = dx / dist
                ny = dy / dist
                dot = vel[0] * nx + vel[1] * ny
                vel[0] -= 2 * dot * nx
                vel[1] -= 2 * dot * ny
                pos[0] = CENTER[0] + (self.radius - ball_radius - 1) * nx
                pos[1] = CENTER[1] + (self.radius - ball_radius - 1) * ny

    def explode(self):
        self.active = False
        for _ in range(30):
            particles.append([ball_pos[:], [random.uniform(-5, 5), random.uniform(-5, 5)], random.choice([(255, 0, 0), (255, 255, 0), (255, 150, 0)]), 30])

# Explosion particles
particles = []

# Create spinning circles
spinning_circles = [SpinningCircle(RADIUS - 50 * i) for i in range(1, 6)]

def reflect_main_circle(pos, vel):
    cx, cy = CENTER
    dx = pos[0] - cx
    dy = pos[1] - cy
    dist = math.hypot(dx, dy)

    if dist >= RADIUS - ball_radius:
        nx = dx / dist
        ny = dy / dist
        dot = vel[0] * nx + vel[1] * ny
        vel[0] -= 2 * dot * nx
        vel[1] -= 2 * dot * ny
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

    reflect_main_circle(ball_pos, ball_vel)
    for circle in spinning_circles:
        circle.reflect(ball_pos, ball_vel)

    # Update and draw spinning circles
    for circle in spinning_circles:
        circle.update()
        circle.draw(screen)

    # Add to trail
    trail.append((ball_pos[0], ball_pos[1], pygame.time.get_ticks()))
    if len(trail) > max_trail_length:
        trail.pop(0)

    # Draw trail with rainbow colors
    for i, (x, y, t) in enumerate(trail):
        hue = (t * 0.1) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)
        pygame.draw.circle(screen, color, (int(x), int(y)), 4)

    # Draw explosion particles
    for particle in particles[:]:
        pos, vel, color, life = particle
        pos[0] += vel[0]
        pos[1] += vel[1]
        life -= 1
        pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 3)
        particle[3] = life
        if life <= 0:
            particles.remove(particle)

    # Draw ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
