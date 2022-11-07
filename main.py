import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keys import API_TOKEN
from book2 import Book

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

next_button = InlineKeyboardButton(text='Next page >', callback_data="next_page")
prev_button = InlineKeyboardButton(text='< Previous  page', callback_data="prev_page")
keyboard_inline_first_page = InlineKeyboardMarkup().add(next_button)
keyboard_inline = InlineKeyboardMarkup().add(prev_button, next_button)

book = Book()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Read-o-bot!")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_book(message: types.Message):
    if message.content_type == 'document':
        await message.document.download(destination_dir='./', make_dirs=True)
        name = message.document.file_name
        await message.reply(f"We've got a file!\nNAME: {name}")
        book.split_text_for_tg(book.read_book_file())
        await message.reply(book.next_page(), reply_markup=keyboard_inline)

@dp.callback_query_handler(text='next_page')
async def next_page(call: types.CallbackQuery):
    await call.message.answer(book.next_page(), reply_markup=keyboard_inline)
    await call.answer()
    
@dp.callback_query_handler(text='prev_page')
async def prev_page(call: types.CallbackQuery):
    # await call.message.answer("PREV PAGE")
    await call.message.answer(book.prev_page(), reply_markup=keyboard_inline)
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
