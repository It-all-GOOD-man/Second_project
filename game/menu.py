"""
Модуль игрового меню.

Содержит логику отображения и управления главным меню и таблицей рекордов.
"""

import pygame
import sys


class Menu:
    """
    Класс для управления игровым меню.

    Attributes:
        screen: Поверхность Pygame для отрисовки
        db_handler: Обработчик базы данных
        font_large: Шрифт для крупного текста
        font_medium: Шрифт для среднего текста
        font_small: Шрифт для мелкого текста
        selected_option (int): Индекс выбранной опции меню
        options (list): Список доступных опций меню
        player_name (str): Текущее имя игрока
        name_input_active (bool): Флаг активности ввода имени
    """

    def __init__(self, screen, db_handler, default_player_name="Player"):
        """
        Инициализирует меню.

        Args:
            screen: Поверхность Pygame для отрисовки
            db_handler: Обработчик базы данных
            default_player_name (str): Имя игрока по умолчанию
        """
        self.screen = screen
        self.db_handler = db_handler

        # Получаем размеры экрана
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Используем адаптивные размеры шрифтов
        self.font_large = pygame.font.Font(None, int(self.screen_height * 0.1))    # 10% высоты
        self.font_medium = pygame.font.Font(None, int(self.screen_height * 0.06))  # 6% высоты
        self.font_small = pygame.font.Font(None, int(self.screen_height * 0.04))   # 4% высоты

        self.selected_option = 0
        self.options = ["Start Game", "High Scores", "Exit"]
        self.player_name = default_player_name  # Используем имя из аргументов
        self.name_input_active = False

    def draw_main_menu(self):
        """Отрисовывает главное меню."""
        self.screen.fill((0, 0, 0))

        # Центр экрана
        center_x = self.screen_width // 2

        # Заголовок (10% от верха экрана)
        title = self.font_large.render("SNAKE GAME", True, (0, 255, 0))
        title_rect = title.get_rect(center=(center_x, self.screen_height * 0.15))
        self.screen.blit(title, title_rect)

        # Имя игрока (25% от верха экрана)
        name_color = (255, 255, 0) if self.name_input_active else (255, 255, 255)
        name_text = self.font_small.render(f"Player: {self.player_name}", True, name_color)
        name_rect = name_text.get_rect(center=(center_x, self.screen_height * 0.25))
        self.screen.blit(name_text, name_rect)

        if self.name_input_active:
            hint_text = self.font_small.render("Type your name and press ENTER", True, (128, 128, 255))
            hint_rect = hint_text.get_rect(center=(center_x, self.screen_height * 0.30))
            self.screen.blit(hint_text, hint_rect)

        # Опции меню (начинаем с 40% от верха экрана)
        option_start_y = self.screen_height * 0.40
        option_spacing = self.screen_height * 0.10  # 10% высоты между опциями

        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(center_x, option_start_y + i * option_spacing))
            self.screen.blit(text, text_rect)

        # Управление (85% от верха экрана)
        controls_text = "Use ARROW KEYS to navigate, ENTER to select, N to change name"
        controls = self.font_small.render(controls_text, True, (128, 128, 128))
        controls_rect = controls.get_rect(center=(center_x, self.screen_height * 0.85))
        self.screen.blit(controls, controls_rect)

        pygame.display.flip()

    def draw_high_scores(self):
        """Отрисовывает экран с таблицей рекордов."""
        self.screen.fill((0, 0, 0))

        # Центр экрана
        center_x = self.screen_width // 2

        # Заголовок
        title = self.font_large.render("HIGH SCORES", True, (255, 215, 0))
        title_rect = title.get_rect(center=(center_x, self.screen_height * 0.10))
        self.screen.blit(title, title_rect)

        # Получаем рекорды из базы данных
        high_scores = self.db_handler.get_high_scores(10)

        if not high_scores:
            no_scores = self.font_medium.render("No games played yet!", True, (255, 255, 255))
            no_scores_rect = no_scores.get_rect(center=(center_x, self.screen_height * 0.30))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            start_y = self.screen_height * 0.20
            row_spacing = self.screen_height * 0.06

            for i, (player, score, duration, date) in enumerate(high_scores):
                score_text = f"{i + 1}. {player}: {score} pts - {duration}s"
                text = self.font_small.render(score_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(center_x, start_y + i * row_spacing))
                self.screen.blit(text, text_rect)

        # Кнопка возврата (90% от верха экрана)
        back_text = self.font_medium.render("Press ESC to return", True, (128, 128, 128))
        back_rect = back_text.get_rect(center=(center_x, self.screen_height * 0.90))
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def handle_name_input(self, event):
        """
        Обрабатывает ввод имени игрока.

        Args:
            event: Событие клавиатуры Pygame
        """
        if event.key == pygame.K_RETURN:
            self.name_input_active = False
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        else:
            if len(self.player_name) < 15 and event.unicode.isalnum():
                self.player_name += event.unicode

    def run(self):
        """
        Запускает главный цикл меню.

        Returns:
            tuple: (player_name, game_started) где:
                player_name (str): Имя игрока
                game_started (bool): Флаг начала игры
        """
        running = True
        game_started = False
        show_high_scores = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None, False

                if self.name_input_active:
                    if event.type == pygame.KEYDOWN:
                        self.handle_name_input(event)
                    continue

                if event.type == pygame.KEYDOWN:
                    if show_high_scores:
                        if event.key == pygame.K_ESCAPE:
                            show_high_scores = False

                    else:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:  # Start Game
                                game_started = True
                                running = False
                            elif self.selected_option == 1:  # High Scores
                                show_high_scores = True
                            elif self.selected_option == 2:  # Exit
                                running = False
                                return None, False
                        elif event.key == pygame.K_n:
                            self.name_input_active = True

            if show_high_scores:
                self.draw_high_scores()
            else:
                self.draw_main_menu()

        return self.player_name, game_started