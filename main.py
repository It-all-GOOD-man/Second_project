"""
Главный модуль игры Змейка.

Запускает игру, инициализирует настройки, базу данных и управляет основным игровым циклом.
"""

import pygame
import sys
import os

# Добавляем пути к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from config.settings import GameSettings
from database.db_handler import DatabaseHandler
from game.menu import Menu
from game.game_logic import GameLogic


def main():
    """
    Главная функция, запускающая игру.

    Инициализирует Pygame, загружает настройки, создает подключение к БД
    и управляет основным игровым циклом (меню → игра → завершение).
    """
    # Инициализация Pygame
    pygame.init()

    try:
        # Загрузка настроек из аргументов командной строки (только игровые)
        settings_manager = GameSettings()
        settings = settings_manager.get_settings()

        # АВТОМАТИЧЕСКОЕ подключение к PostgreSQL БЕЗ параметров
        db_handler = DatabaseHandler()  # Убрали db_config

        # Создание экрана для меню
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Snake Game')

        # Главный игровой цикл
        while True:
            # Показываем меню с именем игрока из аргументов
            menu = Menu(screen, db_handler, settings['player_name'])
            player_name, start_game = menu.run()

            if not start_game:
                break

            # Запускаем игру
            game = GameLogic(settings, db_handler)
            continue_playing = game.run(player_name)

            if not continue_playing:
                break

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Завершение работы
        if 'db_handler' in locals():
            db_handler.close()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()