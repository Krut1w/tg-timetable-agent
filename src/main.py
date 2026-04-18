from calc import test_get_num

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