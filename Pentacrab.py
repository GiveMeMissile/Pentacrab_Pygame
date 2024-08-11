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
PLAYER_HEALTH = 30
GRAVITY = 7
HITBOX_WIDTH, HITBOX_HEIGHT = 20, 70
velocity = 0
ACCELERATION = 1
MAX_VELOCITY = 6
FRICTION = 0.1
PLAYER_DIFFERENCE = 15
PLAYER_HEALTH_X, PLAYER_HEALTH_Y = 450, 80
player_health_points = []

TELEPORT_DAMAGE = 5
TELEPORT_AMOUNT = 500
TP_DELAY = 500
TP_COOLDOWN = 5500
TELEPORT_WIDTH, TELEPORT_HEIGHT = HITBOX_HEIGHT + PLAYER_DIFFERENCE, HITBOX_HEIGHT + PLAYER_DIFFERENCE

TELEPORT_SYMBOL = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Teleport.png")),
                                         (TELEPORT_WIDTH, TELEPORT_HEIGHT))
TELEPORT_COOLDOWN = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Tp_cooldown.png")), (TELEPORT_WIDTH, TELEPORT_HEIGHT))

LIGHTNING_BOLT_DAMAGE = 1
LIGHTNING_MOVEMENT_SPEED = 12
LIGHTNING_WIDTH, LIGHTNING_HEIGHT = 15, 60
LIGHTNING_DELAY = 400
LIGHTNING_MAX = 10
LIGHTNING_REFRESH = 3000
lightning_bolt_up = []
lightning_bolt_down = []
lightning_bolt_left = []
lightning_bolt_right = []

LIGHTNING_BOLT_IMAGE_UP = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Lightning_blast.png")), (LIGHTNING_WIDTH, LIGHTNING_HEIGHT))
LIGHTNING_BOLT_IMAGE_DOWN = pygame.transform.flip(LIGHTNING_BOLT_IMAGE_UP, flip_y=True, flip_x=False)
LIGHTNING_BOLT_IMAGE_RIGHT = pygame.transform.rotate(LIGHTNING_BOLT_IMAGE_UP, 90)
LIGHTNING_BOLT_IMAGE_LEFT = pygame.transform.flip(LIGHTNING_BOLT_IMAGE_RIGHT, flip_y=False, flip_x=True)

INDICATOR_IMAGE_UP = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Directional_indicator.png")), (20, 40))
INDICATOR_IMAGE_DOWN = pygame.transform.flip(INDICATOR_IMAGE_UP, flip_y=True, flip_x=False)
INDICATOR_IMAGE_LEFT = pygame.transform.rotate(INDICATOR_IMAGE_UP, 90)
INDICATOR_IMAGE_RIGHT = pygame.transform.flip(INDICATOR_IMAGE_LEFT, flip_y=False, flip_x=True)

AURA_DAMAGE = 10
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
LASER_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Boss_laser_sound.wav")
LIGHTNING_BOLT_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Lightning_bolt_sound.wav")
SPAGHETTI_EAT_SOUND = pygame.mixer.Sound("Pentacrab_Assets/Heal_sound_effect.mp3")

#Health Spaghetti
HEALTH_SPAGHETTI_WIDTH, HEALTH_SPAGHETTI_HEIGHT = 80, 60
HEALTH_GAIN = 3
HEALTH_SPAGHETTI_COOLDOWN = 30000
HEALTH_SPAGHETTI_MAX = 3
Health_spaghetti = []

HEALTH_SPAGHETTI_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Health_spaghetti.png")), (HEALTH_SPAGHETTI_WIDTH, HEALTH_SPAGHETTI_HEIGHT))

# Platform settings
PLATFORM_HEIGHT = 60
PLATFORM_WIDTH = 200
platforms = []
PLATFORM_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Cloud_platfrom.png")),
                                        (PLATFORM_WIDTH, PLATFORM_HEIGHT))
PLATFORM = pygame.transform.rotate(pygame.transform.scale(PLATFORM_IMAGE, (PLATFORM_WIDTH, PLATFORM_HEIGHT)), 180)

