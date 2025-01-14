import pygame
import sys
import math
import random
import pytmx

pygame.init()

# ------------------------
# ГЛОБАЛЬНЫЕ КОНСТАНТЫ
# ------------------------
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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра")
font = pygame.font.SysFont("Arial", 24)

# ------------------------
# СИСТЕМА ДОСТИЖЕНИЙ
# ------------------------
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


# ------------------------
# КЛАССЫ ДЛЯ МЕНЮ И ЭКРАНОВ
# ------------------------

class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(FPS)
            screen.fill(BLACK)

            title = font.render("МЕНЮ", True, WHITE)
            play_btn = font.render("1. ИГРАТЬ", True, WHITE)
            achieve_btn = font.render("2. ДОСТИЖЕНИЯ", True, WHITE)
            controls_btn = font.render("3. УПРАВЛЕНИЕ", True, WHITE)

            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(play_btn, (WIDTH // 2 - play_btn.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(achieve_btn, (WIDTH // 2 - achieve_btn.get_width() // 2, HEIGHT // 2 + 20))
            screen.blit(controls_btn, (WIDTH // 2 - controls_btn.get_width() // 2, HEIGHT // 2 + 70))

            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 - 120, 300, 250), 2)
            pygame.draw.line(screen, WHITE, (WIDTH // 2 - 100, HEIGHT // 2 - 70),
                             (WIDTH // 2 + 100, HEIGHT // 2 - 70), 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        LevelSelection().run()
                    elif event.key == pygame.K_2:
                        AchievementsScreen().run()
                    elif event.key == pygame.K_3:
                        ControlsScreen().run()


class AchievementsScreen:
    def __init__(self):
        self.running = True
        self.scroll_y = 0
        self.scroll_speed = 20
        self.total_height = len(achievements) * 100 + 150
        self.visible_height = HEIGHT - 100

    def run(self):
        while self.running:
            screen.fill(BLACK)
            title = font.render("ДОСТИЖЕНИЯ", True, PASTEL_YELLOW)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 150 + self.scroll_y
            for achievement_id, achievement_data in achievements.items():
                if y_offset + 80 > 100 and y_offset < HEIGHT:
                    pygame.draw.rect(screen, WHITE, (WIDTH // 4, y_offset, WIDTH // 2, 80), 2)
                    name_color = PASTEL_GREEN if achievement_data["unlocked"] else WHITE
                    name = font.render(achievement_data["name"], True, name_color)
                    screen.blit(name, (WIDTH // 4 + 20, y_offset + 10))

                    desc = font.render(achievement_data["description"], True, WHITE)
                    screen.blit(desc, (WIDTH // 4 + 20, y_offset + 40))

                    indicator_color = PASTEL_GREEN if achievement_data["unlocked"] else PASTEL_RED
                    pygame.draw.rect(screen, indicator_color,
                                     (WIDTH // 4 + WIDTH // 2 + 20, y_offset + 25, 30, 30))
                y_offset += 100

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_UP:
                        self.scroll_y += self.scroll_speed
                        if self.scroll_y > 0:
                            self.scroll_y = 0
                    elif event.key == pygame.K_DOWN:
                        min_scroll = -(self.total_height - self.visible_height)
                        self.scroll_y -= self.scroll_speed
                        if self.scroll_y < min_scroll:
                            self.scroll_y = min_scroll
                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll_y += event.y * self.scroll_speed
                    if self.scroll_y > 0:
                        self.scroll_y = 0
                    min_scroll = -(self.total_height - self.visible_height)
                    if self.scroll_y < min_scroll:
                        self.scroll_y = min_scroll

            pygame.display.flip()


class ControlsScreen:
    def __init__(self):
        self.running = True
        self.controls = [
            {"key": "ESC", "action": "Вернуться назад"},
            {"key": "→", "action": "Движение вправо"},
            {"key": "←", "action": "Движение влево"},
            {"key": "ПРОБЕЛ", "action": "Прыжок"}
        ]

    def run(self):
        while self.running:
            screen.fill(BLACK)
            title = font.render("УПРАВЛЕНИЕ", True, PASTEL_YELLOW)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 150
            for c in self.controls:
                pygame.draw.rect(screen, PASTEL_BLUE, (WIDTH // 4, y_offset, WIDTH // 2, 60), 2)
                key_text = font.render(c["key"], True, PASTEL_GREEN)
                action_text = font.render(c["action"], True, WHITE)
                screen.blit(key_text, (WIDTH // 4 + 20, y_offset + 20))
                screen.blit(action_text, (WIDTH // 4 + 150, y_offset + 20))
                y_offset += 80

            instruction = font.render("Нажмите ESC для возврата", True, WHITE)
            screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return


class LevelSelection:
    def run(self):
        while True:
            screen.fill(BLACK)

            title = font.render("ВЫБОР УРОВНЯ", True, PASTEL_YELLOW)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            level_boxes = [
                {"rect": pygame.Rect(WIDTH // 4, 150, WIDTH // 2, 100),
                 "title": "Уровень 1: Заброшенный замок",
                 "color": GREY_TONE},
                {"rect": pygame.Rect(WIDTH // 4, 280, WIDTH // 2, 100),
                 "title": "Уровень 2: Подземная пещера",
                 "color": (20, 15, 15)},
                {"rect": pygame.Rect(WIDTH // 4, 410, WIDTH // 2, 100),
                 "title": "Уровень 3: Небесные острова",
                 "color": CLOUD_COLOR}
            ]

            for box in level_boxes:
                pygame.draw.rect(screen, box["color"], box["rect"], 3)
                level_text = font.render(box["title"], True, WHITE)
                screen.blit(level_text, (
                    box["rect"].centerx - level_text.get_width() // 2,
                    box["rect"].centery - level_text.get_height() // 2
                ))

            instruction = font.render("Нажмите 1, 2 или 3 для выбора уровня", True, WHITE)
            screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 50))

            pygame.draw.line(screen, WHITE, (WIDTH // 4, 100), (WIDTH * 3 // 4, 100), 2)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        LevelOne().run()
                    elif event.key == pygame.K_2:
                        LevelTwo().run()
                    elif event.key == pygame.K_3:
                        LevelThree().run()
                    elif event.key == pygame.K_ESCAPE:
                        return


# ------------------------
# КЛАССЫ ДЛЯ УРОВНЕЙ
# ------------------------

class LevelOne:
    """
    Логика уровня 1 (Замок).
    Сохранён весь игровой процесс:
    платформы, турели, враги, ключи и т.д.
    """

    def __init__(self):
        # Переменные игрока
        self.player_pos = [100, HEIGHT - 50 - 100]
        self.player_velocity = [0, 0]
        self.is_on_ground = False
        self.health = 100
        self.score = 0
        self.key_count = 0
        self.camera_x = 0

        # Турели
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_delay = 5000
        self.bullets = []
        self.turrets = [
            {'rect': pygame.Rect(1500, HEIGHT - 300, 40, 40), 'bullets': []},
            {'rect': pygame.Rect(2000, HEIGHT - 400, 40, 40), 'bullets': []},
            {'rect': pygame.Rect(2500, HEIGHT - 350, 40, 40), 'bullets': []}
        ]

        # Наклонные платформы
        self.sloped_platforms = [
            {'rect': pygame.Rect(800, HEIGHT - 200, 200, 20), 'angle': 15},
            {'rect': pygame.Rect(1200, HEIGHT - 300, 200, 20), 'angle': -15},
            {'rect': pygame.Rect(1600, HEIGHT - 400, 200, 20), 'angle': 20}
        ]

        # Платформы
        self.platforms = [
            pygame.Rect(0, HEIGHT - 50, 4000, 50),
            pygame.Rect(-50, 0, 50, HEIGHT),
            pygame.Rect(200, HEIGHT - 150, 100, 20),
            pygame.Rect(400, HEIGHT - 250, 80, 20),
            pygame.Rect(600, HEIGHT - 350, 120, 20),

            pygame.Rect(300, HEIGHT - 400, 100, 20),
            pygame.Rect(500, HEIGHT - 450, 100, 20),
            pygame.Rect(700, HEIGHT - 500, 100, 20),

            pygame.Rect(800, HEIGHT - 200, 100, 20),
            pygame.Rect(1000, HEIGHT - 200, 100, 20),
            pygame.Rect(1200, HEIGHT - 200, 100, 20),

            pygame.Rect(1500, HEIGHT - 600, 100, 20),
            pygame.Rect(1700, HEIGHT - 550, 100, 20),
            pygame.Rect(1900, HEIGHT - 500, 100, 20),

            pygame.Rect(1100, HEIGHT - 400, 50, 200),
            pygame.Rect(1400, HEIGHT - 500, 50, 300),
            pygame.Rect(1800, HEIGHT - 400, 50, 250),

            pygame.Rect(2200, HEIGHT - 350, 200, 20),
            pygame.Rect(2500, HEIGHT - 400, 150, 20),
            pygame.Rect(2800, HEIGHT - 450, 100, 20),
            pygame.Rect(3100, HEIGHT - 500, 200, 20)
        ]

        # Очки опыта
        self.exp_points = [pygame.Rect(x, y, 15, 15) for x, y in [
            (250, HEIGHT - 180), (450, HEIGHT - 280), (650, HEIGHT - 380),
            (350, HEIGHT - 430), (550, HEIGHT - 480), (750, HEIGHT - 530),
            (850, HEIGHT - 230), (1050, HEIGHT - 230), (1250, HEIGHT - 230),
            (1550, HEIGHT - 630), (1750, HEIGHT - 580), (1950, HEIGHT - 530),
            (2250, HEIGHT - 380), (2550, HEIGHT - 430), (2850, HEIGHT - 480),
            (3150, HEIGHT - 530)
        ]]

        # Ключи
        self.keys = [
            pygame.Rect(1250, HEIGHT - 230, 30, 30),
            pygame.Rect(1950, HEIGHT - 530, 30, 30),
            pygame.Rect(3150, HEIGHT - 530, 30, 30)
        ]

        # Враги
        self.ground_enemies = [
            {'rect': pygame.Rect(400, HEIGHT - 110, 60, 60), 'direction': 1, 'start_x': 400, 'end_x': 600},
            {'rect': pygame.Rect(1400, HEIGHT - 110, 60, 60), 'direction': 1, 'start_x': 1400, 'end_x': 1600},
            {'rect': pygame.Rect(2400, HEIGHT - 110, 60, 60), 'direction': 1, 'start_x': 2400, 'end_x': 2600}
        ]

        self.air_enemies = [
            {'rect': pygame.Rect(700, HEIGHT - 300, 30, 30), 'dx': 3, 'dy': 2,
             'bounds': pygame.Rect(600, HEIGHT - 400, 200, 200)},
            {'rect': pygame.Rect(1600, HEIGHT - 400, 30, 30), 'dx': 4, 'dy': 3,
             'bounds': pygame.Rect(1500, HEIGHT - 500, 200, 200)},
            {'rect': pygame.Rect(2500, HEIGHT - 350, 30, 30), 'dx': 5, 'dy': 2,
             'bounds': pygame.Rect(2400, HEIGHT - 450, 200, 200)}
        ]

        self.tall_enemies = [
            {'rect': pygame.Rect(600, HEIGHT - 130, 40, 70), 'direction': 1, 'start_x': 600, 'end_x': 800},
            {'rect': pygame.Rect(1800, HEIGHT - 130, 40, 70), 'direction': 1, 'start_x': 1800, 'end_x': 2000},
        ]

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(FPS)
            screen.fill(GREY_TONE)
            self.camera_x = self.player_pos[0] - WIDTH // 3

            draw_text("Уровень 1: Заброшенный замок", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.health}", 10, 70)
            draw_text(f"Ключи: {self.key_count}/3", 10, 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Управление
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                self.player_velocity[0] = -5
            elif keys_pressed[pygame.K_RIGHT]:
                self.player_velocity[0] = 5
            else:
                self.player_velocity[0] = 0

            if keys_pressed[pygame.K_SPACE] and self.is_on_ground:
                self.player_velocity[1] = -15
                self.is_on_ground = False

            # Физика
            self.player_velocity[1] += GRAVITY
            self.player_pos[1] += self.player_velocity[1]
            self.player_pos[0] += self.player_velocity[0]
            player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)

            # Коллизии с платформами
            self.is_on_ground = False
            for platform in self.platforms:
                if player_rect.colliderect(platform):
                    overlap_left = player_rect.right - platform.left
                    overlap_right = platform.right - player_rect.left
                    overlap_top = player_rect.bottom - platform.top
                    overlap_bottom = platform.bottom - player_rect.top
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    if min_overlap == overlap_top and self.player_velocity[1] > 0:
                        self.player_pos[1] = platform.top - 50
                        self.player_velocity[1] = 0
                        self.is_on_ground = True
                    elif min_overlap == overlap_bottom and self.player_velocity[1] < 0:
                        self.player_pos[1] = platform.bottom
                        self.player_velocity[1] = 0
                    elif min_overlap == overlap_left:
                        self.player_pos[0] = platform.left - 50
                        self.player_velocity[0] = 0
                    elif min_overlap == overlap_right:
                        self.player_pos[0] = platform.right
                        self.player_velocity[0] = 0

            # Наклонные платформы
            player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
            for slope in self.sloped_platforms:
                # Рисуем
                pygame.draw.rect(screen, (101, 67, 33),
                                 (slope['rect'].x - self.camera_x, slope['rect'].y,
                                  slope['rect'].width, slope['rect'].height))
                if player_rect.colliderect(slope['rect']):
                    slide_speed = math.tan(math.radians(slope['angle'])) * 2
                    self.player_velocity[0] += slide_speed

            # Сбор очков
            for point in self.exp_points[:]:
                if player_rect.colliderect(point):
                    self.exp_points.remove(point)
                    self.score += 10

            # Сбор ключей
            for k in self.keys[:]:
                if player_rect.colliderect(k):
                    self.keys.remove(k)
                    self.key_count += 1
                    self.score += 100

            # Обновление турелей
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shot_delay:
                for turret in self.turrets:
                    for angle in range(0, 360, 45):
                        dx = math.cos(math.radians(angle)) * 5
                        dy = math.sin(math.radians(angle)) * 5
                        bullet = {
                            'rect': pygame.Rect(turret['rect'].centerx, turret['rect'].centery, 10, 10),
                            'dx': dx,
                            'dy': dy,
                            'distance': 0
                        }
                        self.bullets.append(bullet)
                self.last_shot_time = current_time

            # Обновление пуль
            for bullet in self.bullets[:]:
                bullet['rect'].x += bullet['dx']
                bullet['rect'].y += bullet['dy']
                bullet['distance'] += math.sqrt(bullet['dx'] ** 2 + bullet['dy'] ** 2)

                if bullet['distance'] > 300:
                    self.bullets.remove(bullet)
                    continue

                for platform in self.platforms:
                    if bullet['rect'].colliderect(platform):
                        self.bullets.remove(bullet)
                        break

                if bullet['rect'].colliderect(player_rect):
                    self.health -= 1
                    self.bullets.remove(bullet)

            # Наземные враги
            for enemy in self.ground_enemies:
                new_x = enemy['rect'].x + 2 * enemy['direction']
                if new_x <= enemy['start_x'] or new_x >= enemy['end_x']:
                    enemy['direction'] *= -1
                enemy['rect'].x = new_x

            # Воздушные
            for enemy in self.air_enemies:
                enemy['rect'].x += enemy['dx']
                enemy['rect'].y += enemy['dy']
                if not enemy['bounds'].contains(enemy['rect']):
                    if enemy['rect'].left < enemy['bounds'].left or enemy['rect'].right > enemy['bounds'].right:
                        enemy['dx'] *= -1
                    if enemy['rect'].top < enemy['bounds'].top or enemy['rect'].bottom > enemy['bounds'].bottom:
                        enemy['dy'] *= -1
                    enemy['rect'].clamp_ip(enemy['bounds'])

            # Высокие враги
            for enemy in self.tall_enemies:
                enemy['rect'].x += 3 * enemy['direction']
                if enemy['rect'].x <= enemy['start_x']:
                    enemy['direction'] = 1
                elif enemy['rect'].x >= enemy['end_x']:
                    enemy['direction'] = -1

            # Отрисовка платформ
            for p in self.platforms:
                pygame.draw.rect(screen, (101, 67, 33),
                                 (p.x - self.camera_x, p.y, p.width, p.height))

            # Отрисовка очков
            for point in self.exp_points:
                pygame.draw.rect(screen, WHITE,
                                 (point.x - self.camera_x, point.y, point.width, point.height))

            # Отрисовка ключей
            for k in self.keys:
                pygame.draw.rect(screen, PASTEL_YELLOW,
                                 (k.x - self.camera_x, k.y, k.width, k.height))

            # Турель + пули
            for turret in self.turrets:
                pygame.draw.rect(screen, (148, 0, 211),
                                 (turret['rect'].x - self.camera_x, turret['rect'].y,
                                  turret['rect'].width, turret['rect'].height))
            for b in self.bullets:
                pygame.draw.rect(screen, (148, 0, 211),
                                 (b['rect'].x - self.camera_x, b['rect'].y,
                                  b['rect'].width, b['rect'].height))

            # Враги
            for enemy in self.ground_enemies:
                if player_rect.colliderect(enemy['rect']):
                    self.health -= 5
                pygame.draw.rect(screen, PASTEL_RED,
                                 (enemy['rect'].x - self.camera_x, enemy['rect'].y,
                                  enemy['rect'].width, enemy['rect'].height))

            for enemy in self.air_enemies:
                if player_rect.colliderect(enemy['rect']):
                    self.health -= 5
                pygame.draw.rect(screen, (255, 100, 100),
                                 (enemy['rect'].x - self.camera_x, enemy['rect'].y,
                                  enemy['rect'].width, enemy['rect'].height))

            for enemy in self.tall_enemies:
                if player_rect.colliderect(enemy['rect']):
                    self.health -= 10
                pygame.draw.rect(screen, (255, 50, 50),
                                 (enemy['rect'].x - self.camera_x, enemy['rect'].y,
                                  enemy['rect'].width, enemy['rect'].height))

            # Игрок
            pygame.draw.rect(screen, HERO_COLOR_DARK,
                             (self.player_pos[0] - self.camera_x, self.player_pos[1], 50, 50))

            # Проверка победы
            if self.key_count >= 3:
                achievements["all_keys"]["unlocked"] = True
                achievements["level1_complete"]["unlocked"] = True
                draw_text("Уровень пройден!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            # Проверка смерти
            if self.health <= 0:
                achievements["died_mobs"]["unlocked"] = True
                draw_text("Игра окончена!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


class LevelTwo:
    """
    Уровень 2 (Подземная пещера).
    Тот же игровой процесс, что раньше, просто в классе.
    """

    def __init__(self):
        self.player_pos = [100, HEIGHT - 50 - 100]
        self.player_velocity = [0, 0]
        self.is_on_ground = False
        self.health = 100
        self.score = 0
        self.camera_x = 0

        self.platforms = [
            pygame.Rect(0, HEIGHT - 50, 3200, 50),
            pygame.Rect(200, HEIGHT - 150, 150, 20),
            pygame.Rect(500, HEIGHT - 250, 150, 20),
            pygame.Rect(800, HEIGHT - 350, 150, 20),
            pygame.Rect(1100, HEIGHT - 450, 150, 20),
            pygame.Rect(1400, HEIGHT - 250, 150, 20),
            pygame.Rect(1700, HEIGHT - 350, 150, 20),
            pygame.Rect(2000, HEIGHT - 450, 150, 20),
        ]

        self.enemies = [pygame.Rect(x, y, 30, 30) for x, y in
                        [(400, HEIGHT - 300), (800, HEIGHT - 400), (1200, HEIGHT - 200)]]

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(FPS)
            screen.fill((20, 15, 15))
            self.camera_x = self.player_pos[0] - WIDTH // 3

            draw_text("Уровень 2: Подземная пещера", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.health}", 10, 70)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                self.player_velocity[0] = -5
            elif keys_pressed[pygame.K_RIGHT]:
                self.player_velocity[0] = 5
            else:
                self.player_velocity[0] = 0

            if keys_pressed[pygame.K_SPACE] and self.is_on_ground:
                self.player_velocity[1] = -15
                self.is_on_ground = False

            self.player_velocity[1] += GRAVITY
            self.player_pos[1] += self.player_velocity[1]
            self.player_pos[0] += self.player_velocity[0]

            player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
            self.is_on_ground = False

            for platform in self.platforms:
                if player_rect.colliderect(platform):
                    if self.player_velocity[1] > 0:
                        self.player_pos[1] = platform.top - 50
                        self.player_velocity[1] = 0
                        self.is_on_ground = True

            # Отрисовка игрока и платформ
            pygame.draw.rect(screen, HERO_COLOR_LIGHT,
                             (self.player_pos[0] - self.camera_x, self.player_pos[1], 50, 50))
            for p in self.platforms:
                pygame.draw.rect(screen, (50, 50, 50),
                                 (p.x - self.camera_x, p.y, p.width, p.height))

            for enemy in self.enemies:
                if player_rect.colliderect(enemy):
                    self.health -= 1
                # колебания по синусу
                enemy.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
                pygame.draw.rect(screen, PASTEL_RED,
                                 (enemy.x - self.camera_x, enemy.y, enemy.width, enemy.height))

            if self.player_pos[0] > WIDTH * 3:
                achievements["level2_complete"]["unlocked"] = True
                draw_text("Уровень пройден!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            if self.health <= 0:
                achievements["died_mobs"]["unlocked"] = True
                draw_text("Игра окончена!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


class LevelThree:
    """
    Уровень 3 (Небесные острова).
    """

    def __init__(self):
        self.player_pos = [100, HEIGHT - 50 - 100]
        self.player_velocity = [0, 0]
        self.is_on_ground = False
        self.health = 100
        self.score = 0
        self.camera_x = 0

        self.platforms = [
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

        self.clouds = [pygame.Rect(random.randint(0, WIDTH),
                                   random.randint(0, HEIGHT // 2), 60, 30) for _ in range(10)]

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(FPS)
            screen.fill(CLOUD_COLOR)
            self.camera_x = self.player_pos[0] - WIDTH // 3

            draw_text("Уровень 3: Небесные острова", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.health}", 10, 70)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                self.player_velocity[0] = -5
            elif keys_pressed[pygame.K_RIGHT]:
                self.player_velocity[0] = 5
            else:
                self.player_velocity[0] = 0

            if keys_pressed[pygame.K_SPACE] and self.is_on_ground:
                self.player_velocity[1] = -15
                self.is_on_ground = False

            self.player_velocity[1] += GRAVITY * 0.7
            self.player_pos[1] += self.player_velocity[1]
            self.player_pos[0] += self.player_velocity[0]

            player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 50, 50)
            self.is_on_ground = False
            for p in self.platforms:
                if player_rect.colliderect(p):
                    if self.player_velocity[1] > 0:
                        self.player_pos[1] = p.top - 50
                        self.player_velocity[1] = 0
                        self.is_on_ground = True

            # Облака
            for cloud in self.clouds:
                cloud.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
                pygame.draw.ellipse(screen, WHITE,
                                    (cloud.x - self.camera_x, cloud.y, cloud.width, cloud.height))

            # Игрок и платформы
            pygame.draw.rect(screen, HERO_COLOR_DARK,
                             (self.player_pos[0] - self.camera_x, self.player_pos[1], 50, 50))
            for p in self.platforms:
                pygame.draw.rect(screen, PLATFORM_COLOR,
                                 (p.x - self.camera_x, p.y, p.width, p.height))

            # Проверка завершения
            if self.player_pos[0] >= 3000:
                achievements["level3_complete"]["unlocked"] = True
                draw_text("Уровень пройден!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            if self.player_pos[1] > HEIGHT:
                achievements["died_fall"]["unlocked"] = True
                draw_text("Игра окончена!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


# ------------------------
# ЗАПУСК ВСЕЙ ИГРЫ
# ------------------------
if __name__ == "__main__":
    MainMenu().run()
