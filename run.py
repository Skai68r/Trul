from bot_settings import bot
from handlers import welcome

welcome.register_welcome_handlers()


bot.polling(non_stop=True)  #бесперерывный ответ бота на запросы
