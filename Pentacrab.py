import pygame
import os
import random

pygame.init()

# Window control
WIDTH = 1350
HEIGHT = 650
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Background.png")),
                                    (WIDTH, HEIGHT))
FPS = 60

# Player settings
JUMP_HEIGHT = 70
JUMP_SLOW = 30
GRAVITY = 7
HITBOX_WIDTH, HITBOX_HEIGHT = 20, 70
velocity = 0
ACCELERATION = 1
MAX_VELOCITY = 6
FRICTION = 0.1
PLAYER_DIFFERENCE = 15

TELEPORT_DAMAGE = 5
TELEPORT_AMOUNT = 500
TP_DELAY = 500
TP_COOLDOWN = 5500
TELEPORT_WIDTH, TELEPORT_HEIGHT = HITBOX_HEIGHT + PLAYER_DIFFERENCE, HITBOX_HEIGHT + PLAYER_DIFFERENCE

TELEPORT_SYMBOL = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Teleport.png")),
                                         (TELEPORT_WIDTH, TELEPORT_HEIGHT))
TELEPORT_COOLDOWN = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Tp_cooldown.png")), (TELEPORT_WIDTH, TELEPORT_HEIGHT))

AURA_DAMAGE = 15
AURA_WIDTH = 400
AURA_COOLDOWN = 10000
AURA_PULSE_ON = 150
AURA_PULSE_OFF = 200
aura = []

AURA_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Lightning_aura.png")), (AURA_WIDTH, HITBOX_HEIGHT + 80))
AURA_COOLDOWN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Electic_pulse_cooldown.png")), (HITBOX_WIDTH, HITBOX_HEIGHT))

X = WIDTH // 2
Y = HEIGHT - HITBOX_HEIGHT
HITBOX = pygame.Rect(X, Y, HITBOX_WIDTH, HITBOX_HEIGHT)

PLAYER_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Player.png")),
                                      (HITBOX_WIDTH + 30, HITBOX_HEIGHT + 20))
PLAYER_LEFT = pygame.transform.flip(PLAYER_RIGHT, flip_y=False, flip_x=True)
PLAYER_JUMP_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Player_jump.png")),
                                           (HITBOX_WIDTH + 30, HITBOX_HEIGHT + 20))
PLAYER_JUMP_LEFT = pygame.transform.flip(PLAYER_JUMP_RIGHT, flip_y=False, flip_x=True)

# Sounds
JUMP_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Player_jump.mp3")
TELEPORT_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Teleport.mp3")
DAMAGE_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Damage1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Bullet_fire.mp3")
ELECTRIC_AURA_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Electric_aura.wav")

# Platform settings
PLATFORM_HEIGHT = 60
PLATFORM_WIDTH = 200
platforms = []
PLATFORM_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Cloud_platfrom.png")),
                                        (PLATFORM_WIDTH, PLATFORM_HEIGHT))
PLATFORM = pygame.transform.rotate(pygame.transform.scale(PLATFORM_IMAGE, (PLATFORM_WIDTH, PLATFORM_HEIGHT)), 180)

# Boss settings
BOSS_WIDTH, BOSS_HEIGHT = 100, 100
BOSS_Y = 100
BOSS_HITBOX = pygame.Rect(X - 50, BOSS_Y, BOSS_WIDTH, BOSS_HEIGHT)
BOSS_MOVEMENT = 5

BOSS_CONTACT_DAMAGE = 3
BOSS_ATTACK_DELAY = 5000

BOSS_BULLET_DELAY = 250
boss_bullets = []
boss_bullet_warning = []
BULLET_DAMAGE = 1
BULLET_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Bullet.png")), (20, 20))
BULLET_WARNING_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Bullet_warning.png")), (30, 30))
BULLET_REDO = 1000

BOSS_LASER_DAMAGE = 2
boss_laser = []
BOSS_LASER_ATTACK = 3000
BOSS_LASER_COOLDOWN = 1500

