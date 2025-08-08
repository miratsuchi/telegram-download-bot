import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = "8168140620:AAHEL7fDn5vO_KsLuo-R1iC_tLCM4TTM918"
ADMIN_ID = 8144158477  # твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    waiting_for_file = State()

# Загружаем/инициализируем базу файлов
try:
    with open("files.json", "r") as f:
        files_db = json.load(f)
except FileNotFoundError:
    files_db = {}

@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ты не админ.")
        return
    await message.answer("Привет! Отправь мне файл, который я буду отдавать по ссылке.")
    await state.set_state(Form.waiting_for_file)

@dp.message(Form.waiting_for_file, F.document)
async def file_handler(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ты не админ.")
        return

    file_id = message.document.file_id
    files_db["current_file"] = file_id
    with open("files.json", "w") as f:
        json.dump(files_db, f)

    await message.answer("Файл сохранён! Теперь его можно скачивать по ссылке.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())