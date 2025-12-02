"""
Модуль основной игровой логики.

Содержит главный игровой цикл, обработку событий и отрисовку игры.
"""

import pygame
import time
from .snake import Snake
from .food import Food


class GameLogic:
    """
    Класс основной игровой логики.

    Управляет игровым процессом, обработкой событий, обновлением состояния
    и отрисовкой игры.

    Attributes:
        settings (dict): Настройки игры
        db_handler: Обработчик базы данных
        screen_width (int): Ширина экрана
        screen_height (int): Высота экрана
        grid_size (int): Размер клетки сетки
        snake (Snake): Объект змейки
        food (Food): Объект еды
    """

    def __init__(self, settings, db_handler):
        """
        Инициализирует игровую логику.

        Args:
            settings (dict): Словарь с настройками игры
            db_handler: Объект для работы с базой данных
        """
        self.settings = settings
        self.db_handler = db_handler
        self.screen_width = settings['width']
        self.screen_height = settings['height']
        self.grid_size = settings['grid_size']

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()
        self.snake = Snake(self.grid_size, settings['snake_color'])
        self.food = Food(self.grid_size, settings['food_color'])
        self.food.randomize_position(self.snake.positions, self.screen_width, self.screen_height)

        self.font = pygame.font.Font(None, 36)
        self.start_time = time.time()
        self.food_eaten = 0
        self.max_length = 3

    def handle_events(self):
        """
        Обрабатывает события Pygame.

        Returns:
            bool: False если игра должна завершиться, иначе True
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.turn((0, -self.grid_size))
                elif event.key == pygame.K_DOWN:
                    self.snake.turn((0, self.grid_size))
                elif event.key == pygame.K_LEFT:
                    self.snake.turn((-self.grid_size, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn((self.grid_size, 0))
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        """
        Обновляет игровое состояние.

        Returns:
            bool: False если игра окончена, иначе True
        """
        # Движение змейки
        if not self.snake.move(self.settings['wall_pass'], self.screen_width, self.screen_height):
            return False  # Game over

        # Проверка столкновения со стенами (если wall_pass=False)
        head = self.snake.get_head_position()
        if not self.settings['wall_pass']:
            if (head[0] < 0 or head[0] >= self.screen_width or
                    head[1] < 0 or head[1] >= self.screen_height):
                return False  # Game over

        # Проверка поедания еды
        if head == self.food.position:
            self.snake.grow()
            self.food_eaten += 1
            self.food.randomize_position(self.snake.positions, self.screen_width, self.screen_height)

            # Обновляем максимальную длину
            current_length = self.snake.get_length()
            if current_length > self.max_length:
                self.max_length = current_length

        return True

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Рисуем сетку
        for x in range(0, self.screen_width, self.grid_size):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.grid_size):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.screen_width, y))

        # Рисуем змейку и еду
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Динамический размер шрифта в зависимости от разрешения
        base_font_size = max(24, int(min(self.screen_width, self.screen_height) * 0.02))
        font = pygame.font.Font(None, base_font_size)


        score_text = font.render(f'Score: {self.snake.score}', True, (255, 255, 255))

        # Отступ рассчитываем как процент от ширины экрана
        padding_x = max(20, int(self.screen_width * 0.02))  # Минимум 20px или 2% ширины
        padding_y = max(10, int(self.screen_height * 0.02))  # Минимум 10px или 2% высоты

        # Позиции текста с отступами
        self.screen.blit(score_text, (padding_x, padding_y))

        # Отображаем длину змейки
        length_text = font.render(f'Length: {self.snake.get_length()}', True, (255, 255, 255))
        self.screen.blit(length_text, (padding_x, padding_y + base_font_size + 5))

        # Отображаем время игры
        game_time = int(time.time() - self.start_time)
        time_text = font.render(f'Time: {game_time}s', True, (255, 255, 255))
        self.screen.blit(time_text, (padding_x, padding_y + (base_font_size + 5) * 2))


        if self.settings['wall_pass']:
            wall_text = font.render('Wall Pass: ON', True, (255, 100, 100))
            self.screen.blit(wall_text, (padding_x, padding_y + (base_font_size + 5) * 4))

        pygame.display.flip()

    def show_game_over(self, player_name):
        """
        Показывает экран завершения игры и сохраняет результаты.

        Args:
            player_name (str): Имя игрока

        Returns:
            bool: True если игра должна продолжиться, False для выхода
        """
        game_duration = int(time.time() - self.start_time)

        # Сохраняем результаты в базу данных
        settings_data = {
            'speed': self.settings['speed'],
            'wall_pass': self.settings['wall_pass'],
            'snake_color': self.settings['snake_color'],
            'food_color': self.settings['food_color']
        }

        self.db_handler.save_game_session(
            player_name=player_name,
            score=self.snake.score,
            game_duration=game_duration,
            settings=settings_data,
            food_eaten=self.food_eaten,
            max_length=self.max_length,
            walls_passed=self.settings['wall_pass']
        )

        # Отображаем экран завершения игры
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 74)
        font_medium = pygame.font.Font(None, 48)

        game_over = font_large.render('GAME OVER', True, (255, 0, 0))
        score_text = font_medium.render(f'Final Score: {self.snake.score}', True, (255, 255, 255))
        length_text = font_medium.render(f'Max Length: {self.max_length}', True, (255, 255, 255))
        time_text = font_medium.render(f'Time: {game_duration}s', True, (255, 255, 255))
        continue_text = font_medium.render('Press ENTER to continue', True, (128, 128, 128))

        self.screen.blit(game_over, (self.screen_width // 2 - game_over.get_width() // 2, 150))
        self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 250))
        self.screen.blit(length_text, (self.screen_width // 2 - length_text.get_width() // 2, 300))
        self.screen.blit(time_text, (self.screen_width // 2 - time_text.get_width() // 2, 350))
        self.screen.blit(continue_text, (self.screen_width // 2 - continue_text.get_width() // 2, 450))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        return False
            self.clock.tick(30)

    def run(self, player_name):
        """
        Запускает главный игровой цикл.

        Args:
            player_name (str): Имя игрока

        Returns:
            bool: True если игра должна продолжиться с новым раундом, False для выхода в меню
        """
        running = True
        game_active = True

        while running:
            if game_active:
                running = self.handle_events()
                if running:
                    game_active = self.update()
                    self.draw()
                    self.clock.tick(self.settings['speed'])
            else:
                # Игра завершена
                continue_game = self.show_game_over(player_name)
                return continue_game

        return False
