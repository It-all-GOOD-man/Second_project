import pygame
import sys


class Menu:
    def __init__(self, screen, db_handler, default_player_name="Player"):
        self.screen = screen
        self.db_handler = db_handler
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "High Scores", "Exit"]
        self.player_name = default_player_name  # Используем имя из аргументов
        self.name_input_active = False

    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))

        # Заголовок
        title = self.font_large.render("SNAKE GAME", True, (0, 255, 0))
        title_rect = title.get_rect(center=(400, 100))
        self.screen.blit(title, title_rect)

        # Имя игрока
        name_color = (255, 255, 0) if self.name_input_active else (255, 255, 255)
        name_text = self.font_small.render(f"Player: {self.player_name}", True, name_color)
        name_rect = name_text.get_rect(center=(400, 180))
        self.screen.blit(name_text, name_rect)

        if self.name_input_active:
            hint_text = self.font_small.render("Type your name and press ENTER", True, (128, 128, 255))
            hint_rect = hint_text.get_rect(center=(400, 220))
            self.screen.blit(hint_text, hint_rect)

        # Опции меню
        for i, option in enumerate(self.options):
            color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(400, 280 + i * 60))
            self.screen.blit(text, text_rect)

        # Управление
        controls_text = "Use ARROW KEYS to navigate, ENTER to select, N to change name"
        controls = self.font_small.render(controls_text, True, (128, 128, 128))
        controls_rect = controls.get_rect(center=(400, 500))
        self.screen.blit(controls, controls_rect)

        pygame.display.flip()

    def draw_high_scores(self):
        self.screen.fill((0, 0, 0))

        # Заголовок
        title = self.font_large.render("HIGH SCORES", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 80))
        self.screen.blit(title, title_rect)

        # Получаем рекорды из базы данных
        high_scores = self.db_handler.get_high_scores(10)

        if not high_scores:
            no_scores = self.font_medium.render("No games played yet!", True, (255, 255, 255))
            no_scores_rect = no_scores.get_rect(center=(400, 200))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            for i, (player, score, duration, date) in enumerate(high_scores):
                score_text = f"{i + 1}. {player}: {score} pts - {duration}s"
                text = self.font_small.render(score_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 150 + i * 40))
                self.screen.blit(text, text_rect)

        # Кнопка возврата
        back_text = self.font_medium.render("Press ESC to return", True, (128, 128, 128))
        back_rect = back_text.get_rect(center=(400, 550))
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def handle_name_input(self, event):
        if event.key == pygame.K_RETURN:
            self.name_input_active = False
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        else:
            if len(self.player_name) < 15 and event.unicode.isalnum():
                self.player_name += event.unicode

    def run(self):
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