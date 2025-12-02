"""
Модуль для работы с базой данных PostgreSQL.

Обеспечивает подключение к БД, создание таблиц, сохранение игровых сессий
и получение рекордов.
"""

import psycopg2
from datetime import datetime
import json


class DatabaseHandler:
    """
    Класс для управления подключением и операциями с базой данных.

    Attributes:
        connection: Подключение к PostgreSQL
        db_config (dict): Конфигурация подключения к БД
    """

    def __init__(self):
        """
        Инициализирует подключение к БД и создает таблицы.
        """
        self.connection = None
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'dbname': 'snake_game',
            'user': 'postgres',
            'password': 'admin'  # ваш пароль
        }
        self.connect()
        if self.connection:
            self.create_tables()

    def connect(self):
        """
        Устанавливает подключение к PostgreSQL.

        Prints:
            Сообщение об успешном подключении или ошибке.
        """
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Автоподключение к PostgreSQL успешно!")
        except Exception as e:
            print(f"❌ Ошибка подключения к PostgreSQL: {e}")
            self.connection = None

    def create_tables(self):
        """
        Создает необходимые таблицы в БД если они не существуют.

        Создает таблицы:
            - game_sessions: для хранения игровых сессий
            - game_stats: для хранения статистики игр
        """
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()

            # Таблица для хранения игровых сессий
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

            # Таблица для хранения статистики по играм
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
        """
        Сохраняет игровую сессию и статистику в БД.

        Args:
            player_name (str): Имя игрока
            score (int): Финальный счет
            game_duration (int): Длительность игры в секундах
            settings (dict): Настройки игры
            food_eaten (int): Количество съеденной еды
            max_length (int): Максимальная длина змейки
            walls_passed (bool): Флаг прохождения сквозь стены

        Returns:
            int or None: ID сохраненной сессии или None при ошибке
        """
        if not self.connection:
            print("❌ Нет подключения к БД")
            return None

        try:
            cursor = self.connection.cursor()

            # Сохраняем игровую сессию
            cursor.execute('''
                INSERT INTO game_sessions (player_name, start_time, end_time, score, game_duration, settings)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (player_name, datetime.now(), datetime.now(), score, game_duration, json.dumps(settings)))

            session_id = cursor.fetchone()[0]

            # Сохраняем статистику
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
        """
        Получает таблицу рекордов из БД.

        Args:
            limit (int): Количество возвращаемых записей (по умолчанию 10)

        Returns:
            list: Список кортежей с данными рекордов:
                (player_name, score, game_duration, end_time)
        """
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
        """
        Закрывает подключение к БД.
        """
        if self.connection:
            self.connection.close()
            print("✅ Подключение к PostgreSQL закрыто")