BOSS_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Pentacrab.png")), (BOSS_WIDTH + 40, BOSS_HEIGHT + 50))

#other
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
IMMUNITY = 500

def location_reset():
    HITBOX.x = WIDTH/2 + HITBOX_WIDTH/2
    HITBOX.y = HEIGHT - HITBOX_HEIGHT
    BOSS_HITBOX.x = WIDTH/2 - BOSS_WIDTH/2
    BOSS_HITBOX.y = BOSS_Y
def draw():
    WINDOW.blit(BACKGROUND, (0, 0))
    boss_health_text = HEALTH_FONT.render("Boss Health: " + str(boss_health), 1, (255, 255, 255 ))
    player_health_text = HEALTH_FONT.render("Player Health: " + str(player_health), 1, (255, 255, 255))
    WINDOW.blit(boss_health_text, (0, 0))
    WINDOW.blit(player_health_text, (WIDTH - 350, 0))
    for platform_location_x, platform_location_y in platforms:
        WINDOW.blit(PLATFORM, (platform_location_x, platform_location_y))
    
    if tp_cooldown:
        WINDOW.blit(TELEPORT_COOLDOWN, (HITBOX.x + PLAYER_DIFFERENCE - TELEPORT_WIDTH / 2,HITBOX.y - PLAYER_DIFFERENCE))
    for portal_hitbox in tp_hitbox:
        WINDOW.blit(TELEPORT_SYMBOL, (portal_hitbox.x, portal_hitbox.y))
    
    WINDOW.blit(BOSS_IMAGE, (BOSS_HITBOX.x - 20, BOSS_HITBOX.y))
    
    for bullet_warning in boss_bullet_warning:
        WINDOW.blit(BULLET_WARNING_IMAGE, (bullet_warning.x, bullet_warning.y))
    for bullet in boss_bullets:
        WINDOW.blit(BULLET_IMAGE, (bullet.x, bullet.y))

    for aura_hitbox in aura:
        WINDOW.blit(AURA_IMAGE, (aura_hitbox.x, aura_hitbox.y))
    if not Jump:
        if left:
            WINDOW.blit(PLAYER_LEFT, (HITBOX.x - 15, HITBOX.y - 15))
        else:
            WINDOW.blit(PLAYER_RIGHT, (HITBOX.x - 15, HITBOX.y - 15))
    if Jump:
        if left:
            WINDOW.blit(PLAYER_JUMP_LEFT, (HITBOX.x - PLAYER_DIFFERENCE, HITBOX.y - PLAYER_DIFFERENCE))
        else:
            WINDOW.blit(PLAYER_JUMP_RIGHT, (HITBOX.x - PLAYER_DIFFERENCE, HITBOX.y - PLAYER_DIFFERENCE))
    if aura_cooldown:
        WINDOW.blit(AURA_COOLDOWN_IMAGE, (HITBOX.x, HITBOX.y))
    pygame.display.update()


def setup_platforms():
    platform_location_x = 100
    platform_location_y = 280
    for _ in range(5):
        platforms.append([platform_location_x, platform_location_y])
        platform_location_x += PLATFORM_WIDTH + 50
        if len(platforms) <= 2:
            platform_location_y += PLATFORM_HEIGHT + 50
        else:
            platform_location_y -= PLATFORM_HEIGHT + 50


def player_movements():
    global velocity, left
    if player_health >= 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            velocity += ACCELERATION
            left = False
        elif keys[pygame.K_a]:
            left = True
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

    HITBOX.x += velocity
    if HITBOX.x < 0:
        HITBOX.x = 0
        velocity = 0
    elif HITBOX.x + HITBOX_WIDTH > WIDTH:
        HITBOX.x = WIDTH - HITBOX_WIDTH
        velocity = 0


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
                HITBOX.y = platform_rect.y + GRAVITY - HITBOX_HEIGHT
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


