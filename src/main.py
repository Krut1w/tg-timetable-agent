import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
# from libs import test_get_num

script_dir = os.path.dirname(os.path.abspath(__file__))
if load_dotenv(f"{script_dir}/../.env") == False:
    print("Error load .env. Rename .env.example and add information in file")

TG_TOKEN = os.getenv("TG_TOKEN")
DB_CONFIG = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')} host={os.getenv('DB_HOST')}"


bot = Bot(token=TG_TOKEN, session=session) # session=session - часть проксирования
dp = Dispatcher()

# pool = AsyncConnectionPool(conninfo=DB_CONFIG, open=False)

@dp.message(Command("add"))
async def add_record(message: types.Message, command: CommandObject):
    if not command.args:
        return await message.answer("Enter text after command. /add Hello World")

    user_id = message.from_user.id
    content = command.args

    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO users_tasks (user_id, task) VALUES (%s, %s)",
                    (message.from_user.id, command.args)
                )
        await message.answer(f"Add note: ID {user_id}, text: {content}")
    
    except Exception as e:
        print(f"Error BD: {e}")
        await message.answer("Error save text.")


async def main():
    #await pool.open()

    try:
        await dp.start_polling(bot)
    finally:
        pass #await pool.close()

    # try:
    #     val = 10
    #     result = test_get_num(val)
    #     print(f"Число из Python: {val}")
    #     print(f"Результат из C: {result}")
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