# Boss settings
BOSS_WIDTH, BOSS_HEIGHT = 100, 120
BOSS_Y = 100
BOSS_HITBOX = pygame.Rect(X - 50, BOSS_Y, BOSS_WIDTH, BOSS_HEIGHT)
BOSS_MOVEMENT = 5
BOSS_HEALTH = 300
BOSS_HEALTH_X, BOSS_HEALTH_Y = WIDTH/4, 40
boss_health_points = []

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
boss_laser_hitbox = []
boss_laser_warning = []
BOSS_LASER_ATTACK = 4500
BOSS_LASER_COOLDOWN = 1500

LASER_WARNING_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Energy_laser_warning.png")), (30, 30))
LASER_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Boss_energy_laser.png")), (180, HEIGHT))

BOSS_DIVE_SPEED = 10
BOSS_DIVE_COOLDOWN = 1000

BOSS_DIVE_WARNING = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Boss_dive_attack_warning.png")), (BOSS_WIDTH, BOSS_HEIGHT))

BOSS_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Pentacrab.png")), (BOSS_WIDTH + 40, BOSS_HEIGHT + 30))

#Boss Minions
MINION_HEIGHT, MINION_WIDTH = 50, 60
MINION_DAMAGE = 2
MINION_RESPAWN_COOLDOWN = 5000

MINION_ONE_HITBOX = pygame.Rect(0, HEIGHT - MINION_HEIGHT, MINION_WIDTH, MINION_HEIGHT)
MINION_TWO_HITBOX = pygame.Rect(WIDTH - MINION_WIDTH, HEIGHT - MINION_HEIGHT, MINION_WIDTH, MINION_HEIGHT)

MINION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Pentacrab.png")), (MINION_WIDTH, MINION_HEIGHT))
RIGHT_MINION_IMAGE = pygame.transform.rotate(MINION_IMAGE, 90)
LEFT_MINION_IMAGE = pygame.transform.rotate(MINION_IMAGE, 270)
SUMMON_MINION_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Pentacrab_Assets", "Summoning_portal.png")), (MINION_HEIGHT, MINION_HEIGHT))

#other
HEALTH_FONT = pygame.font.SysFont("Times New Roman", 40)
IMMUNITY = 500
HEALTH_POINT_WIDTH, HEALTH_POINT_HEIGHT = (WIDTH/2)/BOSS_HEALTH, 10
HEALTH_POINT_ADDITION = (WIDTH/3)/PLAYER_HEALTH
RED = (255, 100, 100)
BLUE = (0, 0, 255)

def reset():
    global attack_end, attack_redo
    HITBOX.x = WIDTH/2 + HITBOX_WIDTH/2
    HITBOX.y = HEIGHT - HITBOX_HEIGHT
    BOSS_HITBOX.x = WIDTH/2 - BOSS_WIDTH/2
    BOSS_HITBOX.y = BOSS_Y
    boss_laser_warning.clear()
    boss_laser_hitbox.clear()
    boss_bullets.clear()
    boss_bullet_warning.clear()
    aura.clear()
    boss_health_x = BOSS_HEALTH_X
    for _ in range(boss_health):
        boss_health_point = pygame.Rect(boss_health_x, BOSS_HEALTH_Y, HEALTH_POINT_WIDTH, HEALTH_POINT_HEIGHT)
        boss_health_x += HEALTH_POINT_WIDTH
        boss_health_points.append(boss_health_point)
    player_health_x = PLAYER_HEALTH_X
    for _ in range(player_health):
        player_health_point = pygame.Rect(player_health_x, PLAYER_HEALTH_Y, HEALTH_POINT_ADDITION, HEALTH_POINT_HEIGHT)
        player_health_x += HEALTH_POINT_ADDITION
        player_health_points.append(player_health_point)

