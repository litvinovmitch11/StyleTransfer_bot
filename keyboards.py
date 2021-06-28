from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button1 = KeyboardButton('/start')
button2 = KeyboardButton('/help')
button3 = KeyboardButton('/content')
button4 = KeyboardButton('/style')
button5 = KeyboardButton('/get')

greet_kb = ReplyKeyboardMarkup()
greet_kb.row(
    button1, button2).row(
    button3, button4).add(
    button5)