def teleport_movement():
    global tele_up, tele_left, tele_right, tp_cooldown, tp_delay

    if tele_up and (current_time - tp_delay >= TP_DELAY):
        if HITBOX.y + TELEPORT_AMOUNT <= BOSS_Y:
            HITBOX.y -= TELEPORT_AMOUNT
        else:
            HITBOX.y = BOSS_Y
        tele_up = False

    if tele_left and (current_time - tp_delay >= TP_DELAY):
        if HITBOX.x - TELEPORT_AMOUNT >= 0:
            HITBOX.x -= TELEPORT_AMOUNT
        else:
            HITBOX.x = 0
        tele_left = False

    if tele_right and (current_time - tp_delay >= TP_DELAY):
        if HITBOX.x + TELEPORT_AMOUNT <= WIDTH:
            HITBOX.x += TELEPORT_AMOUNT
        else:
            HITBOX.x = WIDTH
        tele_right = False

    if tp_cooldown and (current_time - tp_delay >= TP_COOLDOWN):
        tp_cooldown = False


def teleport_visual():
    global tp_hitbox, tp
    dif = 0
    if tp:
        tp_hitbox.clear()
    if tele_up or tele_left or tele_right:
        tp = True
        for _ in range(2):
            dif += 1
            if dif == 1:
                portal_hitbox = pygame.Rect(HITBOX.x + PLAYER_DIFFERENCE - TELEPORT_WIDTH / 2,
                                            HITBOX.y - PLAYER_DIFFERENCE, TELEPORT_WIDTH, TELEPORT_HEIGHT)
            elif dif == 2:
                if tele_up:
                    portal_hitbox = pygame.Rect(HITBOX.x + PLAYER_DIFFERENCE - TELEPORT_WIDTH / 2,
                                                HITBOX.y - PLAYER_DIFFERENCE - TELEPORT_AMOUNT, TELEPORT_WIDTH,
                                                TELEPORT_HEIGHT)
                elif tele_left:
                    portal_hitbox = pygame.Rect(HITBOX.x + PLAYER_DIFFERENCE - TELEPORT_AMOUNT - TELEPORT_WIDTH / 2,
                                                HITBOX.y + PLAYER_DIFFERENCE, TELEPORT_WIDTH, TELEPORT_HEIGHT)
                elif tele_right:
                    portal_hitbox = pygame.Rect(HITBOX.x + PLAYER_DIFFERENCE + TELEPORT_AMOUNT - TELEPORT_WIDTH / 2,
                                                HITBOX.y - PLAYER_DIFFERENCE, TELEPORT_WIDTH, TELEPORT_HEIGHT)
            tp_hitbox.append(portal_hitbox)
    else:
        tp_hitbox.clear()
        tp = False

def boss_movement():
    global boss_right, boss_health, victory
    if BOSS_HITBOX.x >= WIDTH - BOSS_WIDTH:
        boss_right = False
    if BOSS_HITBOX.x <= 0:
        boss_right = True
    if boss_right and not victory:
        BOSS_HITBOX.x += BOSS_MOVEMENT
    elif not victory:
        BOSS_HITBOX.x -= BOSS_MOVEMENT

def boss_bullet_movement():
    for bullet in boss_bullets:
        bullet.y += 7
        if bullet.y >= HEIGHT:
            boss_bullets.remove(bullet)
        if bullet.y == HEIGHT:
            boss_bullets.remove(bullet)

