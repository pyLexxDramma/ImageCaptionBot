import os
import requests
import datetime
import random
from PIL import Image
from PIL import ImageDraw
from telebot import TeleBot
from telebot.apihelper import get_file

print('Start telegram bot...')

token_bot = os.getenv('TOKEN')
bot = TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def message_reply(message):
    file_id = message.photo[-1].file_id
    file_info = get_file(token_bot, file_id)
    file_path = file_info.get('file_path')
    url = f"https://api.telegram.org/file/bot{token_bot}/{file_path}"
    response = requests.get(url)
    image = response.content
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
    folder = os.getenv('PATH_FOLDER')
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name = f"{now}_{message.chat.id}.jpg"
    path = os.path.join(folder, file_name)
    with open(path, 'wb') as f:
        f.write(image)
    bot.send_message(message.chat.id, 'Картинка обрабатывается...')
    image = add_title(path)
    bot.send_photo(message.chat.id, photo=image)


def get_title() -> str:
    path = os.getenv("PATH_FILE_STORAGE")
    with open(path, ) as f:
        titles = f.readlines()
    title = random.choice(titles)
    return title


def add_title(path_file):
    title = get_title()
    img = Image.open(path_file)
    image = ImageDraw.Draw(img)
    image.text((int(img.width/2), int(img.height/1.5)), title)
    img.show()
    return img


bot.infinity_polling(skip_pending=True)
