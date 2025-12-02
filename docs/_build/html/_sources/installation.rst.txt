Установка и настройка
=====================

Требования
----------

* Python 3.8 или выше
* PostgreSQL 12 или выше
* Pygame 2.0+
* Psycopg2

Установка зависимостей
----------------------

.. code-block:: bash

   pip install -r requirements.txt

Или установите пакеты отдельно:

.. code-block:: bash

   pip install pygame psycopg2-binary

Настройка базы данных
---------------------

1. Установите PostgreSQL
2. Создайте базу данных:

.. code-block:: sql

   CREATE DATABASE snake_game;

3. Настройте подключение в ``database/db_handler.py``:

.. code-block:: python

   db_config = {
       'host': 'localhost',
       'port': '5432',
       'dbname': 'snake_game',
       'user': 'postgres',
       'password': 'your_password'
   }

Проверка установки
------------------

Запустите игру для проверки:

.. code-block:: bash

   python main.py --player-name "Test"

Если игра запускается и показывает меню - установка прошла успешно!