def player_attack_handler():
    global aura_attack, aura_create, aura_cooldown, aura_cooldown_timer, aura_pulse_on,\
        aura_pulse_off, aura_off
    for aura_hitbox in aura:
        aura_hitbox.x = (HITBOX.x - AURA_WIDTH/2 - 1)
        aura_hitbox.y = HITBOX.y - 80
    if aura_cooldown and current_time - aura_cooldown_timer >= AURA_COOLDOWN:
        aura_cooldown = False
    if aura_attack:
        if not aura_create:
            aura_hitbox = pygame.Rect(HITBOX.x - AURA_WIDTH/2 - 10, HITBOX.y - 80, AURA_WIDTH, HITBOX_HEIGHT + 80)
            aura_create = True
            aura.append(aura_hitbox)
            aura_cooldown = True
            aura_cooldown_timer = current_time
            aura_pulse_on = current_time
            aura_pulse_off = current_time
            aura_off += 1
        if current_time - aura_pulse_on >= AURA_PULSE_ON:
            aura.clear()
            if aura_off > + 3:
                aura_attack = False
                aura_off = 1
        if current_time - aura_pulse_off >= AURA_PULSE_OFF:
            aura_create = False



def boss_attack_handler():
    global  boss_attack, boss_attack_timer, initialized_attack, attack_end, attack_number,\
        bullet_fired, bullet_delay_timer, bullet_total, attack_redo, bullet_redo_delay,\
        bullet_redo_timelaser_delay, laser_fire_time, laser_cooldown, laser_active, laser_start
    if boss_attack:
        if not initialized_attack and not attack_end:
            initialized_attack = True
            attack_number = random.randint(1, 2)
        if attack_number == 1 and initialized_attack:
            boss_bullet_warning.clear()
            bullet_warning = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 15, BOSS_HITBOX.y + BOSS_HEIGHT + 20, 30, 30)
            boss_bullet_warning.append(bullet_warning)
            if not bullet_fired and not bullet_redo_delay:
                bullet_fired = True
                bullet = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 10, BOSS_HITBOX.y + BOSS_HEIGHT + 20, 20, 20)
                boss_bullets.append(bullet)
                bullet_delay_timer = current_time
                bullet_total += 1
                BULLET_FIRE_SOUND.play()
            else:
                if current_time - bullet_delay_timer >= BULLET_REDO:
                    bullet_redo_delay = False
                if attack_redo >= 2 and bullet_total >= 10:
                    attack_number = 6
                    attack_end = True
                    attack_redo = 0
                    bullet_total = 0
                if bullet_total >= 10:
                    bullet_total = 0
                    attack_redo += 1
                    bullet_redo_delay = True
                    bullet_redo_timer = current_time
                if current_time - bullet_delay_timer >= BOSS_BULLET_DELAY:
                    bullet_fired = False
        if attack_number == 2 and initialized_attack:
            if not laser_active:
                boss_laser.clear()
                laser_start = False
                laser_active = True
                laser_cooldown = current_time
                laser_warning = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 15, BOSS_HITBOX.y + BOSS_HEIGHT + 20, 30, 30)
                boss_laser.append(laser_warning)
            if laser_active and current_time - laser_cooldown >= BOSS_LASER_COOLDOWN and not laser_start:
                laser_start = True
                laser = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 30, BOSS_HITBOX.y + BOSS_HEIGHT + 20, 60, HEIGHT)
                boss_laser.append(laser)
                laser_fire_time = current_time
                
        if initialized_attack and attack_end:
            boss_attack_timer = current_time
            boss_attack = False
            initialized_attack = False
            attack_end = False
            boss_bullet_warning.clear()
    if current_time - boss_attack_timer >= BOSS_ATTACK_DELAY and not boss_attack:
        boss_attack = True

def boss_health_manager():
    global boss_health, victory, boss_immunity, boss_immunity_timer
    if not boss_immunity:
        boss_immunity = True
        boss_immunity_timer = current_time
        for portal_hitbox in tp_hitbox:
            if BOSS_HITBOX.colliderect(portal_hitbox):
                boss_health -= TELEPORT_DAMAGE
        for aura_hitbox in aura:
            if BOSS_HITBOX.colliderect(aura_hitbox):
                boss_health -= AURA_DAMAGE
    if current_time - boss_immunity_timer >= IMMUNITY:
        boss_immunity = False
    if boss_health <= 0:
        BOSS_HITBOX.y -= 500
        victory = True