def draw():
    WINDOW.blit(BACKGROUND, (0, 0))
    boss_health_text = HEALTH_FONT.render("Boss Health: " + str(boss_health), 1, (255, 255, 255 ))
    player_health_text = HEALTH_FONT.render("Player Health: " + str(player_health), 1, (255, 255, 255))
    WINDOW.blit(boss_health_text, (WIDTH/2 - 110, 0))
    WINDOW.blit(player_health_text, (WIDTH/2 - 110, 42))

    for boss_health_point in boss_health_points:
        pygame.draw.rect(WINDOW, RED, boss_health_point)
    for player_health_point in player_health_points:
        pygame.draw.rect(WINDOW, BLUE, player_health_point)

    for platform_location_x, platform_location_y in platforms:
        WINDOW.blit(PLATFORM, (platform_location_x, platform_location_y))

    if lightning_up:
        WINDOW.blit(INDICATOR_IMAGE_UP, (HITBOX.x, HITBOX.y - 70))
    elif lightning_down:
        WINDOW.blit(INDICATOR_IMAGE_DOWN, (HITBOX.x, HITBOX.y + HITBOX_HEIGHT))
    elif lightning_right:
        WINDOW.blit(INDICATOR_IMAGE_RIGHT, (HITBOX.x + 40, HITBOX.y + 20))
    elif lightning_left:
        WINDOW.blit(INDICATOR_IMAGE_LEFT, (HITBOX.x - 50, HITBOX.y + 20))

    for lightning_hitbox_up in lightning_bolt_up:
        WINDOW.blit(LIGHTNING_BOLT_IMAGE_UP, (lightning_hitbox_up.x, lightning_hitbox_up.y))
    for lightning_hitbox_left in lightning_bolt_left:
        WINDOW.blit(LIGHTNING_BOLT_IMAGE_LEFT, (lightning_hitbox_left.x, lightning_hitbox_left.y))
    for lightning_hitbox_right in lightning_bolt_right:
        WINDOW.blit(LIGHTNING_BOLT_IMAGE_RIGHT, (lightning_hitbox_right.x, lightning_hitbox_right.y))
    for lightning_hitbox_down in lightning_bolt_down:
        WINDOW.blit(LIGHTNING_BOLT_IMAGE_DOWN, (lightning_hitbox_down.x, lightning_hitbox_down.y))

    for spaghetti_hitbox in Health_spaghetti:
        WINDOW.blit(HEALTH_SPAGHETTI_IMAGE, (spaghetti_hitbox.x, spaghetti_hitbox.y))

    if tp_cooldown:
        WINDOW.blit(TELEPORT_COOLDOWN, (HITBOX.x + PLAYER_DIFFERENCE - TELEPORT_WIDTH / 2,HITBOX.y - PLAYER_DIFFERENCE))
    for portal_hitbox in tp_hitbox:
        WINDOW.blit(TELEPORT_SYMBOL, (portal_hitbox.x, portal_hitbox.y))
    
    WINDOW.blit(BOSS_IMAGE, (BOSS_HITBOX.x - 20, BOSS_HITBOX.y))
    if boss_dive_attack:
        WINDOW.blit(BOSS_DIVE_WARNING, (BOSS_HITBOX.x, BOSS_HITBOX.y))
    
    for bullet_warning in boss_bullet_warning:
        WINDOW.blit(BULLET_WARNING_IMAGE, (bullet_warning.x, bullet_warning.y))
    for bullet in boss_bullets:
        WINDOW.blit(BULLET_IMAGE, (bullet.x, bullet.y))
    for laser_hitbox in boss_laser_hitbox:
        WINDOW.blit(LASER_IMAGE, (laser_hitbox.x - 180/2 + 10, laser_hitbox.y + 5))
    for laser_warning in boss_laser_warning:
        WINDOW.blit(LASER_WARNING_IMAGE, (laser_warning.x, laser_warning.y))

    if minion_two_alive and not victory:
        if minion_two_left:
            WINDOW.blit(LEFT_MINION_IMAGE, (MINION_TWO_HITBOX.x, MINION_TWO_HITBOX.y))
        if not minion_two_left:
            WINDOW.blit(RIGHT_MINION_IMAGE, (MINION_TWO_HITBOX.x, MINION_TWO_HITBOX.y))
    elif not victory:
        WINDOW.blit(SUMMON_MINION_IMAGE, (MINION_TWO_HITBOX.x + 10, MINION_TWO_HITBOX.y))

    if minion_one_alive and not victory:
        if minion_one_right:
            WINDOW.blit(RIGHT_MINION_IMAGE, (MINION_ONE_HITBOX.x, MINION_ONE_HITBOX.y))
        if not minion_one_right:
            WINDOW.blit(LEFT_MINION_IMAGE, (MINION_ONE_HITBOX.x, MINION_ONE_HITBOX.y))
    elif not victory:
        WINDOW.blit(SUMMON_MINION_IMAGE, (MINION_ONE_HITBOX.x, MINION_ONE_HITBOX.y))

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
    if not boss_dive_attack:
        if BOSS_HITBOX.x >= WIDTH - BOSS_WIDTH:
            boss_right = False
        if BOSS_HITBOX.x <= 0:
            boss_right = True
        if boss_right and not victory:
            BOSS_HITBOX.x += BOSS_MOVEMENT
        elif not victory:
            BOSS_HITBOX.x -= BOSS_MOVEMENT
    if boss_dive_attack and current_time - boss_dive_timer <= BOSS_DIVE_COOLDOWN:
        if HITBOX.x > BOSS_HITBOX.x:
            BOSS_HITBOX.x += BOSS_MOVEMENT
        elif HITBOX.x < BOSS_HITBOX.x:
            BOSS_HITBOX.x -= BOSS_MOVEMENT

