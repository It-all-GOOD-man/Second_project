import pygame
import random


class Food:
    def __init__(self, grid_size, color='red'):
        self.grid_size = grid_size
        self.color = self._get_color(color)
        self.position = (0, 0)
        self.randomize_position()

    def _get_color(self, color_name):
        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128)
        }
        return colors.get(color_name, (255, 0, 0))

    def randomize_position(self, snake_positions=None, screen_width=800, screen_height=600):
        if snake_positions is None:
            snake_positions = []

        while True:
            x = random.randint(0, (screen_width - self.grid_size) // self.grid_size) * self.grid_size
            y = random.randint(0, (screen_height - self.grid_size) // self.grid_size) * self.grid_size
            self.position = (x, y)

            if self.position not in snake_positions:
                break

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (self.grid_size, self.grid_size))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

        # Рисую внутренний круг для еды
        inner_rect = pygame.Rect(
            (self.position[0] + self.grid_size // 4, self.position[1] + self.grid_size // 4),
            (self.grid_size // 2, self.grid_size // 2)
        )
        pygame.draw.ellipse(surface, (255, 255, 255), inner_rect)
