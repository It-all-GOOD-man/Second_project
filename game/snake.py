import pygame


class Snake:
    def __init__(self, grid_size, color='green'):
        self.grid_size = grid_size
        self.color = self._get_color(color)
        self.reset()

    def _get_color(self, color_name):
        colors = {
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128)
        }
        return colors.get(color_name, (0, 255, 0))

    def reset(self):
        self.length = 3
        self.positions = [(self.grid_size * 5, self.grid_size * 5)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i * self.grid_size, self.positions[0][1]))
        self.direction = (self.grid_size, 0)
        self.score = 0
        self.grow_to = 3

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point

    def move(self, wall_pass=False, screen_width=0, screen_height=0):
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
        self.grow_to += 1
        self.score += 10

    def draw(self, surface):
        for i, p in enumerate(self.positions):
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
        return len(self.positions)