def boss_attack_movement():
    for bullet in boss_bullets:
        bullet.y += 7
        if bullet.y >= HEIGHT:
            boss_bullets.remove(bullet)
        if bullet.y == HEIGHT:
            boss_bullets.remove(bullet)
    for laser_hitbox in boss_laser_hitbox:
        laser_hitbox.x = BOSS_HITBOX.x + BOSS_WIDTH/2 - 10
        laser_hitbox.y = BOSS_HITBOX.y + BOSS_HEIGHT
    for laser_warning in boss_laser_warning:
        laser_warning.x = BOSS_HITBOX.x + BOSS_WIDTH/2 - 15
        laser_warning.y = BOSS_HITBOX.y + BOSS_HEIGHT

def player_attack_handler():
    global aura_attack, aura_create, aura_cooldown, aura_cooldown_timer, aura_pulse_on,\
        aura_pulse_off, aura_off, lightning_activate, lightning_cooldown,\
        lightning_cooldown_timer

    #aura attack
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

    #lightning bolt attack
    if lightning_activate:
        lightning_activate = False
        lightning_cooldown = True
        lightning_cooldown_timer = current_time
        if lightning_up:
            lightning_hitbot_up = pygame.Rect(HITBOX.x + 2.5, HITBOX.y - LIGHTNING_HEIGHT - 20, LIGHTNING_WIDTH, LIGHTNING_HEIGHT)
            lightning_bolt_up.append(lightning_hitbot_up)
        if lightning_down:
            lightning_hitbot_down = pygame.Rect(HITBOX.x + 2.5, HITBOX.y + HITBOX_HEIGHT, LIGHTNING_WIDTH, LIGHTNING_HEIGHT)
            lightning_bolt_down.append(lightning_hitbot_down)
        if lightning_right:
            lightning_hitbot_right = pygame.Rect(HITBOX.x + 40, HITBOX.y + 20, LIGHTNING_WIDTH, LIGHTNING_HEIGHT)
            lightning_bolt_right.append(lightning_hitbot_right)
        if lightning_left:
            lightning_hitbot_left = pygame.Rect(HITBOX.x - 50, HITBOX.y + 20, LIGHTNING_WIDTH, LIGHTNING_HEIGHT)
            lightning_bolt_left.append(lightning_hitbot_left)

    if current_time - lightning_cooldown_timer >= LIGHTNING_DELAY:
        lightning_cooldown = False
    for lightning_hitbot_up in lightning_bolt_up:
        lightning_hitbot_up.y -= LIGHTNING_MOVEMENT_SPEED
        if lightning_hitbot_up.y <= 0 - LIGHTNING_HEIGHT:
            lightning_bolt_up.remove(lightning_hitbot_up)
    for lightning_hitbot_right in lightning_bolt_right:
        lightning_hitbot_right.x += LIGHTNING_MOVEMENT_SPEED
        if lightning_hitbot_right.x >= WIDTH:
            lightning_bolt_right.remove(lightning_hitbot_right)
    for lightning_hitbot_left in lightning_bolt_left:
        lightning_hitbot_left.x -= LIGHTNING_MOVEMENT_SPEED
        if lightning_hitbot_left.x <= 0:
            lightning_bolt_left.remove(lightning_hitbot_left)
    for lightning_hitbot_down in lightning_bolt_down:
        lightning_hitbot_down.y += LIGHTNING_MOVEMENT_SPEED
        if lightning_hitbot_down.y >= HEIGHT:
            lightning_bolt_down.remove(lightning_hitbot_down )

