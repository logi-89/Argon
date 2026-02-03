import pygame
import math

#  SETTINGS
WIDTH = 1267
HEIGHT = 775
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 220
MAX_DEPTH = 650
DELTA_ANGLE = FOV / NUM_RAYS
SCALE = WIDTH / NUM_RAYS

# GAME STATES
MENU = "menu"
GAME = "game"
CREDITS = "credits"
#game_state = MENU
game_state = GAME

# INIT 
pygame.init()
pygame.display.set_caption("Argon: The Last Knight")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

SQW = 1000
SQH = 1000

# Main Map
MAP =[
    "###########",
    "#...@..#..#",
    "#@#$#....$#",
    "#.###....##",
    "#..#.......",
    "##....##$.#",
    "##@####.###",
    "##.$##.@@@$",
    "#$.####$..#",
    "##...####.#",
    "#....$##$.#",
    "###.#####.#",
    "##$..##...#",
    "#.#......##",
    "#@@#..#..##",
    "#@@@@@@####",
    "####..@####"
]

area1 = [
    "###########",
    "#.......#.#",
    "#..##..##.#",
    "#..##.##..#",
    "#..###....#",
    "#...####.##",
    "###########"
]

TILE = 100
MAP_WIDTH = len(MAP[0]) * TILE
MAP_HEIGHT = len(MAP) * TILE

chests = []
swords = []
fire = []
lightning = []

# Locate chests in the map
for row_idx, row in enumerate(MAP):
    for col_idx, cell in enumerate(row):
        if cell == "$":
            chests.append((
                col_idx * TILE + TILE // 2,
                row_idx * TILE + TILE // 2
            ))

# Locate fire walls in the map
for row_idx, row in enumerate(MAP):
    for col_idx, cell in enumerate(row):
        if cell == "@":
            fire.append((
                col_idx * TILE + TILE // 2,
                row_idx * TILE + TILE // 2
            ))

# FONTS
title_font = pygame.font.SysFont("arialblack", 72)
menu_font = pygame.font.SysFont("arial", 32)
small_font = pygame.font.SysFont("arial", 24)

# PLAYER 
px, py = 150, 150
angle = 0
speed = 2
SWORD_PICKUP_DIST = 40
has_sword = False
coins = 0

# Chest
Chest_size = 255
Chest_image = pygame.image.load("Chest.png")
Chest_image = pygame.transform.scale(Chest_image, (Chest_size, Chest_size))

# sword
sword_size = 255
sword_image = pygame.image.load("sword.png")
sword_image = pygame.transform.scale(sword_image, (sword_size, sword_size))

def draw_centered_text(text, font, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)

def draw_left_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)

