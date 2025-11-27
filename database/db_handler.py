import psycopg2
from datetime import datetime
import json


class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'snake_game',
            'user': 'postgres',
            'password': '1111' 
        }
        self.connect()
        if self.connection:
            self.create_tables()

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Автоподключение к PostgreSQL успешно!")
        except Exception as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            self.connection = None

    def create_tables(self):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()


            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_name VARCHAR(100) NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    score INTEGER DEFAULT 0,
                    game_duration INTEGER,
                    settings JSONB
                )
            ''')


            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_stats (
                    id SERIAL PRIMARY KEY,
                    session_id INTEGER REFERENCES game_sessions(id),
                    food_eaten INTEGER DEFAULT 0,
                    max_length INTEGER DEFAULT 0,
                    walls_passed BOOLEAN DEFAULT FALSE,
                    final_score INTEGER DEFAULT 0
                )
            ''')

            self.connection.commit()
            cursor.close()
            print("✅ Таблицы PostgreSQL созданы/проверены")

        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")

    def save_game_session(self, player_name, score, game_duration, settings, food_eaten, max_length, walls_passed):
        if not self.connection:
            print("❌ Нет подключения к БД")
            return None

        try:
            cursor = self.connection.cursor()


            cursor.execute('''
                INSERT INTO game_sessions (player_name, start_time, end_time, score, game_duration, settings)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (player_name, datetime.now(), datetime.now(), score, game_duration, json.dumps(settings)))

            session_id = cursor.fetchone()[0]


            cursor.execute('''
                INSERT INTO game_stats (session_id, food_eaten, max_length, walls_passed, final_score)
                VALUES (%s, %s, %s, %s, %s)
            ''', (session_id, food_eaten, max_length, walls_passed, score))

            self.connection.commit()
            cursor.close()
            print(f"✅ Игра сохранена в PostgreSQL. Игрок: {player_name}, Счет: {score}")
            return session_id

        except Exception as e:
            print(f"❌ Ошибка сохранения игры: {e}")
            return None

    def get_high_scores(self, limit=10):
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT player_name, score, game_duration, end_time
                FROM game_sessions
                ORDER BY score DESC
                LIMIT %s
            ''', (limit,))

            results = cursor.fetchall()
            cursor.close()
            return results

        except Exception as e:
            print(f"❌ Ошибка получения рекордов: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print("✅ Подключение к PostgreSQL закрыто")