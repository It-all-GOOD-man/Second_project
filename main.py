import pygame
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))

from config.settings import GameSettings
from database.db_handler import DatabaseHandler
from game.menu import Menu
from game.game_logic import GameLogic


def main():

    pygame.init()

    try:
 
        settings_manager = GameSettings()
        settings = settings_manager.get_settings()


        db_handler = DatabaseHandler() 


        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Snake Game')

  
        while True:
        
            menu = Menu(screen, db_handler, settings['player_name'])
            player_name, start_game = menu.run()

            if not start_game:
                break

            game = GameLogic(settings, db_handler)
            continue_playing = game.run(player_name)

            if not continue_playing:
                break

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()

    finally:

        if 'db_handler' in locals():
            db_handler.close()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()