import pygame
import sys
import random
import math

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
PASTEL_RED = (255, 182, 193)
PASTEL_GREEN = (144, 238, 144)
PASTEL_YELLOW = (255, 255, 224)
PASTEL_BLUE = (173, 216, 230)
DARK_BACKGROUND = (36, 27, 27)
GREY_TONE = (135, 135, 135)
BANNER_RED = (84, 0, 0)
DARK_PILLAR = (38, 38, 38)
CLOUD_COLOR = (173, 216, 230)
PLATFORM_COLOR = (255, 255, 255)
HERO_COLOR_LIGHT = (200, 200, 200)
HERO_COLOR_DARK = (0, 0, 0)

# Глобальные переменные
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 24)

# Система достижений
achievements = {
    "all_keys": {"name": "Ключник", "description": "Собрать все ключи на уровне", "unlocked": False},
    "level1_complete": {"name": "Покоритель замка", "description": "Пройти первый уровень", "unlocked": False},
    "level2_complete": {"name": "Исследователь пещер", "description": "Пройти второй уровень", "unlocked": False},
    "level3_complete": {"name": "Властелин небес", "description": "Пройти третий уровень", "unlocked": False}
}

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))
    
def main_menu():
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        screen.fill(BLACK)
        
        title = font.render("МЕНЮ", True, WHITE)
        play_btn = font.render("1. ИГРАТЬ", True, WHITE)
        achieve_btn = font.render("2. ДОСТИЖЕНИЯ", True, WHITE)
        controls_btn = font.render("3. УПРАВЛЕНИЕ", True, WHITE)  # Изменено название
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(play_btn, (WIDTH//2 - play_btn.get_width()//2, HEIGHT//2 - 30))
        screen.blit(achieve_btn, (WIDTH//2 - achieve_btn.get_width()//2, HEIGHT//2 + 20))
        screen.blit(controls_btn, (WIDTH//2 - controls_btn.get_width()//2, HEIGHT//2 + 70))
        
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 150, HEIGHT//2 - 120, 300, 250), 2)
        pygame.draw.line(screen, WHITE, (WIDTH//2 - 100, HEIGHT//2 - 70), 
                        (WIDTH//2 + 100, HEIGHT//2 - 70), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_selection()
                elif event.key == pygame.K_2:
                    show_achievements()
                elif event.key == pygame.K_3:
                    show_controls()  # Убедитесь, что эта строка есть

        pygame.display.flip()
    

def show_achievements():
    running = True
    while running:
        screen.fill(BLACK)
        
        title = font.render("ДОСТИЖЕНИЯ", True, PASTEL_YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        y_offset = 150
        for achievement in achievements.values():
            pygame.draw.rect(screen, PASTEL_BLUE, (WIDTH//4, y_offset, WIDTH//2, 80), 2)
            name = font.render(achievement["name"], True, WHITE)
            screen.blit(name, (WIDTH//4 + 20, y_offset + 10))
            desc = font.render(achievement["description"], True, PASTEL_GREEN)
            screen.blit(desc, (WIDTH//4 + 20, y_offset + 40))
            status = "✓" if achievement["unlocked"] else "✗"
            status_text = font.render(status, True, PASTEL_GREEN if achievement["unlocked"] else PASTEL_RED)
            screen.blit(status_text, (WIDTH//4 + WIDTH//2 - 40, y_offset + 25))
            y_offset += 100
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
def level_selection():
    while True:
        screen.fill(BLACK)
        
        title = font.render("ВЫБОР УРОВНЯ", True, PASTEL_YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        level_boxes = [
            {"rect": pygame.Rect(WIDTH//4, 150, WIDTH//2, 100),
             "title": "Уровень 1: Заброшенный замок",
             "color": GREY_TONE},
            {"rect": pygame.Rect(WIDTH//4, 280, WIDTH//2, 100),
             "title": "Уровень 2: Подземная пещера",
             "color": (20, 15, 15)},
            {"rect": pygame.Rect(WIDTH//4, 410, WIDTH//2, 100),
             "title": "Уровень 3: Небесные острова",
             "color": CLOUD_COLOR}
        ]
        
        for box in level_boxes:
            pygame.draw.rect(screen, box["color"], box["rect"], 3)
            level_text = font.render(box["title"], True, WHITE)
            screen.blit(level_text, (box["rect"].centerx - level_text.get_width()//2, 
                                   box["rect"].centery - level_text.get_height()//2))
        
        instruction = font.render("Нажмите 1, 2 или 3 для выбора уровня", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 50))
        
        pygame.draw.line(screen, WHITE, (WIDTH//4, 100), (WIDTH*3//4, 100), 2)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_1()
                elif event.key == pygame.K_2:
                    level_2()
                elif event.key == pygame.K_3:
                    level_3()
                elif event.key == pygame.K_ESCAPE:
                    return

def show_controls():
    running = True
    controls = [
        {"key": "ESC", "action": "Вернуться назад"},
        {"key": "→", "action": "Движение вправо"},
        {"key": "←", "action": "Движение влево"},
        {"key": "ПРОБЕЛ", "action": "Прыжок"}
    ]
    
    while running:
        screen.fill(BLACK)
        
        # Заголовок
        title = font.render("УПРАВЛЕНИЕ", True, PASTEL_YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Отрисовка управления
        y_offset = 150
        for control in controls:
            # Рамка для каждой клавиши
            pygame.draw.rect(screen, PASTEL_BLUE, (WIDTH//4, y_offset, WIDTH//2, 60), 2)
            
            # Клавиша
            key = font.render(control["key"], True, PASTEL_GREEN)
            screen.blit(key, (WIDTH//4 + 20, y_offset + 20))
            
            # Действие
            action = font.render(control["action"], True, WHITE)
            screen.blit(action, (WIDTH//4 + 150, y_offset + 20))
            
            y_offset += 80
        
        # Инструкция внизу
        instruction = font.render("Нажмите ESC для возврата", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return



def level_1():
    player_pos = [100, HEIGHT - 50 - 100]
    player_velocity = [0, 0]
    is_on_ground = False
    health = 100
    score = 0
    key_count = 0
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

    platforms = [
        pygame.Rect(0, HEIGHT - 50, 3200, 50),
        pygame.Rect(200, HEIGHT - 150, 150, 20),
        pygame.Rect(400, HEIGHT - 250, 150, 20),
        pygame.Rect(800, HEIGHT - 350, 150, 20),
        pygame.Rect(1200, HEIGHT - 450, 150, 20),
        pygame.Rect(1600, HEIGHT - 250, 150, 20),
        pygame.Rect(2400, HEIGHT - 350, 150, 20),
        pygame.Rect(2800, HEIGHT - 450, 150, 20),
        pygame.Rect(600, HEIGHT - 200, 150, 20)
    ]

    keys = [
        pygame.Rect(210, HEIGHT - 190, 20, 20),
        pygame.Rect(410, HEIGHT - 290, 20, 20),
        pygame.Rect(610, HEIGHT - 390, 20, 20)
    ]

    enemies = [
        pygame.Rect(300, HEIGHT-100, 40, 40),
        pygame.Rect(800, HEIGHT-200, 40, 40),
        pygame.Rect(1200, HEIGHT-300, 40, 40)
    ]

    running = True
    while running:
        screen.fill(GREY_TONE)
        draw_text("Уровень 1: Заброшенный замок", 10, 10)
        draw_text(f"Очки: {score}", 10, 40)
        draw_text(f"Здоровье: {health}", 10, 70)
        draw_text(f"Ключи: {key_count}/3", 10, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            player_velocity[0] = -5
        elif keys_pressed[pygame.K_RIGHT]:
            player_velocity[0] = 5
        else:
            player_velocity[0] = 0

        if keys_pressed[pygame.K_SPACE] and is_on_ground:
            player_velocity[1] = -15
            is_on_ground = False

        player_velocity[1] += GRAVITY
        player_pos[1] += player_velocity[1]
        player_pos[0] += player_velocity[0]

        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        is_on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_velocity[1] > 0:
                    player_pos[1] = platform.top - 50
                    player_velocity[1] = 0
                    is_on_ground = True

        for key in keys[:]:
            if player_rect.colliderect(key):
                keys.remove(key)
                key_count += 1
                score += 100

        if key_count >= 3:
            achievements["all_keys"]["unlocked"] = True
            achievements["level1_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                health -= 1
            enemy.x += random.randint(-2, 2)
            enemy.y += random.randint(-2, 2)
            enemy.x = max(0, min(enemy.x, WIDTH - 40))
            enemy.y = max(0, min(enemy.y, HEIGHT - 90))

        if health <= 0:
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        pygame.draw.rect(screen, HERO_COLOR_DARK, player_rect)
        for platform in platforms:
            pygame.draw.rect(screen, (101, 67, 33), platform)
        for key in keys:
            pygame.draw.polygon(screen, PASTEL_YELLOW, [
                (key.x, key.y), 
                (key.x + 10, key.y - 10), 
                (key.x + 20, key.y), 
                (key.x + 10, key.y + 10)
            ])
        for enemy in enemies:
            pygame.draw.rect(screen, PASTEL_RED, enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
        
        pygame.display.flip()
        pygame.time.delay(30)


def level_2():
    player_pos = [100, HEIGHT - 50 - 100]
    player_velocity = [0, 0]
    is_on_ground = False
    health = 100
    score = 0
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

    platforms = [
        pygame.Rect(0, HEIGHT - 50, 3200, 50),
        pygame.Rect(200, HEIGHT - 150, 150, 20),
        pygame.Rect(500, HEIGHT - 250, 150, 20),
        pygame.Rect(800, HEIGHT - 350, 150, 20),
        pygame.Rect(1100, HEIGHT - 450, 150, 20),
        pygame.Rect(1400, HEIGHT - 250, 150, 20),
        pygame.Rect(1700, HEIGHT - 350, 150, 20),
        pygame.Rect(2000, HEIGHT - 450, 150, 20),
    ]

    enemies = [pygame.Rect(x, y, 30, 30) for x, y in 
              [(400, HEIGHT-300), (800, HEIGHT-400), (1200, HEIGHT-200)]]

    running = True
    while running:
        screen.fill((20, 15, 15))  # Тёмный фон для пещеры
        draw_text("Уровень 2: Подземная пещера", 10, 10)
        draw_text(f"Очки: {score}", 10, 40)
        draw_text(f"Здоровье: {health}", 10, 70)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            player_velocity[0] = -5
        elif keys_pressed[pygame.K_RIGHT]:
            player_velocity[0] = 5
        else:
            player_velocity[0] = 0

        if keys_pressed[pygame.K_SPACE] and is_on_ground:
            player_velocity[1] = -15
            is_on_ground = False

        player_velocity[1] += GRAVITY
        player_pos[1] += player_velocity[1]
        player_pos[0] += player_velocity[0]

        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        is_on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_velocity[1] > 0:
                    player_pos[1] = platform.top - 50
                    player_velocity[1] = 0
                    is_on_ground = True

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                health -= 1
            enemy.y += math.sin(pygame.time.get_ticks() * 0.01) * 2

        if player_pos[0] > WIDTH * 3:
            achievements["level2_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if health <= 0:
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        pygame.draw.rect(screen, HERO_COLOR_LIGHT, player_rect)
        for platform in platforms:
            pygame.draw.rect(screen, (50, 50, 50), platform)
        for enemy in enemies:
            pygame.draw.rect(screen, PASTEL_RED, enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
                
        pygame.display.flip()
        pygame.time.delay(30)

def level_3():
    player_pos = [100, HEIGHT - 50 - 100]
    player_velocity = [0, 0]
    is_on_ground = False
    health = 100
    score = 0
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

    platforms = [
        pygame.Rect(x, y, 150, 20) for x, y in [
            (0, HEIGHT - 50),
            (200, HEIGHT - 150),
            (400, HEIGHT - 250),
            (600, HEIGHT - 350),
            (800, HEIGHT - 450),
            (1000, HEIGHT - 350),
            (1200, HEIGHT - 250),
            (1400, HEIGHT - 150)
        ]
    ]

    clouds = [pygame.Rect(random.randint(0, WIDTH), 
              random.randint(0, HEIGHT//2), 60, 30) for _ in range(10)]

    running = True
    while running:
        screen.fill(CLOUD_COLOR)
        draw_text("Уровень 3: Небесные острова", 10, 10)
        draw_text(f"Очки: {score}", 10, 40)
        draw_text(f"Здоровье: {health}", 10, 70)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            player_velocity[0] = -5
        elif keys_pressed[pygame.K_RIGHT]:
            player_velocity[0] = 5
        else:
            player_velocity[0] = 0

        if keys_pressed[pygame.K_SPACE] and is_on_ground:
            player_velocity[1] = -15
            is_on_ground = False

        player_velocity[1] += GRAVITY * 0.7  # Уменьшенная гравитация для небесного уровня
        player_pos[1] += player_velocity[1]
        player_pos[0] += player_velocity[0]

        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        is_on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_velocity[1] > 0:
                    player_pos[1] = platform.top - 50
                    player_velocity[1] = 0
                    is_on_ground = True

        if player_pos[1] < 0:
            achievements["level3_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if player_pos[1] > HEIGHT:
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return
        
        # Движение облаков
        for cloud in clouds:
            cloud.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
            pygame.draw.ellipse(screen, WHITE, cloud)

        pygame.draw.rect(screen, HERO_COLOR_DARK, player_rect)
        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
        
        pygame.display.flip()
        pygame.time.delay(30)

if __name__ == "__main__":
    pygame.display.set_caption("Игра")
    main_menu()