def boss_attack_handler():
    global  boss_attack, boss_attack_timer, initialized_attack, attack_end, attack_number,\
        bullet_fired, bullet_delay_timer, bullet_total, attack_redo, bullet_redo_delay,\
        bullet_redo_timelaser_delay, laser_fire_time, laser_active, laser_start,\
        boss_attack_number, boss_dive_attack, boss_dive_timer, dive_start, boss_dive_down
    if boss_attack and not victory:

        if not initialized_attack and not attack_end:
            initialized_attack = True
            attack_number = random.randint(1, boss_attack_number)

        #Bullet Attack
        if attack_number == 1 and initialized_attack:
            boss_bullet_warning.clear()
            bullet_warning = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 15, BOSS_HITBOX.y + BOSS_HEIGHT, 30, 30)
            boss_bullet_warning.append(bullet_warning)
            if not bullet_fired and not bullet_redo_delay:
                bullet_fired = True
                bullet = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 10, BOSS_HITBOX.y + BOSS_HEIGHT, 20, 20)
                boss_bullets.append(bullet)
                bullet_delay_timer = current_time
                bullet_total += 1
                BULLET_FIRE_SOUND.play()
            else:
                if current_time - bullet_delay_timer >= BULLET_REDO:
                    bullet_redo_delay = False
                if attack_redo >= 2 and bullet_total >= 10:
                    attack_end = True
                    bullet_total = 0
                if bullet_total >= 10:
                    bullet_total = 0
                    attack_redo += 1
                    bullet_redo_delay = True
                if current_time - bullet_delay_timer >= BOSS_BULLET_DELAY:
                    bullet_fired = False

        # Laser Attack
        if attack_number == 2 and initialized_attack:
            if not laser_active:
                boss_laser_hitbox.clear()
                laser_start = False
                laser_active = True
                laser_fire_time = current_time
                laser_warning = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 15, BOSS_HITBOX.y + BOSS_HEIGHT, 30, 30)
                boss_laser_warning.append(laser_warning)
            if laser_active and current_time - laser_fire_time >= BOSS_LASER_COOLDOWN and not laser_start:
                LASER_SOUND.play()
                laser_start = True
                laser_hitbox = pygame.Rect(BOSS_HITBOX.x + BOSS_WIDTH/2 - 10, BOSS_HITBOX.y + BOSS_HEIGHT, 20, HEIGHT)
                boss_laser_hitbox.append(laser_hitbox)
            if laser_start and current_time - laser_fire_time >= BOSS_LASER_ATTACK:
                laser_active = False
                attack_redo += 1
            if attack_redo >= 3 and laser_start:
                boss_laser_warning.clear()
                attack_end = True
                boss_laser_hitbox.clear()

        if attack_number == 3 and initialized_attack:
            if not dive_start:
                boss_dive_attack = True
                boss_dive_timer = current_time
                dive_start = True
                boss_dive_down = True
                attack_redo += 1
            if current_time - boss_dive_timer >= BOSS_DIVE_COOLDOWN and dive_start:
                if boss_dive_down:
                    BOSS_HITBOX.y += BOSS_DIVE_SPEED
                if not boss_dive_down:
                    BOSS_HITBOX.y -= BOSS_DIVE_SPEED
                if BOSS_HITBOX.y >= HEIGHT - BOSS_HEIGHT:
                    boss_dive_down = False
                if BOSS_HITBOX.y <= BOSS_Y:
                    BOSS_HITBOX.y = BOSS_Y
                    dive_start = False
            if attack_redo >= 4:
                attack_end = True
                dive_start = False
                boss_dive_down = False
                boss_dive_attack = False


        if initialized_attack and attack_end:
            boss_attack_timer = current_time
            boss_attack = False
            initialized_attack = False
            attack_end = False
            boss_bullet_warning.clear()
            attack_number = 6
            attack_redo = 0
    if current_time - boss_attack_timer >= BOSS_ATTACK_DELAY and not boss_attack:
        boss_attack = True

