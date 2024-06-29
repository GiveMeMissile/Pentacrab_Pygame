import pygame
import os

pygame.init()

# Window control
WIDTH = 1200
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Background.png")), (WIDTH, HEIGHT))
FPS = 60

# Player settings
JUMP_HEIGHT = 70
JUMP_SLOW = 30
GRAVITY = 7
HITBOX_WIDTH, HITBOX_HEIGHT = 20, 70
velocity = 0
ACCELERATION = 0.5
MAX_VELOCITY = 5
FRICTION = 0.1
X = WIDTH // 2
Y = HEIGHT - HITBOX_HEIGHT
HITBOX = pygame.Rect(X, Y, HITBOX_WIDTH, HITBOX_HEIGHT)
JUMP_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Player_jump.mp3")

# Platform settings
PLATFORM_HEIGHT = 60
PLATFORM_WIDTH = 200
PLATFORM_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Cloud_platfrom.png")), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
PLATFORM = pygame.transform.rotate(pygame.transform.scale(PLATFORM_IMAGE, (PLATFORM_WIDTH, PLATFORM_HEIGHT)), 180)

platforms = []

def draw():
    platform_location_x = 100
    platform_location_y = 550
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, (255, 0, 0), HITBOX)
    for _ in range(5):
        WINDOW.blit(PLATFORM, (platform_location_x, platform_location_y))
        platforms.append([platform_location_x, platform_location_y])
        platform_location_x += PLATFORM_WIDTH + 50
        platform_location_y -= PLATFORM_HEIGHT
    pygame.display.update()

def player_movements():
    global velocity, X
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        velocity += ACCELERATION
    elif keys[pygame.K_a]:
        velocity -= ACCELERATION
    else:
        if velocity > 0:
            velocity -= FRICTION
            if velocity < 0:
                velocity = 0
        elif velocity < 0:
            velocity += FRICTION
            if velocity > 0:
                velocity = 0

    if velocity > MAX_VELOCITY:
        velocity = MAX_VELOCITY
    elif velocity < -MAX_VELOCITY:
        velocity = -MAX_VELOCITY

    X += velocity
    if X < 0:
        X = 0
        velocity = 0
    elif X + HITBOX_WIDTH > WIDTH:
        X = WIDTH - HITBOX_WIDTH
        velocity = 0

    HITBOX.x = X

def player_jump():
    global decent, Jump, initial_height, falling
    if decent == False:
        if HITBOX.y > initial_height - (JUMP_HEIGHT + HITBOX_HEIGHT + JUMP_SLOW):
            HITBOX.y -= 3
            if initial_height - (JUMP_HEIGHT + HITBOX_HEIGHT) < HITBOX.y:
                HITBOX.y -= 4
        else:
            decent = True
    if decent:
        HITBOX.y += GRAVITY
        for platform_location_x, platform_location_y in platforms:
            platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
                HITBOX.y = platform_rect.y - HITBOX_HEIGHT
                decent = False
                Jump = False
                falling = False
                initial_height = HITBOX.y
                return
        if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
            HITBOX.y = HEIGHT - HITBOX_HEIGHT
            decent = False
            Jump = False
            initial_height = HEIGHT - HITBOX_HEIGHT

def gravity():
    global initial_height, falling, Jump
    if Jump == False:
        for platform_location_x, platform_location_y in platforms:
            platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
                HITBOX.y = platform_rect.y + 5 - HITBOX_HEIGHT
                initial_height = HITBOX.y
                falling = False
                return
        if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
            HITBOX.y = HEIGHT - HITBOX_HEIGHT
            initial_height = HEIGHT - HITBOX_HEIGHT
            falling = False
            return
        if falling == True:
            HITBOX.y += GRAVITY


def main():
    global run, Jump, decent, falling, platforms, initial_height
    falling = True
    Jump = False
    decent = False
    platforms = []
    initial_height = HEIGHT - HITBOX_HEIGHT
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not Jump and not falling:
                    Jump = True
                    JUMP_SOUND.play()
            if event.type == pygame.QUIT:
                run = False
        falling = True
        if not Jump:
            gravity()
        else:
            player_jump()
        player_movements()
        draw()
    pygame.quit()

main()