def is_wall(x, y):
    if x < 0 or y < 0:
        return True
    if x >= MAP_WIDTH or y >= MAP_HEIGHT:
        return True
    return MAP[int(y // TILE)][int(x // TILE)] == "#"

def is_fire_wall(x, y):
    if x < 0 or y < 0:
        return False
    if x >= MAP_WIDTH or y >= MAP_HEIGHT:
        return False
    return MAP[int(y // TILE)][int(x // TILE)] == "@"

def draw_sword_in_hand():
    if has_sword:
        hand_sword = pygame.transform.scale(sword_image, (300, 300))
        screen.blit(
            hand_sword,
            (WIDTH - 300, HEIGHT - 300)
        )

# GAME LOOP 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == MENU:
                game_state = GAME
            elif game_state == CREDITS:
                game_state = MENU
            elif event.key == pygame.K_c and game_state == GAME:
                game_state = CREDITS

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        if game_state == GAME:
            game_state = MENU
        else:
            running = False

    for chest in chests[:]:
        cx, cy = chest
        if math.hypot(px - cx, py - cy) < 40:
            chests.remove(chest)
            swords.append((cx + 20, cy + 20))
            print("Got Swords")
            coins = coins + 1
            print("Coins:")
            print(coins)

    for lx, ly in lightning:
        if math.hypot(px - lx, py - ly) < 40:
            print("You were struck by lightning! Game Over.")
            running = False

    for fx, fy in fire:
        if math.hypot(px - fx, py - fy) < 40:
            print("You walked into fire!")


    # MENU 
    if game_state == MENU:
        screen.fill((10, 10, 20))

        draw_centered_text("ARGON", title_font, (200, 200, 255), HEIGHT // 2 - 80)
        draw_centered_text("The Last Knight", menu_font, (180, 180, 220), HEIGHT // 2 - 20)

        draw_centered_text("Press any key to begin", small_font, (200, 200, 200), HEIGHT // 2 + 60)
        draw_centered_text("ESC to quit", small_font, (150, 150, 150), HEIGHT // 2 + 100)

        pygame.display.flip()
        clock.tick(60)
        continue

    # CREDITS
    if game_state == CREDITS:
        screen.fill((0, 0, 0))

        draw_centered_text("Credits", menu_font, (255, 255, 255), 120)
        draw_centered_text("Argon: The Last Knight", small_font, (200, 200, 200), 180)
        draw_centered_text("Created by Nathan Chan", small_font, (200, 200, 200), 220)
        draw_centered_text("Powered by Python & Pygame", small_font, (200, 200, 200), 260)
        draw_centered_text("Press any key to return", small_font, (180, 180, 180), 340)

        pygame.display.flip()
        clock.tick(60)
        continue

    # zbuffer
    zbuffer = [0] * NUM_RAYS

    # GAME
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    if keys[pygame.K_w] and not is_wall(px + dx, py + dy):
        px += dx
        py += dy
    if keys[pygame.K_s] and not is_wall(px - dx, py - dy):
        px -= dx
        py -= dy
    if keys[pygame.K_a]:
        angle -= 0.04
    if keys[pygame.K_d]:
        angle += 0.04

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (70, 70, 70), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

    draw_sword_in_hand()

    ray_angle = angle - HALF_FOV

    for ray in range(NUM_RAYS):
        for depth in range(1, MAX_DEPTH):
            x = px + depth * math.cos(ray_angle)
            y = py + depth * math.sin(ray_angle)

            if is_fire_wall(x, y):
                depth *= math.cos(angle - ray_angle)
                wall_height = (50000 / (depth + 0.0001))
                zbuffer[ray] = depth # store wall depth

                #Fire wall coloring
                for i in range(5250):
                    reds = 110 + i // 50

                color = 255 / (1 + depth * depth * 0.00002)
                pygame.draw.rect(screen,(255, 100, 0),(int(ray * SCALE), HEIGHT // 2 - wall_height // 2, int(SCALE + 1), wall_height))
                break

            if is_wall(x, y):
                depth *= math.cos(angle - ray_angle)
                wall_height = (50000 / (depth + 0.0001))
                zbuffer[ray] = depth # store wall depth

                color = 255 / (1 + depth * depth * 0.00002)
                pygame.draw.rect(screen,(color, color, color),(int(ray * SCALE), HEIGHT // 2 - wall_height // 2, int(SCALE + 1), wall_height))
                break

        ray_angle += DELTA_ANGLE

    for cx, cy in chests:
        dx = cx - px
        dy = cy - py
        distance = math.hypot(dx, dy)

        angle_to_chest = math.atan2(dy, dx)
        delta_angle = angle_to_chest - angle

        # Normalize angle
        while delta_angle > math.pi:
            delta_angle -= 2 * math.pi
        while delta_angle < -math.pi:
            delta_angle += 2 * math.pi

        # Inside FOV
        if -HALF_FOV < delta_angle < HALF_FOV and distance > 30:
            projected_dist = distance * math.cos(delta_angle)
            chest_size = min(400, int(50000 / projected_dist))

            ray_index = int((delta_angle + HALF_FOV) / FOV * NUM_RAYS)
            screen_x = ray_index * SCALE

            # Z-buffer check (THIS prevents see-through walls)
            if 0 <= ray_index < NUM_RAYS and projected_dist < zbuffer[ray_index]:
                chest_img = pygame.transform.scale(
                    Chest_image, (chest_size, chest_size)
                )

                screen.blit(
                    chest_img,
                    (screen_x - chest_size // 2, HEIGHT // 2 - chest_size // 2 )
                )
                
    for sword in swords[:]:
        sx, sy = sword
        if math.hypot(px - sx, py - sy) < SWORD_PICKUP_DIST:
            swords.remove(sword)
            has_sword = True
            continue

    for sx, sy in swords:
        dx = sx - px
        dy = sy - py
        distance = math.hypot(dx, dy)

        angle_to_sword = math.atan2(dy, dx)
        delta_angle = angle_to_sword - angle

        while delta_angle > math.pi:
            delta_angle -= 2 * math.pi
        while delta_angle < -math.pi:
            delta_angle += 2 * math.pi

        if -HALF_FOV < delta_angle < HALF_FOV and distance > 30:
            projected_dist = distance * math.cos(delta_angle)
            sword_size = min(350, int(50000 / projected_dist))

            ray_index = int((delta_angle + HALF_FOV) / FOV * NUM_RAYS)
            screen_x = ray_index * SCALE

            if 0 <= ray_index < NUM_RAYS and projected_dist < zbuffer[ray_index]:
                sword_img = pygame.transform.scale(
                    sword_image, (sword_size, sword_size)
                )

                screen.blit(
                    sword_img,
                    (screen_x - sword_size // 2,
                    HEIGHT // 2 + (HEIGHT // 4) - sword_size)
                )

        #draw_centered_text("Press C for Credits", small_font, (200, 200, 200), HEIGHT - 20)
        draw_left_text(f"Coins: {coins}", small_font, (200, 200, 200), 20, 20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
