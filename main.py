from StyleTransfer import get_new_img, imsave
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import keyboards as kb
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = str(message.chat.id)
    if not os.path.exists('data\\' + chat_id):
        os.mkdir(f'data\\{chat_id}')
        os.mkdir(f'data\\{chat_id}\\transfer')
        os.mkdir(f'data\\{chat_id}\\style')
        os.mkdir(f'data\\{chat_id}\\content')
    with open(f'data\\{chat_id}\\key.txt', 'w') as f:
        f.write("style")
    await message.reply('Привет!\nЯ бот, который умеет переносить стиль одного изображения на другое\n '
                        'Чтобы узнать подробнее об этом, а также самому попробовать, напишите /help, я все расскажу',
                        reply_markup=kb.greet_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Отлично, все очень просто, сейчас я пришлю тебе пример того, что должно получиться")
    with open('data\\example.jpg', 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo)
        await bot.send_message(message.from_user.id, 'Здорово, правда?!\n\n'
                               '• Чтобы выбрать свой стиль, напиши мне /style и пришли какое-нибудь изображение "стиля"'
                               ', например картину Ван Гога "Звездная ночь"\n'
                               '• Затем, чтобы выбрать свое фото, напиши мне /content и пришли какое-нибудь фото '
                               '"контента", например твой вид из окна\n'
                               '• После этого напиши /get и жди изображение, на это может уйти до 5 минут\n'
                               '• Если захочешь попробовать другие изображения стиля или контента, '
                               'просто еще раз набери /style или /content соответственно и пришли новую картинку\n\n'
                               'Ну что, пробуем?')


@dp.message_handler(commands=['style'])
async def process_style_command(message: types.Message):
    chat_id = str(message.chat.id)
    with open(f'data\\{chat_id}\\key.txt', 'w') as f:
        f.write("style")
    await bot.send_message(message.from_user.id, "Жду твой стиль")


@dp.message_handler(commands=['content'])
async def process_content_command(message: types.Message):
    chat_id = str(message.chat.id)
    with open(f'data\\{chat_id}\\key.txt', 'w') as f:
        f.write("content")
    await bot.send_message(message.from_user.id, "Жду твое фото")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    chat_id = str(message.chat.id)
    with open(f'data\\{chat_id}\\key.txt', 'r') as f:
        key = f.read()
    await message.photo[-1].download(f'data\\{chat_id}\\{key}\\last_{key}.jpg')
    await bot.send_message(message.from_user.id, "Замечательно, изображение получил")


@dp.message_handler(commands=['get'])
async def process_content_command(message: types.Message):
    chat_id = str(message.chat.id)

    if not os.listdir(f"data\\{chat_id}\\content"):
        await bot.send_message(message.from_user.id, "Извините, у меня нет изображения контента, "
                                                     "напишите /content и отправьте фото еще раз")
    elif not os.listdir(f"data\\{chat_id}\\style"):
        await bot.send_message(message.from_user.id, "Извините, у меня нет изображения стиля, "
                                                     "напишите /style и отправьте фото еще раз")
    else:
        content_name = f"data\\{chat_id}\\content\\last_content.jpg"
        style_name = f"data\\{chat_id}\\style\\last_style.jpg"
        max_size = 256

        await bot.send_message(message.from_user.id, "Еще несколько минут, и будет готово")

        output = get_new_img(content_name, style_name, max_size)
        imsave(output, f"data\\{chat_id}\\transfer\\last_output.jpg")
        with open(f"data\\{chat_id}\\transfer\\last_output.jpg", 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo)


if __name__ == '__main__':
    executor.start_polling(dp)
