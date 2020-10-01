from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('menu', 'Меню'),
        types.BotCommand('settings', 'Настройки')
    ])