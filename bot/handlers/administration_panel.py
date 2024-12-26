from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot.utils.read_text import load_text_form_file
from bot.database.database import (
    get_user_starting_the_bot,  # Импорт функции для получения не авторизованных пользователей
)
from bot.keyboards.keyboards import (
    generate_admin_panel_keyboard,
)

router_administration_panel = (
    Router()
)  # Создание маршрутизатора для обработки команд и сообщений.


class MessageStorage(StatesGroup):
    message_to_be_sent = State()  # Состояние хранения сообщения.


# Обработчик состояния админской-панели
@router_administration_panel.callback_query(F.data == "admin_panel")
async def login_to_the_admin_panel(callback_query: CallbackQuery) -> None:
    """
    Переходит в админское меню

    Аргументы:
    :param callback_query: Сообщение пользователю
    """
    await callback_query.message.edit_text(
        f"{load_text_form_file('text_admin_panel.json')}",
        reply_markup=generate_admin_panel_keyboard(),
    )


# Обработчик состояния подготовки сообщения пользователям
@router_administration_panel.callback_query(F.data == "sending_messages")
async def messages_for_user(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Начинает процесс регистрации сообщения для отправки пользователям

    Аргументы:
    :param callback_query: Сообщение пользователя
    :param state:
    """
    await state.set_state(MessageStorage.message_to_be_sent)
    await callback_query.message.answer(
        f"{load_text_form_file('text_what_do_you_sending_message.json')}"
    )


# Обработчик состояния отправки сообщения пользователям
@router_administration_panel.message(MessageStorage.message_to_be_sent)
async def sending_messages_for_user(
        message: Message, state: FSMContext, bot: Bot
) -> None:
    """
    Отправляет сообщения пользователям

    Аргументы:
    :param message: Сообщение пользователя
    :param state:
    :param bot:
    """
    await state.update_data(message_to_be_sent=message.text)
    message_storage = await state.get_data()
    admin_messages = message_storage["message_to_be_sent"]

    for id_user, name in get_user_starting_the_bot():
        await bot.send_message(chat_id=id_user, text=f"{admin_messages}")

    await message.answer(f"{load_text_form_file('text_sending_message.json')}")
    await message.answer(
        f"{load_text_form_file('text_admin_panel.json')}",
        reply_markup=generate_admin_panel_keyboard(),
    )

    await state.clear()  # Сброс состояния после отправки сообщения пользователям.


# Обработчик состояния статистики
@router_administration_panel.callback_query(F.data == "statistics")
async def user_activity_analysis(callback_query: CallbackQuery) -> None:
    """
    Статистика

    Аргументы:
    :param callback_query:
    """
    await callback_query.message.answer(
        f"{load_text_form_file('text_statistics.json')}"
    )