def player_health_manager():
    global player_health, player_immunity, player_immunity_timer
    if not player_immunity:
        if HITBOX.colliderect(BOSS_HITBOX):
            player_health -= BOSS_CONTACT_DAMAGE
            player_immunity = True
            player_immunity_timer = current_time
            DAMAGE_SOUND.play()
        for bullet in boss_bullets:
            if bullet.colliderect(HITBOX):
                player_health -= BULLET_DAMAGE
                DAMAGE_SOUND.play()
                boss_bullets.remove(bullet)
    if current_time - player_immunity_timer >= IMMUNITY and player_immunity:
        player_immunity = False

def main():
    global run, Jump, decent, falling, initial_height, tele_up, current_time, tp_delay, \
        tele_left, tp_cooldown, tele_right, left, tp_hitbox, tp, boss_right, boss_health, \
        player_health, victory, player_immunity, player_immunity_timer, boss_immunity_timer,\
        boss_immunity, boss_attack, boss_attack_timer, initialized_attack, attack_end,\
        attack_number, bullet_fired, bullet_delay_timer, bullet_total, attack_redo, bullet_redo_delay, \
        bullet_redo_timer, aura_cooldown, aura_attack, aura_cooldown_timer, aura_create, \
        aura_pulse_on, aura_pulse_off, aura_off, laser_delay, laser_fire_time, laser_cooldown,\
        laser_active, laser_start
    location_reset()
    laser_start = False
    laser_active = False
    laser_fire_time = 99999999
    laser_cooldown = 99999999
    aura_off = 1
    aura_pulse_on = 99999999
    aura_pulse_off = 99999999
    aura_create = False
    aura_cooldown_timer = 99999999
    aura_cooldown = False
    aura_attack = False
    bullet_redo_delay = False
    bullet_redo_timer = 99999999
    attack_redo = 0
    bullet_total = 0
    bullet_fired = False
    attack_number = 6
    attack_end = False
    initialized_attack = False
    boss_attack_timer = 0
    bullet_delay_timer = 99999999
    boss_attack = False
    boss_immunity_timer = 99999999
    boss_immunity = False
    player_immunity_timer = 99999999
    player_immunity = False
    victory = False
    boss_right = True
    boss_health = 100
    player_health = 30
    tp_hitbox = []
    tp = False
    tp_delay = 99999999
    left = False
    tp_cooldown = False
    tele_up = False
    tele_left = False
    tele_right = False
    falling = True
    Jump = False
    decent = False
    platforms.clear()
    initial_height = HEIGHT - HITBOX_HEIGHT
    setup_platforms()
    run = True
    clock = pygame.time.Clock()
    while run:
        current_time = pygame.time.get_ticks()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not Jump and not falling:
                    Jump = True
                    JUMP_SOUND.play()
                if event.key == pygame.K_UP and not tp_cooldown:
                    tele_up = True
                    tp_delay = current_time
                    tp_cooldown = True
                    TELEPORT_SOUND.play()
                if event.key == pygame.K_LEFT and not tp_cooldown:
                    tele_left = True
                    tp_delay = current_time
                    tp_cooldown = True
                    TELEPORT_SOUND.play()
                if event.key == pygame.K_RIGHT and not tp_cooldown:
                    tele_right = True
                    tp_delay = current_time
                    tp_cooldown = True
                    TELEPORT_SOUND.play()
                if event.key == pygame.K_e and not aura_cooldown:
                    aura_attack = True
                    aura_cooldown = True
                    aura_cooldown_timer = current_time
                    ELECTRIC_AURA_SOUND.play()
            if event.type == pygame.QUIT:
                run = False
        falling = True
        if not Jump:
            gravity()
        else:
            player_jump()
        teleport_visual()
        teleport_movement()
        player_movements()
        boss_attack_handler()
        boss_bullet_movement()
        player_attack_handler()
        boss_health_manager()
        player_health_manager()
        boss_movement()
        if player_health <= 0:
            main()
        draw()
    pygame.quit()

main()
