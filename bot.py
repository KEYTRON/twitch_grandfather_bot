import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage  # Подключаем хранилище для FSM

#from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import API_TOKEN  # Ваш токен API

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация хранилища
storage = MemoryStorage()  # Хранилище для FSM

# Инициализация диспетчера
dp = Dispatcher(storage=storage, bot=bot)  # Передаем bot и storage через именованные параметры

# Список всех пользователей, которые начали взаимодействовать с ботом
user_ids = set()  # Множество для хранения ID пользователей

# Идентификатор группы или канала, куда бот будет отправлять уведомления
GROUP_ID = 2213876546  # Используйте свой ID группы или канала


# Обработчик команды /start
@dp.message(Text("/start"))
async def start_command(message: types.Message):
    # Добавление пользователя в список
    user_ids.add(message.from_user.id)

    # Создание клавиатуры
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем кнопки
    donate_button = KeyboardButton(text="💖 Поддержать Деда")
    keyboard.add(donate_button)  # Правильное добавление кнопки

    # Передаем клавиатуру в метод для ответа пользователю
    await message.answer(
        "Добро пожаловать! Я бот для оповещений о стримах и поддержке проекта. "
        "Нажмите кнопку ниже, чтобы поддержать проект 🌟.\n\n"
        "Я всегда рад помочь! Используйте команду /help для получения помощи.",
        reply_markup=keyboard
    )


# Обработчик команды /help
@dp.message(Text("/help"))
async def help_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    donate_button = KeyboardButton(text="💖 Поддержать Деда")
    keyboard.add(donate_button)  # Добавление кнопки

    await message.answer(
        "Привет! Я бот для уведомлений о стримах.\n\n"
        "Вот мои команды:\n"
        "/start - Приветственное сообщение и кнопка поддержки проекта.\n"
        "/help - Помощь и описание команд.\n"
        "/donate - Как поддержать проект с помощью звезд.\n"
        "Также я буду уведомлять вас о начале стримов!",
        reply_markup=keyboard
    )


# Обработчик команды /donate
@dp.message(Text("/donate"))
async def donate_command(message: types.Message):
    await message.answer(
        "Вы можете поддержать проект, отправив звезды ⭐.\n\n"
        "Пример: переведите 5 ⭐ (звёзд), чтобы поблагодарить разработчика!\n"
        "Инструкция по переводу звёзд:\n"
        "1. Найдите наш аккаунт в системе ⭐.\n"
        "2. Отправьте любое количество звёзд.\n"
        "Спасибо за вашу поддержку!"
    )


# Обработчик нажатия на кнопку пожертвования
@dp.message(lambda message: message.text == "💖 Поддержать Деда")
async def donate_handler(message: types.Message):
    await message.answer(
        "Вы можете поддержать проект, отправив звезды.\n\n"
        "Пример: переведите 5 ⭐ (звёзд), чтобы поблагодарить разработчика!\n"
        "Инструкция по переводу звёзд:\n"
        "1. Найдите наш аккаунт в системе ⭐.\n"
        "2. Отправьте любое количество звёзд.\n"
        "Спасибо за вашу поддержку!"
    )


# Функция для уведомления всех пользователей и группы о начале стрима
async def notify_stream_start():
    stream_message = "🎮 Начался стрим! Присоединяйтесь к нам на Twitch: https://www.twitch.tv/nosoulbuy"

    # Создаем кнопки для уведомления
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смотреть стрим", url="https://www.twitch.tv/nosoulbuy")],
        [InlineKeyboardButton(text="Поддержать проект", url="https://t.me/nosoul_propose")]  # Ссылка на группу
    ])

    # Уведомление всех пользователей
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, stream_message, reply_markup=inline_keyboard)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    # Уведомление в группу или канал
    try:
        await bot.send_message(GROUP_ID, stream_message, reply_markup=inline_keyboard)
    except Exception as e:
        print(f"Не удалось отправить сообщение в группу или канал: {e}")


# Запуск бота
if __name__ == "__main__":
    asyncio.run(dp.start_polling())  # Запуск асинхронного polling
