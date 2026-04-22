import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from psycopg_pool import AsyncConnectionPool
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
# from libs import test_get_num

script_dir = os.path.dirname(os.path.abspath(__file__))
if load_dotenv(f"{script_dir}/../.env") == False:
    print("Error load .env. Rename .env.example and add information in file")

TG_TOKEN = os.getenv("TG_TOKEN")
DB_CONFIG = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')} host={os.getenv('DB_HOST')}"

proxy_url = "http://127.0.0.1:20171"
session = AiohttpSession(proxy=proxy_url)
bot = Bot(token=TG_TOKEN, session=session)

# bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

pool = AsyncConnectionPool(conninfo=DB_CONFIG, min_size=2, max_size=10, open=False)
scheduler = AsyncIOScheduler()

class AddTask(StatesGroup):
    waiting_title = State()
    waiting_deadline = State()
    waiting_remind = State()

async def create_user(telegram_id: int, username: str | None):
    async with pool.connection() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, username)
            VALUES (%s, %s)
            ON CONFLICT (telegram_id) DO NOTHING
            """, (telegram_id, username))
        
async def add_task(telegram_id: int, title: str, deadline, remind_at):
    async with pool.connection() as conn:
        row = await conn.execute(
            "SELECT id FROM users WHERE telegram_id=%s", (telegram_id,)
        )
        user = await row.fetchone()

        row = await conn.execute("""
            INSERT INTO tasks (user_id, title, deadline)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (user[0], title, deadline))
        task = await row.fetchone()

        await conn.execute("""
            INSERT INTO reminders(task_id, fire_at)
            VALUES (%s, %s)
            """, (task[0], remind_at))
        
async def get_pending_reminders():
    async with pool.connection() as conn:
        rows = await conn.execute("""
            SELECT r.id, t.title, t.deadline, u.telegram_id
            FROM reminders r
            JOIN tasks t ON t.id = r.task_id
            JOIN users u ON u.id = t.user_id
            WHERE r.fire_at <= NOW() AND r.sent = false
            """)

        return await rows.fetchall()

async def mark_reminder_sent(reminder_id: int):
    async with pool.connection() as conn:
        await conn.execute(
            "UPDATE reminders SET sent = true WHERE id = %s", (reminder_id,)
        )

async def send_reminders():
    reminders = await get_pending_reminders()
    for r_id, title, deadline, telegram_id in reminders:
        deadline_str = deadline.strftime("%d.%m.%Y %H:%M")
        await bot.send_message (
            telegram_id, f"Напоминание: {title}\n Дедлайн: {deadline_str}"
        )
        await mark_reminder_sent(r_id)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer("Hi!\n \"/add\" - add a new task")

@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(AddTask.waiting_title)
    await message.answer("Name task?")

@dp.message(AddTask.waiting_title)
async def got_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddTask.waiting_deadline)
    await message.answer("Deadline? Format: DD.MM.YYYY HH:MM")

@dp.message(AddTask.waiting_deadline)
async def got_deadline(message: Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("Error format")
        return
    
    await state.update_data(deadline=deadline)
    await state.set_state(AddTask.waiting_remind)
    await message.answer("Napominaniye? Format takoy zhe")

@dp.message(AddTask.waiting_remind)
async def got_remind(message: Message, state: FSMContext):
    try:
        remind_at = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("Error format")
        return

    data = await state.get_data()
    await state.clear()

    await add_task(
        telegram_id=message.from_user.id,
        title=data["title"],
        deadline=data["deadline"],
        remind_at=remind_at,
    )

    deadline_str = data["deadline"].strftime("%d.%m.%Y %H:%M")
    remind_str = remind_at.strftime("%d.%m.%Y %H:%M")

    await message.answer(
        f"Add Task\n"
        f"Name: {data['title']}\n"
        f"Deadline: {deadline_str}\n"
        f"Napominanye: {remind_str}"
    )


async def main():
    await pool.open()
    print("db connected")

    scheduler.add_job(send_reminders, "interval", minutes=1)
    scheduler.start() 

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        if scheduler.running:
            scheduler.shutdown()
            
        await pool.close()
        await bot.session.close()
        print("db disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot off")

    # try:
    #     val = 10
    #     result = test_get_num(val)
    #     print(f"Число из Python: {val}")
    #     print(f"Результат из C: {result}")
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")
