import pygame
import sys
import pytmx
from database import init_db, save_achievement, load_achievements


pygame.init()

# ------------------------
# ГЛОБАЛЬНЫЕ КОНСТАНТЫ
# ------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.2

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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра")
font = pygame.font.SysFont("Arial", 24)

from database import init_db, save_achievement, load_achievements

# ------------------------
# СИСТЕМА ДОСТИЖЕНИЙ
# ------------------------
base_achievements = {
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

# Инициализация базы данных и загрузка достижений
init_db()
loaded_achievements = load_achievements()
achievements = base_achievements.copy()

# Обновление статуса достижений из базы данных
if loaded_achievements:
    for key, value in loaded_achievements.items():
        if key in achievements:
            achievements[key]["unlocked"] = value["unlocked"]


def unlock_achievement(achievement_id):
    achievements[achievement_id]["unlocked"] = True
    save_achievement(
        achievement_id,
        achievements[achievement_id]["name"],
        achievements[achievement_id]["description"],
        True
    )



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

    # нарезалка


def load_spritesheet(path):

    sheet = pygame.image.load(path).convert_alpha()
    frame_width = 32
    frame_height = 32
    sheet_width = sheet.get_width()
    # Сколько кадров помещается
    num_frames = sheet_width // frame_width

    frames = []
    for i in range(num_frames):
        # Вырезаем кадр
        frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surf.blit(sheet, (0, 0),
                        (i * frame_width, 0, frame_width, frame_height))
        frames.append(frame_surf)
    return frames


class Bird:
    def __init__(self, x, y, left_bound, right_bound):

        self.x = x
        self.y = y
        self.left_bound = left_bound
        self.right_bound = right_bound

        # Скорость движения
        self.speed_x = 1
        self.direction = 1

        # Загружаем спрайт-лист "bird (32x32).png"
        self.sprite_sheet = pygame.image.load("assets/enemy/bird (32x32).png").convert_alpha()

        frame_width = 32
        frame_height = 32
        num_frames = 9

        self.frames = []
        for i in range(num_frames):
            frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surf.blit(
                self.sprite_sheet,
                (0, 0),
                (i * frame_width, 0, frame_width, frame_height)
            )
            self.frames.append(frame_surf)

        # Параметры анимации
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.08  # скорость перелистывания кадров

    def update(self):

        # Движение
        self.x += self.speed_x * self.direction

        # Меняем направление, достигнув границ
        if self.x < self.left_bound:
            self.x = self.left_bound
            self.direction = 1
        elif self.x > self.right_bound:
            self.x = self.right_bound
            self.direction = -1

        # Анимация
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface, camera_x=0, scale_factor=1.0):

        # Получаем текущий кадр
        frame = self.frames[self.current_frame]

        # Если задан масштаб, подгоняем размер кадра
        if scale_factor != 1.0:
            w = int(frame.get_width() * scale_factor)
            h = int(frame.get_height() * scale_factor)
            frame = pygame.transform.scale(frame, (w, h))

        # Вычисляем экранные координаты с учётом камеры и масштаба
        screen_x = (self.x * scale_factor) - camera_x
        screen_y = self.y * scale_factor

        surface.blit(frame, (screen_x, screen_y))


