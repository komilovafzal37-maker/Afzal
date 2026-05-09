import asyncio
import os   
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)   


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

lessons = {

    "📘 Основы": {

        "📌 Переменные": {
            "code": '''name = "Alex"
age = 16

print(name)
print(age)''',

            "text": (
                "🔹 Переменные\n\n"
                "Переменные нужны для хранения данных.\n\n"
                "name = текст\n"
                "age = число\n\n"
                "print() выводит данные."
            )
        },

        "📌 Условия": {
            "code": '''age = 18

if age >= 18:
    print("Совершеннолетний")
else:
    print("Несовершеннолетний")''',

            "text": (
                "🔹 Условия if\n\n"
                "if проверяет условие.\n"
                "else выполняется если условие ложное."
            )
        },

        "📌 Циклы": {
            "code": '''for i in range(5):
    print(i)''',

            "text": (
                "🔹 Циклы\n\n"
                "for повторяет код несколько раз.\n"
                "range(5) = от 0 до 4."
            )
        },

        "📌 Функции": {
            "code": '''def hello(name):
    print("Привет", name)

hello("Alex")''',

            "text": (
                "🔹 Функции\n\n"
                "def создаёт функцию.\n"
                "Функции помогают не повторять код."
            )
        }
    },


    "🌐 Веб-разработка": {

        "Flask": {
            "code": '''from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"''',

            "text": (
                "🔹 Flask\n\n"
                "Flask используется для создания сайтов.\n"
                "@app.route создаёт страницу."
            )
        },

        "FastAPI": {
            "code": '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}''',

            "text": (
                "🔹 FastAPI\n\n"
                "FastAPI нужен для API и backend."
            )
        }
    },

    "🤖 AI и нейросети": {

        "NumPy": {
            "code": '''import numpy as np

arr = np.array([1, 2, 3])

print(arr)''',

            "text": (
                "🔹 NumPy\n\n"
                "NumPy используется для работы с массивами."
            )
        },

        "Pandas": {
            "code": '''import pandas as pd

data = {
    "name": ["Alex", "John"]
}

df = pd.DataFrame(data)

print(df)''',

            "text": (
                "🔹 Pandas\n\n"
                "Pandas нужен для анализа данных."
            )
        }
    },

    "🔒 Парсинг и боты": {

        "Aiogram": {
            "code": '''from aiogram import Bot''',

            "text": (
                "🔹 Aiogram\n\n"
                "Aiogram используется для Telegram-ботов."
            )
        },

        "Requests": {
            "code": '''import requests

response = requests.get("https://example.com")

print(response.text)''',

            "text": (
                "🔹 Requests\n\n"
                "Requests отправляет HTTP запросы."
            )
        }
    }
}

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Основы")],
        [KeyboardButton(text="🌐 Веб-разработка")],
        [KeyboardButton(text="🤖 AI и нейросети")],
        [KeyboardButton(text="🔒 Парсинг и боты")]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(message: Message):

    text = (
        "🐍 Python Helper Bot\n\n"
        "Выберите направление Python."
    )

    await message.answer(
        text,
        reply_markup=main_keyboard
    )

@dp.message(F.text.in_(lessons.keys()))
async def category(message: Message):

    category_name = message.text

    topics = lessons[category_name]

    keyboard = []

    for topic in topics.keys():
        keyboard.append([KeyboardButton(text=topic)])

    keyboard.append([KeyboardButton(text="🔙 Назад")])

    topic_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    await message.answer(
        f"📚 Раздел: {category_name}\n\nВыберите тему:",
        reply_markup=topic_keyboard
    )

@dp.message()
async def lessons_handler(message: Message):

    # Назад
    if message.text == "🔙 Назад":

        await message.answer(
            "🏠 Главное меню",
            reply_markup=main_keyboard
        )

        return

    # Поиск темы
    for category in lessons.values():

        for topic_name, topic_data in category.items():

            if message.text == topic_name:
                code = topic_data["code"]
                text = topic_data["text"]

                answer = (
                    f"{text}\n\n"
                    f"💻 Код:\n\n"
                    f"<pre>{code}</pre>"
                )

                await message.answer(
                    answer,
                    parse_mode="HTML"
                )

                return

    
    await message.answer(
        "❌ Тема не найдена.\n"
        "Выберите раздел через меню."
    )

async def main():

    print("Бот запущен!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())