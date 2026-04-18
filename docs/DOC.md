## Первый запуск

`git clone https://github.com/Krut1w/tg-timetable-agent.git`
`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
`pip install -e .`
`python src/main.py`

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
`lib` - создается после компиляции С файлов, содержит библиотеки
`src` - файлы с python кодом
`venv` - виртуальное окружение
`.gitignore` - гитигнор
`CMakeLists.txt` - файл cmake для компиляции c кода
`pyproject.toml` - конфигурация python проекта
`requirements.txt` - файл с внешними библиотеками для python

## Используемые библиотеки

`aiogram` - общение с Telegram API
`scikit-build-core` - компилирование и использование C библиотек
