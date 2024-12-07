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
    "level3_complete": {"name": "Властелин небес", "description": "Пройти третий уровень", "unlocked": False},
    "exp_50": {"name": "Начинающий собиратель", "description": "Собрать 50 очков опыта", "unlocked": False},
    "exp_100": {"name": "Опытный собиратель", "description": "Собрать 100 очков опыта", "unlocked": False},
    "exp_200": {"name": "Мастер собиратель", "description": "Собрать 200 очков опыта", "unlocked": False},
    "died_mobs": {"name": "Неосторожность", "description": "Умереть от врагов", "unlocked": False},
    "died_fall": {"name": "Неудачный прыжок", "description": "Умереть от падения на 3 уровне", "unlocked": False}
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
    scroll_y = 0
    scroll_speed = 20
    total_height = len(achievements) * 100 + 150  # Общая высота всех достижений
    visible_height = HEIGHT - 100  # Видимая область

    while running:
        screen.fill(BLACK)
        
        # Заголовок (фиксированный)
        title = font.render("ДОСТИЖЕНИЯ", True, PASTEL_YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Область прокрутки
        y_offset = 150 + scroll_y
        
        # Отрисовка достижений
        for achievement_id, achievement in achievements.items():
            # Проверяем, находится ли достижение в видимой области
            if y_offset + 80 > 100 and y_offset < HEIGHT:
                # Рамка достижения
                pygame.draw.rect(screen, WHITE, (WIDTH//4, y_offset, WIDTH//2, 80), 2)
                
                # Название и описание
                name_color = PASTEL_GREEN if achievement["unlocked"] else WHITE
                name = font.render(achievement["name"], True, name_color)
                screen.blit(name, (WIDTH//4 + 20, y_offset + 10))
                
                desc = font.render(achievement["description"], True, WHITE)
                screen.blit(desc, (WIDTH//4 + 20, y_offset + 40))
                
                # Индикатор выполнения (квадрат справа от рамки)
                indicator_color = PASTEL_GREEN if achievement["unlocked"] else PASTEL_RED
                pygame.draw.rect(screen, indicator_color, 
                    (WIDTH//4 + WIDTH//2 + 20, y_offset + 25, 30, 30))
            
            y_offset += 100

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # Прокрутка клавишами вверх/вниз
                elif event.key == pygame.K_UP:
                    scroll_y += scroll_speed
                    if scroll_y > 0:
                        scroll_y = 0
                elif event.key == pygame.K_DOWN:
                    min_scroll = -(total_height - visible_height)
                    scroll_y -= scroll_speed
                    if scroll_y < min_scroll:
                        scroll_y = min_scroll
            # Прокрутка колесиком мыши
            elif event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * scroll_speed
                if scroll_y > 0:
                    scroll_y = 0
                min_scroll = -(total_height - visible_height)
                if scroll_y < min_scroll:
                    scroll_y = min_scroll

        pygame.display.flip()


                    
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
    camera_x = 0

    # Расширенный список платформ разных размеров
    platforms = [
        # Основной пол
        pygame.Rect(0, HEIGHT - 50, 4000, 50),
        # Короткие платформы
        pygame.Rect(200, HEIGHT - 150, 100, 20),
        pygame.Rect(500, HEIGHT - 250, 80, 20),
        pygame.Rect(800, HEIGHT - 350, 120, 20),
        # Средние платформы
        pygame.Rect(1200, HEIGHT - 450, 200, 20),
        pygame.Rect(1600, HEIGHT - 250, 180, 20),
        pygame.Rect(2000, HEIGHT - 350, 160, 20),
        # Длинные платформы
        pygame.Rect(2400, HEIGHT - 250, 300, 20),
        pygame.Rect(2800, HEIGHT - 350, 250, 20),
        pygame.Rect(3200, HEIGHT - 450, 280, 20),
        # Вертикальные платформы
        pygame.Rect(1000, HEIGHT - 300, 50, 250),
        pygame.Rect(1800, HEIGHT - 400, 50, 350),
        pygame.Rect(2600, HEIGHT - 350, 50, 300)
    ]

    # Очки (белые точки)
    exp_points = [
        pygame.Rect(x, y, 15, 15) for x, y in [
            (250, HEIGHT - 180),  # На короткой платформе
            (520, HEIGHT - 280),  # На другой платформе
            (850, HEIGHT - 380),
            (1250, HEIGHT - 480),
            (1650, HEIGHT - 280),
            (2050, HEIGHT - 380),
            (2450, HEIGHT - 280),
            (2850, HEIGHT - 380),
            (3250, HEIGHT - 480),
            # На полу
            (400, HEIGHT - 80),
            (800, HEIGHT - 80),
            (1200, HEIGHT - 80),
            (1600, HEIGHT - 80),
            (2000, HEIGHT - 80),
            (2400, HEIGHT - 80),
            (2800, HEIGHT - 80),
            (3200, HEIGHT - 80)
        ]
    ]

    # Ключи (желтые, 3 штуки)
    keys = [
        pygame.Rect(600, HEIGHT - 300, 30, 30),    # Первый ключ
        pygame.Rect(1500, HEIGHT - 500, 30, 30),   # Второй ключ
        pygame.Rect(3300, HEIGHT - 500, 30, 30)    # Последний ключ
    ]

    # Наземные враги (с корректной начальной позицией)
    ground_enemies = [
        {'rect': pygame.Rect(400, HEIGHT-110, 60, 60), 'direction': 1, 'start_x': 400, 'end_x': 600},
        {'rect': pygame.Rect(1400, HEIGHT-110, 60, 60), 'direction': 1, 'start_x': 1400, 'end_x': 1600},
        {'rect': pygame.Rect(2400, HEIGHT-110, 60, 60), 'direction': 1, 'start_x': 2400, 'end_x': 2600}
    ]

    # Воздушные враги с ограничением движения
    air_enemies = [
        {'rect': pygame.Rect(700, HEIGHT-300, 30, 30), 'dx': 3, 'dy': 2, 'bounds': pygame.Rect(600, HEIGHT-400, 200, 200)},
        {'rect': pygame.Rect(1600, HEIGHT-400, 30, 30), 'dx': 4, 'dy': 3, 'bounds': pygame.Rect(1500, HEIGHT-500, 200, 200)},
        {'rect': pygame.Rect(2500, HEIGHT-350, 30, 30), 'dx': 5, 'dy': 2, 'bounds': pygame.Rect(2400, HEIGHT-450, 200, 200)}
    ]

    running = True
    while running:
        screen.fill(GREY_TONE)
        camera_x = player_pos[0] - WIDTH//3

        # UI
        draw_text("Уровень 1: Заброшенный замок", 10, 10)
        draw_text(f"Очки: {score}", 10, 40)
        draw_text(f"Здоровье: {health}", 10, 70)
        draw_text(f"Ключи: {key_count}/3", 10, 100)

        # Обработка движения и коллизий (оставляем как есть)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Управление
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

        # Физика
        player_velocity[1] += GRAVITY
        player_pos[1] += player_velocity[1]
        player_pos[0] += player_velocity[0]

        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        # Коллизии с платформами
        is_on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_velocity[1] > 0:
                    player_pos[1] = platform.top - 50
                    player_velocity[1] = 0
                    is_on_ground = True

        # Сбор ключей
        for key in keys[:]:
            if player_rect.colliderect(key):
                keys.remove(key)
                key_count += 1
                score += 100

        # Сбор очков
        for point in exp_points[:]:
            if player_rect.colliderect(point):
                exp_points.remove(point)
                score += 10
                if score >= 50:
                    achievements["exp_50"]["unlocked"] = True
                if score >= 100:
                    achievements["exp_100"]["unlocked"] = True
                if score >= 200:
                    achievements["exp_200"]["unlocked"] = True

        # Движение наземных врагов с ограничениями
        for enemy in ground_enemies:
            enemy['rect'].x += 2 * enemy['direction']
            if enemy['rect'].x <= enemy['start_x'] or enemy['rect'].x >= enemy['end_x']:
                enemy['direction'] *= -1
            
            # Проверка коллизии с полом
            on_platform = False
            for platform in platforms:
                if enemy['rect'].bottom == platform.top and \
                   enemy['rect'].right >= platform.left and \
                   enemy['rect'].left <= platform.right:
                    on_platform = True
                    break
            if not on_platform:
                enemy['rect'].bottom = HEIGHT - 50  # Возвращаем на пол

        # Движение воздушных врагов с ограничениями
        for enemy in air_enemies:
            enemy['rect'].x += enemy['dx']
            enemy['rect'].y += enemy['dy']
            
            # Ограничение движения в заданных границах
            if not enemy['bounds'].contains(enemy['rect']):
                if enemy['rect'].left < enemy['bounds'].left or enemy['rect'].right > enemy['bounds'].right:
                    enemy['dx'] *= -1
                if enemy['rect'].top < enemy['bounds'].top or enemy['rect'].bottom > enemy['bounds'].bottom:
                    enemy['dy'] *= -1
                # Возвращаем врага в границы
                enemy['rect'].clamp_ip(enemy['bounds'])

        # Отрисовка
        # Платформы
        for platform in platforms:
            pygame.draw.rect(screen, (101, 67, 33), 
                (platform.x - camera_x, platform.y, platform.width, platform.height))

        # Очки (белые)
        for point in exp_points:
            pygame.draw.rect(screen, WHITE, 
                (point.x - camera_x, point.y, point.width, point.height))

        # Ключи (желтые)
        for key in keys:
            pygame.draw.rect(screen, PASTEL_YELLOW, 
                (key.x - camera_x, key.y, key.width, key.height))

        # Враги
        for enemy in ground_enemies:
            pygame.draw.rect(screen, PASTEL_RED, 
                (enemy['rect'].x - camera_x, enemy['rect'].y, 
                 enemy['rect'].width, enemy['rect'].height))

        for enemy in air_enemies:
            pygame.draw.rect(screen, (255, 100, 100), 
                (enemy['rect'].x - camera_x, enemy['rect'].y, 
                 enemy['rect'].width, enemy['rect'].height))
            
        if key_count >= 3:
            achievements["all_keys"]["unlocked"] = True
            achievements["level1_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if health <= 0:
            achievements["died_mobs"]["unlocked"] = True
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        # Игрок
        pygame.draw.rect(screen, HERO_COLOR_DARK, 
            (player_pos[0] - camera_x, player_pos[1], 50, 50))

        pygame.display.flip()
        pygame.time.delay(30)




def level_2():
    player_pos = [100, HEIGHT - 50 - 100]
    player_velocity = [0, 0]
    is_on_ground = False
    health = 100
    score = 0
    camera_x = 0

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
        screen.fill((20, 15, 15))
        camera_x = player_pos[0] - WIDTH//3

        # UI элементы
        draw_text("Уровень 2: Подземная пещера", 10, 10)
        draw_text(f"Очки: {score}", 10, 40)
        draw_text(f"Здоровье: {health}", 10, 70)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Управление
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

        # Физика
        player_velocity[1] += GRAVITY
        player_pos[1] += player_velocity[1]
        player_pos[0] += player_velocity[0]

        # Коллизии
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
        is_on_ground = False
        
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_velocity[1] > 0:
                    player_pos[1] = platform.top - 50
                    player_velocity[1] = 0
                    is_on_ground = True

        # Отрисовка с учетом камеры
        pygame.draw.rect(screen, HERO_COLOR_LIGHT, 
            (player_pos[0] - camera_x, player_pos[1], 50, 50))

        for platform in platforms:
            pygame.draw.rect(screen, (50, 50, 50), 
                (platform.x - camera_x, platform.y, platform.width, platform.height))

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                health -= 1
            enemy.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
            pygame.draw.rect(screen, PASTEL_RED, 
                (enemy.x - camera_x, enemy.y, enemy.width, enemy.height))

        if player_pos[0] > WIDTH * 3:
            achievements["level2_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if health <= 0:
            achievements["died_mobs"]["unlocked"] = True
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        pygame.display.flip()
        pygame.time.delay(30)

def level_3():
    player_pos = [100, HEIGHT - 50 - 100]
    player_velocity = [0, 0]
    is_on_ground = False
    health = 100
    score = 0
    camera_x = 0

    platforms = [
        pygame.Rect(x, y, 150, 20) for x, y in [
            (0, HEIGHT - 50),
            (200, HEIGHT - 150),
            (400, HEIGHT - 250),
            (600, HEIGHT - 350),
            (800, HEIGHT - 450),
            (1000, HEIGHT - 350),
            (1200, HEIGHT - 250),
            (1400, HEIGHT - 150),
            (1600, HEIGHT - 200),
            (1800, HEIGHT - 300),
            (2000, HEIGHT - 400),
            (2200, HEIGHT - 200),
            (2400, HEIGHT - 300),
            (2600, HEIGHT - 400),
            (2800, HEIGHT - 200),
            (3000, HEIGHT - 300)
        ]
    ]

    clouds = [pygame.Rect(random.randint(0, WIDTH), 
              random.randint(0, HEIGHT//2), 60, 30) for _ in range(10)]

    running = True
    while running:
        screen.fill(CLOUD_COLOR)
        camera_x = player_pos[0] - WIDTH//3

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

        player_velocity[1] += GRAVITY * 0.7
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

        # Отрисовка облаков
        for cloud in clouds:
            cloud.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
            pygame.draw.ellipse(screen, WHITE, 
                (cloud.x - camera_x, cloud.y, cloud.width, cloud.height))

        # Отрисовка игрока и платформ
        pygame.draw.rect(screen, HERO_COLOR_DARK, 
            (player_pos[0] - camera_x, player_pos[1], 50, 50))

        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, 
                (platform.x - camera_x, platform.y, platform.width, platform.height))

        # Проверка завершения уровня
        if player_pos[0] >= 3000:
            achievements["level3_complete"]["unlocked"] = True
            draw_text("Уровень пройден!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if player_pos[1] > HEIGHT:
            achievements["died_fall"]["unlocked"] = True
            draw_text("Игра окончена!", WIDTH//2 - 100, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        pygame.display.flip()
        pygame.time.delay(30)

        
if __name__ == "__main__":
    pygame.display.set_caption("Игра")
    main_menu()