def minion_handler():
    global minion_one_timer, minion_two_timer, minion_one_alive, minion_two_alive,\
        minion_two_left, minion_one_right
    if victory:
        minion_two_alive = False
        minion_one_alive = False
    if current_time - minion_one_timer >= MINION_RESPAWN_COOLDOWN and not minion_one_alive:
        minion_one_alive = True
    if current_time - minion_two_timer >= MINION_RESPAWN_COOLDOWN and not minion_two_alive:
        minion_two_alive = True
    if minion_two_alive and not victory:
        if minion_two_left:
            MINION_TWO_HITBOX.x -= 5
        if not minion_two_left:
            MINION_TWO_HITBOX.x += 5
        if MINION_TWO_HITBOX.x >= WIDTH - MINION_WIDTH:
            minion_two_left = True
        if MINION_TWO_HITBOX.x <= 0:
            minion_two_left = False
        for aura_hitbox in aura:
            if aura_hitbox.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
        for teleport_hitbox in tp_hitbox:
            if teleport_hitbox.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
        for lightning_hitbox_left in lightning_bolt_left:
            if lightning_hitbox_left.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
                lightning_bolt_left.remove(lightning_hitbox_left)
        for lightning_hitbox_down in lightning_bolt_down:
            if lightning_hitbox_down.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
                lightning_bolt_down.remove(lightning_hitbox_down)
        for lightning_hitbox_right in lightning_bolt_right:
            if lightning_hitbox_right.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
                lightning_bolt_right.remove(lightning_hitbox_right)
        for lightning_hitbox_up in lightning_bolt_up:
            if lightning_hitbox_up.colliderect(MINION_TWO_HITBOX):
                minion_two_alive = False
                lightning_bolt_up.remove(lightning_hitbox_up)
        if not minion_two_alive:
            minion_two_timer = current_time
            MINION_TWO_HITBOX.x = WIDTH - MINION_WIDTH
    if minion_one_alive and not victory:
        if minion_one_right:
            MINION_ONE_HITBOX.x += 5
        if not minion_one_right:
            MINION_ONE_HITBOX.x -= 5
        if MINION_ONE_HITBOX.x <= 0:
            minion_one_right = True
        if MINION_ONE_HITBOX.x >= WIDTH - MINION_WIDTH:
            minion_one_right = False
        for aura_hitbox in aura:
            if aura_hitbox.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
        for teleport_hitbox in tp_hitbox:
            if teleport_hitbox.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
        for lightning_hitbox_left in lightning_bolt_left:
            if lightning_hitbox_left.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
                lightning_bolt_left.remove(lightning_hitbox_left)
        for lightning_hitbox_down in lightning_bolt_down:
            if lightning_hitbox_down.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
                lightning_bolt_down.remove(lightning_hitbox_down)
        for lightning_hitbox_right in lightning_bolt_right:
            if lightning_hitbox_right.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
                lightning_bolt_right.remove(lightning_hitbox_right)
        for lightning_hitbox_up in lightning_bolt_up:
            if lightning_hitbox_up.colliderect(MINION_ONE_HITBOX):
                minion_one_alive = False
                lightning_bolt_up.remove(lightning_hitbox_up)
        if not minion_one_alive:
            minion_one_timer = current_time
            MINION_ONE_HITBOX.x = 0

