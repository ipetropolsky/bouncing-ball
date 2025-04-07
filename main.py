import pygame
import math
import random
from pygame import gfxdraw

def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, int(x), int(y), radius, color)
    gfxdraw.filled_circle(surface, int(x), int(y), radius, color)

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Circle with Trail")

# Clock
clock = pygame.time.Clock()

# https://coolors.co/381d2a-3b435d-3e6990-74938e-aabd8c-e9e3b4-eebf91-f39b6d
COLORS = ['#3A3044', '#3b435d', '#3B3A51', '#3E6990', '#3D5677', '#74938E', '#8FA88D', '#AABD8C', '#CAD0A0', '#E9E3B4', '#ECD1A3', '#EEBF91', '#F1AD7F', '#F39B6D']

NUM_CIRCLES = 10
VEL_BOOST = 5
boost_on_next_collision = None

# Circle settings
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 350
CIRCLE_WIDTH = 8
HALF_CIRCLE_WIDTH = CIRCLE_WIDTH / 2 - 2

# Ball settings
ball_pos = [CENTER[0], CENTER[1] - 50]
ball_vel = [5, 0]  # initial velocity
ball_radius = 10
gravity = 0.3

# Trail
trail = []
max_trail_length = 200

debug = False
debug_collision = False

def log(*args):
    if (debug):
        print(*args)

def log_collision(*args):
    if (debug_collision):
        print(*args)

def normalize_angle(angle):
    if angle > 360:
        return angle - 360
    if angle < 0:
        return angle + 360
    return angle

# Spinning Circles with gaps
class SpinningCircle:
    def __init__(self, index, radius):
        self.index = index
        self.radius = radius
        self.gap_length = random.uniform(30, 50)
        self.start_angle = random.uniform(0, 360)
        self.end_angle = self.start_angle - self.gap_length
        self.speed = random.uniform(0.3, 1)
        self.direction = random.choice([-1, 1])
        self.active = True

    def update(self):
        self.start_angle = normalize_angle((self.start_angle + self.speed * self.direction) % 360)
        self.end_angle = normalize_angle(self.start_angle - self.gap_length)

    def draw(self, surface, color):
        log(self.index, self.start_angle, self.end_angle)
        pygame.draw.arc(
            surface,
            color,
            (CENTER[0] - self.radius, CENTER[1] - self.radius, self.radius * 2, self.radius * 2),
            math.radians(self.start_angle),
            math.radians(self.end_angle),
            CIRCLE_WIDTH
        )

    def is_inside_gap(self, pos):
        if not self.active:
            return False
        dx, dy = pos[0] - CENTER[0], pos[1] - CENTER[1]
        angle = normalize_angle(360 - math.degrees(math.atan2(dy, dx)))
        log_collision('is_inside_gap', self.index, angle)
        gap_start = self.end_angle
        gap_end = self.start_angle
        log_collision(self.index, angle, gap_start, gap_end)
        if gap_start < gap_end:
            log_collision(f'is_inside_gap (1) {gap_start} < {angle} < {gap_end}: {gap_start < angle < gap_end}')
            return gap_start < angle < gap_end
        else:
            log_collision(f'is_inside_gap (2) {angle} > {gap_start} or {angle} < {gap_end}: {angle > gap_start or angle < gap_end}')
            return angle > gap_start or angle < gap_end

    def reflect(self, pos, vel):
        if not self.active:
            return
        dx, dy = pos[0] - CENTER[0], pos[1] - CENTER[1]
        dist = math.hypot(dx, dy)
        if abs(dist - self.radius + HALF_CIRCLE_WIDTH) <= ball_radius:
            if self.is_inside_gap(pos):
                log('reflect', self.index, 'exploded')
                ball_vel[1] += 1
                self.explode(60)
                self.active = False
                return
            self.explode()
            nx = dx / dist
            ny = dy / dist
            dot = vel[0] * nx + vel[1] * ny
            vel[0] -= 2 * dot * nx
            vel[1] -= 2 * dot * ny
            pos[0] = CENTER[0] + (self.radius - ball_radius - HALF_CIRCLE_WIDTH - 1) * nx
            pos[1] = CENTER[1] + (self.radius - ball_radius - HALF_CIRCLE_WIDTH - 1) * ny
            global boost_on_next_collision
            if boost_on_next_collision:
                if vel[1] > 0:
                    vel[1] += boost_on_next_collision
                else:
                    vel[1] -= boost_on_next_collision
                boost_on_next_collision = None

    def explode(self, num = 30):
        for _ in range(num):
            particles.append([ball_pos[:], [random.uniform(-5, 5), random.uniform(-5, 5)], random.choice([(255, 0, 0), (255, 255, 0), (255, 150, 0)]), 30])

# Explosion particles
particles = []

# Create spinning circles
spinning_circles = [SpinningCircle(i, RADIUS - 25 * i) for i in range(1, NUM_CIRCLES + 1)]

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
        global boost_on_next_collision
        if boost_on_next_collision:
            if vel[1] > 0:
                vel[1] += boost_on_next_collision
            else:
                vel[1] -= boost_on_next_collision
            boost_on_next_collision = None

running = True
paused = False
while running:
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, pygame.Color(COLORS[0]), CENTER, RADIUS, CIRCLE_WIDTH)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            paused = not paused
            log('MOUSEBUTTONDOWN', paused)
        if event.type == pygame.KEYDOWN:
            log('KEYDOWN', event.key)
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_UP:
                boost_on_next_collision = VEL_BOOST
            if event.key == pygame.K_DOWN:
                boost_on_next_collision = -VEL_BOOST

        if event.type == pygame.QUIT:
            running = False

    if paused:
        continue

    # Physics
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    reflect_main_circle(ball_pos, ball_vel)
    for circle in spinning_circles:
        circle.reflect(ball_pos, ball_vel)

    # Update and draw spinning circles
    for i, circle in enumerate(spinning_circles):
        if circle.active:
            circle.update()
            circle.draw(screen, pygame.Color(COLORS[i + 1]))
        elif debug:
            circle.draw(screen, '#333333')

    # Add to trail
    trail.append((ball_pos[0], ball_pos[1], pygame.time.get_ticks()))
    if len(trail) > max_trail_length:
        trail.pop(0)

    # Draw trail with rainbow colors
    for i, (x, y, t) in enumerate(trail):
        hue = (t * 0.1) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, i / len(trail) * 100, 100)
        draw_circle(screen, x, y, 4, color)

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
