"""
Модуль класса Еды.

Содержит логику генерации и отрисовки еды для змейки.
"""

import pygame
import random


class Food:
    """
    Класс, представляющий еду в игре.

    Attributes:
        grid_size (int): Размер клетки сетки
        color (tuple): Цвет еды в формате RGB
        position (tuple): Текущая позиция еды
    """

    def __init__(self, grid_size, color='red'):
        """
        Инициализирует еду.

        Args:
            grid_size (int): Размер клетки сетки
            color (str): Название цвета еды
        """
        self.grid_size = grid_size
        self.color = self._get_color(color)
        self.position = (0, 0)
        self.randomize_position()

    def _get_color(self, color_name):
        """
        Преобразует название цвета в RGB значения.

        Args:
            color_name (str): Название цвета

        Returns:
            tuple: RGB значения цвета
        """
        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128)
        }
        return colors.get(color_name, (255, 0, 0))

    def randomize_position(self, snake_positions=None, screen_width=800, screen_height=600):
        """
        Случайным образом размещает еду на поле.

        Args:
            snake_positions (list): Список позиций змейки для избежания пересечения
            screen_width (int): Ширина экрана
            screen_height (int): Высота экрана
        """
        if snake_positions is None:
            snake_positions = []

        while True:
            x = random.randint(0, (screen_width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(0, (screen_height - self.grid_size) // self.grid_size) * self.grid_size
            self.position = (x, y)

            if self.position not in snake_positions:
                break

    def draw(self, surface):
        """
        Отрисовывает еду на поверхности.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect((self.position[0], self.position[1]), (self.grid_size, self.grid_size))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

        # Рисуем внутренний круг для еды
        inner_rect = pygame.Rect(
            (self.position[0] + self.grid_size // 4, self.position[1] + self.grid_size // 4),
            (self.grid_size // 2, self.grid_size // 2)
        )
        pygame.draw.ellipse(surface, (255, 255, 255), inner_rect)