def boss_health_manager():
    global boss_health, victory, boss_immunity, boss_immunity_timer, boss_health_change \
        , boss_attack_number, attack_number, initialized_attack
    if not boss_immunity:
        for portal_hitbox in tp_hitbox:
            if BOSS_HITBOX.colliderect(portal_hitbox):
                boss_health -= TELEPORT_DAMAGE
                boss_immunity = True
        for aura_hitbox in aura:
            if BOSS_HITBOX.colliderect(aura_hitbox):
                boss_health -= AURA_DAMAGE
                boss_immunity = True
        for lightning_hitbox_up in lightning_bolt_up:
            if BOSS_HITBOX.colliderect(lightning_hitbox_up):
                boss_health -= LIGHTNING_BOLT_DAMAGE
                boss_immunity = True
                lightning_bolt_up.remove(lightning_hitbox_up)
        for lightning_hitbox_down in lightning_bolt_down:
            if BOSS_HITBOX.colliderect(lightning_hitbox_down):
                boss_health -= LIGHTNING_BOLT_DAMAGE
                boss_immunity = True
                lightning_bolt_down.remove(lightning_hitbox_down)
        for lightning_hitbox_right in lightning_bolt_right:
            if BOSS_HITBOX.colliderect(lightning_hitbox_right):
                boss_health -= LIGHTNING_BOLT_DAMAGE
                boss_immunity = True
                lightning_bolt_right.remove(lightning_hitbox_right)
        for lightning_hitbox_left in lightning_bolt_left:
            if BOSS_HITBOX.colliderect(lightning_hitbox_left):
                boss_health -= LIGHTNING_BOLT_DAMAGE
                boss_immunity = True
                lightning_bolt_left.remove(lightning_hitbox_left)
        if boss_immunity:
            boss_immunity_timer = current_time
            boss_health_points.clear()
            boss_health_x = BOSS_HEALTH_X
            for _ in range(boss_health):
                boss_health_point = pygame.Rect(boss_health_x, BOSS_HEALTH_Y, HEALTH_POINT_WIDTH,
                                                HEALTH_POINT_HEIGHT)
                boss_health_x += HEALTH_POINT_WIDTH
                boss_health_points.append(boss_health_point)
    if boss_health <= BOSS_HEALTH - BOSS_HEALTH/6 and boss_attack_number <= 2 and not boss_attack:
        boss_attack_number = 3
        initialized_attack = True
        attack_number = 3

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
            DAMAGE_SOUND.play()
        for bullet in boss_bullets:
            if bullet.colliderect(HITBOX) and not victory:
                player_health -= BULLET_DAMAGE
                DAMAGE_SOUND.play()
                boss_bullets.remove(bullet)
                player_immunity_timer = current_time
                player_health_x = PLAYER_HEALTH_X
                player_health_points.clear()
                for _ in range(player_health):
                    player_health_point = pygame.Rect(player_health_x, PLAYER_HEALTH_Y, HEALTH_POINT_ADDITION,
                                                      HEALTH_POINT_HEIGHT)
                    player_health_x += HEALTH_POINT_ADDITION
                    player_health_points.append(player_health_point)
        for laser_hitbox in boss_laser_hitbox:
            if laser_hitbox.colliderect(HITBOX) and not victory:
                player_immunity = True
                player_health -= BOSS_LASER_DAMAGE
                DAMAGE_SOUND.play()
        if MINION_TWO_HITBOX.colliderect(HITBOX) and not victory:
            player_immunity = True
            player_health -= MINION_DAMAGE
            DAMAGE_SOUND.play()
        if MINION_ONE_HITBOX.colliderect(HITBOX) and not victory:
            player_immunity = True
            player_health -= MINION_DAMAGE
            DAMAGE_SOUND.play()
        for spaghetti_hitbox in Health_spaghetti:
            if HITBOX.colliderect(spaghetti_hitbox):
                player_health += HEALTH_GAIN
                Health_spaghetti.remove(spaghetti_hitbox)
                SPAGHETTI_EAT_SOUND.play()
                player_health_x = PLAYER_HEALTH_X
                player_health_points.clear()
                for _ in range(player_health):
                    player_health_point = pygame.Rect(player_health_x, PLAYER_HEALTH_Y, HEALTH_POINT_ADDITION,
                                                      HEALTH_POINT_HEIGHT)
                    player_health_x += HEALTH_POINT_ADDITION
                    player_health_points.append(player_health_point)
        if player_immunity:
            player_immunity_timer = current_time
            player_health_x = PLAYER_HEALTH_X
            player_health_points.clear()
            for _ in range(player_health):
                player_health_point = pygame.Rect(player_health_x, PLAYER_HEALTH_Y, HEALTH_POINT_ADDITION,
                                                  HEALTH_POINT_HEIGHT)
                player_health_x += HEALTH_POINT_ADDITION
                player_health_points.append(player_health_point)
    if current_time - player_immunity_timer >= IMMUNITY and player_immunity:
        player_immunity = False