class Player:
    def __init__(self, x=100, y=200, width=32, height=32, health=100):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health

        # Скорости по осям
        self.vel_x = 0
        self.vel_y = 0

        # Для двойного прыжка
        self.max_jumps = 2  # Сколько прыжков подряд можно сделать
        self.jumps_remaining = 2  # Сколько осталось прыжков на данный момент
        self.jump_force = 6  # Сила прыжка (как высоко прыгает)

        # Флаг на земле
        self.is_on_ground = False

        self.space_pressed_last_frame = False

        # ------------------------------
        # 1) ЗАГРУЗКА СПРАЙТОВ
        # ------------------------------
        self.animations = {
            "idle": load_spritesheet("assets/player/Idle (32x32).png"),
            "run": load_spritesheet("assets/player/Run (32x32).png"),
            "jump": load_spritesheet("assets/player/Jump (32x32).png"),
            "double_jump": load_spritesheet("assets/player/Double Jump (32x32).png"),
            "fall": load_spritesheet("assets/player/Fall (32x32).png")
        }

        # Текущая анимация и кадр
        self.current_anim = "idle"
        self.anim_frame = 0
        self.anim_speed = 0.2  # скорость перелистывания

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -3
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 3

        # Проверяем, что SPACE нажат сейчас, но не был нажат в предыдущем кадре
        if keys[pygame.K_SPACE] and not self.space_pressed_last_frame:
            if self.jumps_remaining > 0:
                self.vel_y = -self.jump_force
                self.jumps_remaining -= 1
                self.is_on_ground = False

        # Запоминаем состояние для следующего кадра
        self.space_pressed_last_frame = keys[pygame.K_SPACE]

    def update_physics(self, gravity=1):
        """
        Применяем гравитацию и обновляем координаты.
        Вызывается каждый кадр в игровом цикле.
        """
        self.vel_y += gravity
        self.x += self.vel_x
        self.y += self.vel_y

    def reset_jumps(self):
        """
        Сбрасываем счётчик прыжков (например, когда встали на землю).
        """
        self.jumps_remaining = self.max_jumps

    def get_rect(self):
        """
        Возвращает pygame.Rect, соответствующий игроку в координатах карты.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update_animation(self):
        """
        Определяем, какая анимация сейчас нужна, и переключаем/перелистываем кадры.
        """
        # 1. Выбираем текущую анимацию по состоянию
        if self.is_on_ground:
            # На земле
            if abs(self.vel_x) > 0.1:
                self.current_anim = "run"
            else:
                self.current_anim = "idle"
        else:
            # В воздухе
            if self.vel_y < 0:
                # Прыгаем вверх
                if self.jumps_remaining == self.max_jumps - 1:
                    # Это первый прыжок
                    self.current_anim = "jump"
                else:
                    # Если jumps_remaining уже на 0, значит это второй прыжок
                    self.current_anim = "double_jump"
            else:
                # Падаем вниз
                self.current_anim = "fall"

        # 2. Перелистываем кадры
        self.anim_frame += self.anim_speed
        # Сколько кадров в выбранной анимации?
        anim_list = self.animations[self.current_anim]
        if self.anim_frame >= len(anim_list):
            self.anim_frame = 0

    def draw(self, surface, camera_x, scale_factor):
        """
        Рисуем текущий кадр анимации.
        """
        # Сначала получаем список кадров для self.current_anim
        anim_list = self.animations[self.current_anim]
        # округляем anim_frame вниз, чтобы получить индекс
        frame_index = int(self.anim_frame)
        # защита от выхода за диапазон
        frame_index = min(frame_index, len(anim_list) - 1)

        frame = anim_list[frame_index]

        # Масштабируем кадр, если нужно
        if scale_factor != 1.0:
            w = int(frame.get_width() * scale_factor)
            h = int(frame.get_height() * scale_factor)
            frame = pygame.transform.scale(frame, (w, h))

        # Вычисляем экранные координаты
        screen_x = (self.x * scale_factor) - camera_x
        screen_y = self.y * scale_factor

        surface.blit(frame, (screen_x, screen_y))


# ------------------------
# КЛАССЫ ДЛЯ УРОВНЕЙ
# ------------------------


def draw_text(text, x, y, color=(0, 0, 0)):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


class Bat:
    def __init__(self, x, y, left_bound, right_bound):
        self.x = x
        self.y = y
        self.left_bound = left_bound
        self.right_bound = right_bound

        # Скорость и направление
        self.speed_x = 1
        self.direction = 1

        # Загружаем спрайт-лист "bat (46x30).png"
        self.sprite_sheet = pygame.image.load("assets/enemy/bat (46x30).png").convert_alpha()

        self.frames = []
        frame_width = 46
        frame_height = 30
        num_frames = 8  # Количество кадров
        for i in range(num_frames):
            frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surf.blit(
                self.sprite_sheet,
                (0, 0),
                (i * frame_width, 0, frame_width, frame_height)
            )
            self.frames.append(frame_surf)

        # Параметры анимации
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.08  # скорость перелистывания кадров

    def update(self):
        """ Двигаемся между left_bound и right_bound и листаем анимацию """
        self.x += self.speed_x * self.direction

        # Меняем направление на границах
        if self.x < self.left_bound:
            self.x = self.left_bound
            self.direction = 1
        elif self.x > self.right_bound:
            self.x = self.right_bound
            self.direction = -1

        # Анимация
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface, camera_x=0, scale_factor=1.0):
        frame = self.frames[self.current_frame]

        if scale_factor != 1.0:
            w = int(frame.get_width() * scale_factor)
            h = int(frame.get_height() * scale_factor)
            frame = pygame.transform.scale(frame, (w, h))

        screen_x = (self.x * scale_factor) - camera_x
        screen_y = (self.y * scale_factor)
        surface.blit(frame, (screen_x, screen_y))


class Ghost:
    def __init__(self, x, y, left_bound, right_bound):
        # Позиция в пикселях (координаты карты)
        self.x = x
        self.y = y
        self.left_bound = left_bound
        self.right_bound = right_bound

        self.speed_x = 1
        self.direction = 1

        # Загрузка спрайтового листа
        # Убедитесь, что путь к файлу совпадает с вашей структурой папок:
        self.sprite_sheet = pygame.image.load("assets/enemy/ghost (44x30).png").convert_alpha()

        # Разрезаем спрайт‐шит на кадры (предположим, что там 10 кадров по 44×30)
        self.frames = []
        frame_width = 44
        frame_height = 30
        num_frames = 10  # Количество кадров в спрайте

        for i in range(num_frames):
            frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surf.blit(
                self.sprite_sheet,
                (0, 0),
                (i * frame_width, 0, frame_width, frame_height)
            )
            self.frames.append(frame_surf)

        # Параметры анимации
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.08  # Чем больше, тем быстрее перебираются кадры

    def update(self):
        """
        Обновляем логику привидения:
        - смещаемся, если нужно
        - перелистываем кадры анимации
        """
        # Движение
        self.x += self.speed_x * self.direction

        if self.x < self.left_bound:
            self.x = self.left_bound
            self.direction = 1
        elif self.x > self.right_bound:
            self.x = self.right_bound
            self.direction = -1

        # Анимация
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface, camera_x=0, scale_factor=1.0):
        frame = self.frames[self.current_frame]

        if scale_factor != 1.0:
            w = int(frame.get_width() * scale_factor)
            h = int(frame.get_height() * scale_factor)
            frame = pygame.transform.scale(frame, (w, h))

        screen_x = (self.x * scale_factor) - camera_x
        screen_y = (self.y * scale_factor)
        surface.blit(frame, (screen_x, screen_y))

def save_level1_achievements(key_count=0, win=False, death=False):
    if win:
        achievements["level1_complete"]["unlocked"] = True
        save_achievement("level1_complete", "Покоритель замка", "Пройти первый уровень", True)
        if key_count >= 3:
            achievements["all_keys"]["unlocked"] = True
            save_achievement("all_keys", "Ключник", "Собрать все ключи на уровне", True)
    if death:
        achievements["died_mobs"]["unlocked"] = True
        save_achievement("died_mobs", "Неосторожность", "Умереть от врагов", True)

def save_level2_achievements(key_count=0, win=False, death=False):
    if win:
        achievements["level2_complete"]["unlocked"] = True
        save_achievement("level2_complete", "Исследователь пещер", "Пройти второй уровень", True)
        if key_count >= 3:
            achievements["all_keys"]["unlocked"] = True
            save_achievement("all_keys", "Ключник", "Собрать все ключи на уровне", True)
    if death:
        achievements["died_mobs"]["unlocked"] = True
        save_achievement("died_mobs", "Неосторожность", "Умереть от врагов", True)

def save_level3_achievements(key_count=0, win=False, death=False):
    if win:
        achievements["level3_complete"]["unlocked"] = True
        save_achievement("level3_complete", "Властелин небес", "Пройти третий уровень", True)
        if key_count >= 3:
            achievements["all_keys"]["unlocked"] = True
            save_achievement("all_keys", "Ключник", "Собрать все ключи на уровне", True)
    if death:
        achievements["died_fall"]["unlocked"] = True
        save_achievement("died_fall", "Неудачный прыжок", "Умереть от падения на 3 уровне", True)


class LevelOne:
    def __init__(self):
        # Создаем игрока (x=100, y=200, размер 16×16, здоровье 100)
        self.player = Player(x=100, y=200, width=32, height=32, health=100)

        self.score = 0
        self.key_count = 0

        self.ghosts = [
            Ghost(x=500, y=177, left_bound=350, right_bound=550),
            Ghost(x=900, y=177, left_bound=850, right_bound=1100),
        ]

        self.tmx_data = pytmx.load_pygame("levels/1.tmx", pixelalpha=True)

        map_width_px = self.tmx_data.width * self.tmx_data.tilewidth
        map_height_px = self.tmx_data.height * self.tmx_data.tileheight

        self.scale_factor = HEIGHT / map_height_px
        self.map_width_scaled = int(map_width_px * self.scale_factor)
        self.map_height_scaled = HEIGHT

        temp_surface = pygame.Surface((map_width_px, map_height_px), pygame.SRCALPHA)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        temp_surface.blit(
                            tile_image,
                            (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        )
        self.map_surface = pygame.transform.scale(
            temp_surface,
            (self.map_width_scaled, self.map_height_scaled)
        )

        self.collision_objects = []
        collisions_layer = self.tmx_data.get_layer_by_name("Collisions1")
        if collisions_layer:
            for obj in collisions_layer:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.collision_objects.append(rect)

        self.death_objects = []
        death_layer = self.tmx_data.get_layer_by_name("death1")
        if death_layer:
            for obj in death_layer:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.death_objects.append(rect)

        self.win_objects = []
        win_layer = self.tmx_data.get_layer_by_name("win1")
        if win_layer:
            for obj in win_layer:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.win_objects.append(rect)

        appear_layer = self.tmx_data.get_layer_by_name("Appearing1")
        if appear_layer:
            for obj in appear_layer:
                # Ставим игрока в координаты из карты
                self.player.x = obj.x
                self.player.y = obj.y
                break

        self.key_width = 16
        self.key_height = 16
        self.keys = [
            pygame.Rect(400, 150, self.key_width, self.key_height),
            pygame.Rect(800, 200, self.key_width, self.key_height),
            pygame.Rect(1200, 170, self.key_width, self.key_height)
        ]

        self.camera_x = 0

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)
            screen.fill(GREY_TONE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            keys_pressed = pygame.key.get_pressed()
            self.player.handle_input(keys_pressed)

            self.player.update_physics(gravity=GRAVITY)

            for ghost in self.ghosts:
                ghost.update()

            # Коллизия привидений с игроком
            player_rect = self.player.get_rect()
            for ghost in self.ghosts:
                ghost_w = 44
                ghost_h = 30
                ghost_rect = pygame.Rect(ghost.x, ghost.y, ghost_w, ghost_h)

                if player_rect.colliderect(ghost_rect):
                    self.player.health -= 5

            # Коллизии с платформами
            for obj_rect in self.collision_objects:
                if player_rect.colliderect(obj_rect):
                    overlap_left = player_rect.right - obj_rect.left
                    overlap_right = obj_rect.right - player_rect.left
                    overlap_top = player_rect.bottom - obj_rect.top
                    overlap_bottom = obj_rect.bottom - player_rect.top

                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    # Сверху платформы
                    if min_overlap == overlap_top and self.player.vel_y > 0:
                        self.player.y = obj_rect.top - self.player.height
                        self.player.vel_y = 0
                        self.player.is_on_ground = True
                        self.player.reset_jumps()

                    # Снизу платформы
                    elif min_overlap == overlap_bottom and self.player.vel_y < 0:
                        self.player.y = obj_rect.bottom
                        self.player.vel_y = 0

                    # Слева
                    elif min_overlap == overlap_left:
                        self.player.x = obj_rect.left - self.player.width
                        self.player.vel_x = 0

                    # Справа
                    elif min_overlap == overlap_right:
                        self.player.x = obj_rect.right
                        self.player.vel_x = 0

            # Смертельные объекты
            for drect in self.death_objects:
                if player_rect.colliderect(drect):
                    self.player.health = 0

            # Объекты выигрыша
            for wrect in self.win_objects:
                if player_rect.colliderect(wrect):
                    save_level1_achievements(self.key_count, win=True)
                    draw_text("Уровень пройден!", WIDTH // 2 - 80, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return

            # Сбор ключей
            for k in self.keys[:]:
                if player_rect.colliderect(k):
                    self.keys.remove(k)
                    self.key_count += 1
                    self.score += 100

            # Камера
            camera_center = self.player.x * self.scale_factor
            self.camera_x = camera_center - (WIDTH // 2)
            if self.camera_x < 0:
                self.camera_x = 0
            if self.camera_x > self.map_width_scaled - WIDTH:
                self.camera_x = self.map_width_scaled - WIDTH

            # Рисуем карту
            screen.blit(self.map_surface, (-self.camera_x, 0))

            # Рисуем привидений
            for ghost in self.ghosts:
                ghost.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # Рисуем ключи
            for k in self.keys:
                screen_x = (k.x * self.scale_factor) - self.camera_x
                screen_y = k.y * self.scale_factor
                w = k.width * self.scale_factor
                h = k.height * self.scale_factor
                pygame.draw.rect(screen, PASTEL_YELLOW, (screen_x, screen_y, w, h))

            self.player.update_animation()
            self.player.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # Рисуем игрока
            self.player.draw(
                surface=screen,
                camera_x=self.camera_x,
                scale_factor=self.scale_factor,
            )

            # Вывод текста (HUD)
            draw_text("Уровень 1: Заброшенный замок", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.player.health}", 10, 70)
            draw_text(f"Ключи: {self.key_count}/3", 10, 100)

            # Проверка победы (3 ключа)
            if self.key_count >= 3:
                save_achievement("all_keys", "Ключник", "Собрать все ключи на уровне", True)
                save_achievement("level1_complete", "Покоритель замка", "Пройти первый уровень", True)
                draw_text("Уровень пройден (3 ключа)!", WIDTH // 2 - 100, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            # Проверка смерти
            if self.player.health <= 0:
                save_level1_achievements(death=True)
                draw_text("Игра окончена!", WIDTH // 2 - 60, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


class LevelTwo:
    def __init__(self):
        # Создаём игрока
        self.player = Player(x=100, y=200, width=32, height=32, health=100)

        self.score = 0
        self.key_count = 0

        # 1) Загружаем TMX-карту
        self.tmx_data = pytmx.load_pygame("levels/2.tmx", pixelalpha=True)

        # 2) Считаем размеры карты и масштаб
        map_width_px = self.tmx_data.width * self.tmx_data.tilewidth
        map_height_px = self.tmx_data.height * self.tmx_data.tileheight
        self.scale_factor = HEIGHT / map_height_px
        self.map_width_scaled = int(map_width_px * self.scale_factor)
        self.map_height_scaled = HEIGHT

        # 3) Рендерим все тайлы во временный Surface, потом масштабируем
        temp_surface = pygame.Surface((map_width_px, map_height_px), pygame.SRCALPHA)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        temp_surface.blit(tile_image, (x * self.tmx_data.tilewidth,
                                                       y * self.tmx_data.tileheight))
        self.map_surface = pygame.transform.scale(temp_surface,
                                                  (self.map_width_scaled, self.map_height_scaled))


        self.collision_objects = []
        self.death_objects = []
        self.win_objects = []
        self.bats = []

        collision_layer = self.tmx_data.get_layer_by_name("Collision 2")
        if collision_layer:
            for obj in collision_layer:
                name = obj.name
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

                if name == "ground2":
                    self.collision_objects.append(rect)
                elif name == "death2":
                    self.death_objects.append(rect)
                elif name == "winning2":
                    self.win_objects.append(rect)
                elif name == "appearing2":
                    self.player.x = obj.x
                    self.player.y = obj.y
                elif name == "bat":
                    # Координаты для летучей мыши
                    left_bound = obj.x - 100
                    right_bound = obj.x + 100
                    bat = Bat(x=obj.x, y=obj.y,
                              left_bound=left_bound,
                              right_bound=right_bound)
                    self.bats.append(bat)

        self.keys = [
            pygame.Rect(400, 150, 16, 16),
            pygame.Rect(800, 200, 16, 16),
            pygame.Rect(1200, 170, 16, 16)
        ]

        # Позиция камеры
        self.camera_x = 0

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)
            screen.fill((20, 15, 15))  # Фон подземелья

            # ОБРАБОТКА СОБЫТИЙ
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # УПРАВЛЕНИЕ И ФИЗИКА ИГРОКА
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_input(keys_pressed)
            self.player.update_physics(gravity=GRAVITY)

            player_rect = self.player.get_rect()

            # ОБНОВЛЯЕМ МЫШЕЙ
            for bat in self.bats:
                bat.update()
                # Проверяем столкновение с игроком
                bat_rect = pygame.Rect(bat.x, bat.y, 46, 30)
                if player_rect.colliderect(bat_rect):
                    self.player.health -= 2

            # КОЛЛИЗИИ С ПЛАТФОРМАМИ
            for obj_rect in self.collision_objects:
                if player_rect.colliderect(obj_rect):
                    overlap_left = player_rect.right - obj_rect.left
                    overlap_right = obj_rect.right - player_rect.left
                    overlap_top = player_rect.bottom - obj_rect.top
                    overlap_bottom = obj_rect.bottom - player_rect.top

                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    # Сверху платформы
                    if min_overlap == overlap_top and self.player.vel_y > 0:
                        self.player.y = obj_rect.top - self.player.height
                        self.player.vel_y = 0
                        self.player.is_on_ground = True
                        self.player.reset_jumps()

                    # Снизу платформы
                    elif min_overlap == overlap_bottom and self.player.vel_y < 0:
                        self.player.y = obj_rect.bottom
                        self.player.vel_y = 0

                    # Слева
                    elif min_overlap == overlap_left:
                        self.player.x = obj_rect.left - self.player.width
                        self.player.vel_x = 0

                    # Справа
                    elif min_overlap == overlap_right:
                        self.player.x = obj_rect.right
                        self.player.vel_x = 0

            # СМЕРТЕЛЬНЫЕ ОБЪЕКТЫ
            for drect in self.death_objects:
                if player_rect.colliderect(drect):
                    self.player.health = 0

            # ОБЪЕКТЫ ВЫИГРЫША
            for wrect in self.win_objects:
                if player_rect.colliderect(wrect):
                    save_achievement("level2_complete", "Исследователь пещер", "Пройти второй уровень", True)
                    draw_text("Уровень 2 пройден!", WIDTH // 2 - 60, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return

            # СБОР КЛЮЧЕЙ
            for k in self.keys[:]:
                if player_rect.colliderect(k):
                    self.keys.remove(k)
                    self.key_count += 1
                    self.score += 100

            # КАМЕРА
            camera_center = self.player.x * self.scale_factor
            self.camera_x = camera_center - (WIDTH // 2)
            if self.camera_x < 0:
                self.camera_x = 0
            if self.camera_x > self.map_width_scaled - WIDTH:
                self.camera_x = self.map_width_scaled - WIDTH

            # РИСУЕМ КАРТУ
            screen.blit(self.map_surface, (-self.camera_x, 0))

            # РИСУЕМ МЫШЕЙ
            for bat in self.bats:
                bat.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # РИСУЕМ КЛЮЧИ
            for k in self.keys:
                screen_x = (k.x * self.scale_factor) - self.camera_x
                screen_y = k.y * self.scale_factor
                w = k.width * self.scale_factor
                h = k.height * self.scale_factor
                pygame.draw.rect(screen, PASTEL_YELLOW, (screen_x, screen_y, w, h))

            # АНИМАЦИЯ ИГРОКА
            self.player.update_animation()
            self.player.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # HUD
            draw_text("Уровень 2: Подземная пещера", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.player.health}", 10, 70)
            draw_text(f"Ключи: {self.key_count}/3", 10, 100)

            # Проверка смерти
            if self.player.health <= 0:
                save_level2_achievements(death=True)
                draw_text("Игра окончена!", WIDTH // 2 - 60, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


class LevelThree:
    def __init__(self):
        # Создаём игрока (координаты уточним из appearing3)
        self.player = Player(x=100, y=200, width=32, height=32, health=100)

        self.score = 0
        self.key_count = 0

        # Загружаем карту "3.tmx"
        self.tmx_data = pytmx.load_pygame("levels/3.tmx", pixelalpha=True)

        # Определяем размеры карты и масштаб
        map_width_px = self.tmx_data.width * self.tmx_data.tilewidth  # 400 * 16 = 6400
        map_height_px = self.tmx_data.height * self.tmx_data.tileheight  # 24  * 16 = 384

        # Масштабируем карту по высоте, чтобы занимала весь экран
        self.scale_factor = HEIGHT / map_height_px  # ~1.5625
        self.map_width_scaled = int(map_width_px * self.scale_factor)
        self.map_height_scaled = int(map_height_px * self.scale_factor)  # ≈ 600

        # Рендерим тайлы в Surface и масштабируем
        temp_surface = pygame.Surface((map_width_px, map_height_px), pygame.SRCALPHA)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        temp_surface.blit(
                            tile_image,
                            (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        )
        self.map_surface = pygame.transform.scale(temp_surface,
                                                  (self.map_width_scaled, self.map_height_scaled))

        # Собираем объекты
        self.collision_objects = []
        self.death_objects = []
        self.win_objects = []
        self.birds = []

        collision_layer = self.tmx_data.get_layer_by_name("Collisions 3")
        if collision_layer:
            for obj in collision_layer:
                name = obj.name  # "ground3", "death3", "winning3", "bird", "appearing3" и т.д.
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

                if name == "ground3":
                    self.collision_objects.append(rect)
                elif name == "death3":
                    self.death_objects.append(rect)
                elif name == "winning3":
                    self.win_objects.append(rect)
                elif name == "appearing3":
                    # Точка появления игрока
                    self.player.x = obj.x
                    self.player.y = obj.y
                elif name == "bird":

                    left_bound = obj.x - 100
                    right_bound = obj.x + 100
                    b = Bird(obj.x, obj.y, left_bound, right_bound)
                    self.birds.append(b)

        # Камера (горизонтальный сдвиг в пикселях экрана)
        self.camera_x = 0

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)
            screen.fill(CLOUD_COLOR)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Управление + физика игрока
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_input(keys_pressed)
            self.player.update_physics(gravity=GRAVITY)

            # Коллизии
            player_rect = self.player.get_rect()

            # 1) Птицы
            for bird in self.birds:
                bird.update()
                # Проверка столкновения с игроком

                bird_rect = pygame.Rect(bird.x, bird.y, 32, 32)
                if player_rect.colliderect(bird_rect):
                    self.player.health -= 3

            # 2) Платформы (ground3)
            for rect_obj in self.collision_objects:
                if player_rect.colliderect(rect_obj):
                    overlap_left = player_rect.right - rect_obj.left
                    overlap_right = rect_obj.right - player_rect.left
                    overlap_top = player_rect.bottom - rect_obj.top
                    overlap_bottom = rect_obj.bottom - player_rect.top
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    # Сверху платформы
                    if min_overlap == overlap_top and self.player.vel_y > 0:
                        self.player.y = rect_obj.top - self.player.height
                        self.player.vel_y = 0
                        self.player.is_on_ground = True
                        self.player.reset_jumps()
                    # Снизу
                    elif min_overlap == overlap_bottom and self.player.vel_y < 0:
                        self.player.y = rect_obj.bottom
                        self.player.vel_y = 0
                    # Слева
                    elif min_overlap == overlap_left:
                        self.player.x = rect_obj.left - self.player.width
                        self.player.vel_x = 0
                    # Справа
                    elif min_overlap == overlap_right:
                        self.player.x = rect_obj.right
                        self.player.vel_x = 0

            # 3) Смертельные объекты (death3)
            for drect in self.death_objects:
                if player_rect.colliderect(drect):
                    self.player.health = 0

            # 4) Выигрыш (winning3)
            for wrect in self.win_objects:
                if player_rect.colliderect(wrect):
                    save_achievement("level3_complete", "Властелин небес", "Пройти третий уровень", True)
                    draw_text("Уровень 3 пройден!", WIDTH // 2 - 80, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return

            # Камера
            camera_center = self.player.x * self.scale_factor
            self.camera_x = camera_center - (WIDTH // 2)
            # Не даёт камере "уехать" за край
            if self.camera_x < 0:
                self.camera_x = 0
            if self.camera_x > self.map_width_scaled - WIDTH:
                self.camera_x = self.map_width_scaled - WIDTH

            # Рисуем карту
            screen.blit(self.map_surface, (-self.camera_x, 0))

            # Рисуем птиц
            for bird in self.birds:
                bird.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # Обновляем анимацию игрока и рисуем
            self.player.update_animation()
            self.player.draw(screen, camera_x=self.camera_x, scale_factor=self.scale_factor)

            # HUD
            draw_text("Уровень 3: Небесные острова", 10, 10)
            draw_text(f"Очки: {self.score}", 10, 40)
            draw_text(f"Здоровье: {self.player.health}", 10, 70)


            # Проверка смерти
            if self.player.health <= 0:
                save_level3_achievements(death=True)
                draw_text("Игра окончена!", WIDTH // 2 - 60, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                return

            pygame.display.flip()


# ------------------------
# ЗАПУСК ВСЕЙ ИГРЫ
# ------------------------
if __name__ == "__main__":
    MainMenu().run()
