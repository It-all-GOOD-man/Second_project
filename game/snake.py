"""
Модуль класса Змейки.

Содержит логику движения, отрисовки и управления змейкой.
"""

import pygame


class Snake:
    """
    Класс, представляющий змейку в игре.

    Attributes:
        grid_size (int): Размер клетки сетки
        color (tuple): Цвет змейки в формате RGB
        positions (list): Список позиций сегментов змейки
        direction (tuple): Текущее направление движения
        score (int): Текущий счет
        grow_to (int): Целевая длина для роста
    """

    def __init__(self, grid_size, color='green'):
        """
        Инициализирует змейку.

        Args:
            grid_size (int): Размер клетки сетки
            color (str): Название цвета змейки
        """
        self.grid_size = grid_size
        self.color = self._get_color(color)
        self.reset()

    def _get_color(self, color_name):
        """
        Преобразует название цвета в RGB значения.

        Args:
            color_name (str): Название цвета

        Returns:
            tuple: RGB значения цвета
        """
        colors = {
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128)
        }
        return colors.get(color_name, (0, 255, 0))

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние.
        """
        self.length = 3
        self.positions = [(self.grid_size * 5, self.grid_size * 5)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i * self.grid_size, self.positions[0][1]))
        self.direction = (self.grid_size, 0)  # Начальное направление: вправо
        self.score = 0
        self.grow_to = 3

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Returns:
            tuple: Координаты (x, y) головы змейки
        """
        return self.positions[0]

    def turn(self, point):
        """
        Изменяет направление движения змейки.

        Args:
            point (tuple): Новое направление (dx, dy)
        """
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self, wall_pass=False, screen_width=0, screen_height=0):
        """
        Перемещает змейку в текущем направлении.

        Args:
            wall_pass (bool): Разрешить прохождение сквозь стены
            screen_width (int): Ширина экрана
            screen_height (int): Высота экрана

        Returns:
            bool: False если произошло столкновение с собой, иначе True
        """
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x)
        new_y = (head[1] + y)

        # Обработка прохождения через стены
        if wall_pass:
            if new_x >= screen_width:
                new_x = 0
            elif new_x < 0:
                new_x = screen_width - self.grid_size
            if new_y >= screen_height:
                new_y = 0
            elif new_y < 0:
                new_y = screen_height - self.grid_size

        new_position = (new_x, new_y)

        # Проверка на столкновение с собой
        if new_position in self.positions[1:]:
            return False

        self.positions.insert(0, new_position)
        if len(self.positions) > self.grow_to:
            self.positions.pop()

        return True

    def grow(self):
        """
        Увеличивает длину змейки и добавляет очки.
        """
        self.grow_to += 1
        self.score += 10

    def draw(self, surface):
        """
        Отрисовывает змейку на поверхности.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        for i, p in enumerate(self.positions):
            # Градиент цвета для змейки
            color_factor = max(0.5, i / len(self.positions))
            color = (
                int(self.color[0] * color_factor),
                int(self.color[1] * color_factor),
                int(self.color[2] * color_factor)
            )

            rect = pygame.Rect((p[0], p[1]), (self.grid_size, self.grid_size))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

    def get_length(self):
        """
        Возвращает текущую длину змейки.

        Returns:
            int: Количество сегментов змейки
        """
        return len(self.positions)