def health_spaghetti_handler():
    global spaghetti_cooldown, spaghetti_x, spaghetti_y, spaghetti_activate, spaghetti_cooldown_timer
    if not spaghetti_activate and not spaghetti_cooldown:
        spaghetti_cooldown = True
        spaghetti_cooldown_timer = current_time
    if current_time - spaghetti_cooldown_timer >= HEALTH_SPAGHETTI_COOLDOWN:
        spaghetti_activate = True
        spaghetti_cooldown = False
    if spaghetti_activate and len(Health_spaghetti) <= 3:
        spaghetti_x = random.randint(0, WIDTH - HEALTH_SPAGHETTI_WIDTH)
        spaghetti_y = random.randint(BOSS_Y, HEIGHT - HEALTH_SPAGHETTI_HEIGHT)
        spaghetti_hitbox = pygame.Rect(spaghetti_x, spaghetti_y, HEALTH_SPAGHETTI_WIDTH, HEALTH_SPAGHETTI_HEIGHT)
        Health_spaghetti.append(spaghetti_hitbox)
        spaghetti_activate = False

def main():
    global run, Jump, decent, falling, initial_height, tele_up, current_time, tp_delay, \
        tele_left, tp_cooldown, tele_right, left, tp_hitbox, tp, boss_right, boss_health, \
        player_health, victory, player_immunity, player_immunity_timer, boss_immunity_timer,\
        boss_immunity, boss_attack, boss_attack_timer, initialized_attack, attack_end,\
        attack_number, bullet_fired, bullet_delay_timer, bullet_total, attack_redo, bullet_redo_delay, \
        bullet_redo_timer, aura_cooldown, aura_attack, aura_cooldown_timer, aura_create, \
        aura_pulse_on, aura_pulse_off, aura_off, laser_delay, laser_fire_time,\
        laser_active, laser_start, minion_one_timer, minion_two_timer, minion_one_alive, \
        minion_two_alive, minion_two_left, minion_one_right, lightning_up, lightning_down, \
        lightning_left, lightning_right, lightning_cooldown, lightning_cooldown_timer, \
        lightning_activate, spaghetti_cooldown, spaghetti_x, spaghetti_y, spaghetti_activate, \
        spaghetti_cooldown_timer, boss_attack_number, boss_dive_attack, boss_dive_timer, \
        dive_start, boss_dive_down
    boss_dive_down = False
    dive_start = False
    boss_dive_timer = 99999999
    boss_dive_attack = False
    boss_attack_number = 2
    spaghetti_cooldown_timer = 99999999
    spaghetti_x = 0
    spaghetti_y = 0
    spaghetti_cooldown = False
    spaghetti_activate = False
    lightning_activate = False
    lightning_up = True
    lightning_right = False
    lightning_left = False
    lightning_down = False
    lightning_cooldown_timer = 99999999
    lightning_cooldown = False
    minion_one_right = True
    minion_two_left = True
    minion_one_timer = 0
    minion_two_timer = 0
    minion_one_alive = False
    minion_two_alive = False
    laser_start = False
    laser_active = False
    laser_fire_time = 99999999
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
    boss_health = BOSS_HEALTH
    player_health = PLAYER_HEALTH
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
    reset()
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

                if event.key == pygame.K_LCTRL:
                    indicator_change = False
                    if lightning_down and not indicator_change:
                        lightning_down = False
                        lightning_right = True
                        indicator_change = True
                    if lightning_left and not indicator_change:
                        lightning_left = False
                        lightning_down = True
                        indicator_change = True
                    if lightning_right and not indicator_change:
                        lightning_right = False
                        lightning_up = True
                        indicator_change = True
                    if lightning_up and not indicator_change:
                        lightning_up = False
                        lightning_left = True

                if event.key == pygame.K_RCTRL:
                    indicator_change = False
                    if lightning_up and not indicator_change:
                        lightning_up = False
                        lightning_right = True
                        indicator_change = True
                    if lightning_right and not indicator_change:
                        lightning_right = False
                        lightning_down = True
                        indicator_change = True
                    if lightning_down and not indicator_change:
                        lightning_down = False
                        lightning_left = True
                        indicator_change = True
                    if lightning_left and not indicator_change:
                        lightning_left = False
                        lightning_up = True

                if event.key == pygame.K_SPACE and not lightning_cooldown:
                    LIGHTNING_BOLT_SOUND.play()
                    lightning_activate = True

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
        boss_attack_movement()
        player_attack_handler()
        minion_handler()
        health_spaghetti_handler()
        boss_health_manager()
        player_health_manager()
        boss_movement()
        if player_health <= 0:
            main()
        draw()
    pygame.quit()

main()
