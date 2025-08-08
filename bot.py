import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.content_type import ContentType
import asyncio

API_TOKEN = "8168140620:AAHEL7fDn5vO_KsLuo-R1iC_tLCM4TTM918"
ADMIN_ID = 8144158477  # твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

UPLOAD_FOLDER = "uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@dp.message(F.content_type == ContentType.DOCUMENT)
async def upload_file(message: Message):
    if message.from_user.id == ADMIN_ID:
        file_path = os.path.join(UPLOAD_FOLDER, "file")  # всегда одно и то же имя
        file = await bot.get_file(message.document.file_id)
        await bot.download_file(file.file_path, destination=file_path)
        await message.answer("✅ Файл обновлён! Ссылка осталась прежней.")
    else:
        await message.answer("❌ У вас нет прав загружать файлы.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())