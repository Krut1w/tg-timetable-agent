
## Первый запуск

1. `git clone https://github.com/Krut1w/tg-timetable-agent.git`
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `pip install -e .`
6. `python src/main.py`

Что делает:
1) Клонирует репозиторий
2) Создает виртуальное окружение питона (можно и без него но с ним не ломаются системные пакеты, предпочтительно запускать на линуксе)
3) Запускает это окружение (`deactivate` в консоль - деактивирует) 
4) Загружает внешние зависимости проекта
5) Компилирует С файлы
6) Запускает `main.py`


## Последующие запуски

1. `pip install -e .`
2. `python src/main.py`

## О файлах и папках

`c_src` - файлы с C кодом  
`docs` - документация  
`lib` - создается после компиляции С файлов, содержит скомпилированные файлы библиотек  
`src` - файлы с python кодом  
`venv` - виртуальное окружение  
`.gitignore` - гитигнор  
`CMakeLists.txt` - файл cmake для компиляции c кода  
`pyproject.toml` - конфигурация python проекта  
`requirements.txt` - файл с внешними библиотеками для python   

`src/libs.py` - линковка библиотек и определение функций

## Используемые библиотеки

`aiogram` - общение с Telegram API  
`scikit-build-core` - компилирование и использование C библиотек  

## Файл конфигурации

`.env` - файл с ключами, паролями и т.д

## Создание базы данных

`CREATE DATABASE tg_timeable_db`

`\c tg_timeable_db`

```postgresql
CREATE TABLE users (
id BIGSERIAL PRIMARY KEY,
telegram_id BIGINT NOT NULL UNIQUE,
username VARCHAR(64),
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
```postgresql
CREATE TABLE tasks (
id BIGSERIAL PRIMARY KEY,
user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
title VARCHAR(255) NOT NULL,
deadline TIMESTAMPTZ,
is_done BOOLEAN NOT NULL DEFAULT FALSE,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

```postgresql
CREATE TABLE reminders (
id BIGSERIAL PRIMARY KEY,
task_id BIGINT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
fire_at TIMESTAMPTZ NOT NULL,
sent BOOLEAN NOT NULL DEFAULT FALSE
);
```

`CREATE INDEX ON reminders (fire_at) WHERE sent = false;`

`CREATE INDEX ON tasks (user_id);`
