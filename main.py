import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import MenuButtonCommands

from book2 import Book
from keys import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

next_button = InlineKeyboardButton(text='Next page >', callback_data="next_page")
prev_button = InlineKeyboardButton(text='< Previous  page', callback_data="prev_page")
keyboard_inline_first_page = InlineKeyboardMarkup().add(next_button)
keyboard_inline_last_page = InlineKeyboardMarkup().add(prev_button)
keyboard_inline = InlineKeyboardMarkup().add(prev_button, next_button)

book = Book()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Read-o-bot!\nJust upload some .epub file so you can read it here")


@dp.message_handler(commands=['user'])
async def send_user(message: types.Message):
    await message.reply(str(message.from_user.id))
    await message.reply(str(message.from_id))

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_book(message: types.Message):
    if message.content_type == 'document':
        await message.document.download(destination_dir='./', make_dirs=True)
        name = message.document.file_name
        # await message.reply(f"We've got a file!\nNAME: {name}")
        book.split_text_for_tg(book.read_book_file())
        await message.reply(book.current_page(), reply_markup=keyboard_inline_first_page)


@dp.message_handler(commands=['next'])
async def next_page_command(message: types.Message):
    if book.is_last_page():
        await message.reply(book.next_page(), reply_markup=keyboard_inline_last_page)
    else:
        await message.reply(book.next_page(), reply_markup=keyboard_inline)
    
@dp.callback_query_handler(text='next_page')
async def next_page(call: types.CallbackQuery):
    if book.is_last_page():
        await call.message.answer(book.next_page(), reply_markup=keyboard_inline_last_page)
    else:
        await call.message.answer(book.next_page(), reply_markup=keyboard_inline)
    await call.answer()
    
    
@dp.message_handler(commands=['prev'])
async def prev_page_command(message: types.Message):
    if book.is_first_page():
        await message.reply(book.prev_page(), reply_markup=keyboard_inline_first_page)
    else:
        await message.reply(book.prev_page(), reply_markup=keyboard_inline)    
    
@dp.callback_query_handler(text='prev_page')
async def prev_page(call: types.CallbackQuery):
    if book.is_first_page():
        await call.message.answer(book.prev_page(), reply_markup=keyboard_inline_first_page)
    else:
        await call.message.answer(book.prev_page(), reply_markup=keyboard_inline)
    await call.answer()
    
    
@dp.message_handler(commands=['goto'])
async def goto_page(message: types.Message):
    argument = message.get_args()
    try:
        argument = int(argument)
    except:
        await message.reply("Usage /goto <number_of_page>")
    await message.reply(book.current_page(argument))
#     if book.is_first_page():
#         await message.reply(book.prev_page(), reply_markup=keyboard_inline_first_page)
#     else:
#         await message.reply(book.prev_page(), reply_markup=keyboard_inline) 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
