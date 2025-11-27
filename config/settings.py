import argparse


class GameSettings:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Snake Game')
        self._setup_arguments()
        self.args = self.parser.parse_args()

    def _setup_arguments(self):
        self.parser.add_argument('--speed', type=int, default=10,
                                 help='Snake speed (1-20), default: 10')
        self.parser.add_argument('--wall-pass', action='store_true',
                                 help='Allow passing through walls')
        self.parser.add_argument('--snake-color', type=str, default='green',
                                 choices=['green', 'blue', 'red', 'yellow', 'purple'],
                                 help='Snake color')
        self.parser.add_argument('--food-color', type=str, default='red',
                                 choices=['red', 'green', 'blue', 'yellow', 'purple'],
                                 help='Food color')
        self.parser.add_argument('--grid-size', type=int, default=20,
                                 help='Grid cell size in pixels')
        self.parser.add_argument('--width', type=int, default=800,
                                 help='Window width')
        self.parser.add_argument('--height', type=int, default=600,
                                 help='Window height')
        self.parser.add_argument('--player-name', type=str, default='Player',
                                 help='Player name for high scores')


    def get_settings(self):
        return {
            'speed': self.args.speed,
            'wall_pass': self.args.wall_pass,
            'snake_color': self.args.snake_color,
            'food_color': self.args.food_color,
            'grid_size': self.args.grid_size,
            'width': self.args.width,
            'height': self.args.height,
            'player_name': self.args.player_name
        }