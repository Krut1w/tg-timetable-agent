import os
from dotenv import load_dotenv
from libs import test_get_num

load_dotenv("../.env")

api_key = os.getenv("TG_API_KEY")

def main():
    try:
        val = 10
        result = test_get_num(val)
        print(f"Число из Python: {val}")
        print(f"Результат из C: {result}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()