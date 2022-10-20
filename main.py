import logging
from aiogram import Bot, Dispatcher, executor, types
from keys import API_TOKEN
from book import read_book, split_text_for_tg

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Read-o-bot!")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_book(message: types.Message):
    if message.content_type == 'document':
        await message.document.download(destination_dir='./', make_dirs=True)
        name = message.document.file_name
        await message.reply(f"We've got a file!\nNAME: {name}")
        book = read_book()
        fist_text = split_text_for_tg(book)
        await message.reply(fist_text)
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)