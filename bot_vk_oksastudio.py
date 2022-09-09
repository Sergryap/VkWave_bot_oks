from vkwave.bots import SimpleLongPollBot

from handlers import client_router
from password import TOKEN, GROUP_ID

bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)

bot.dispatcher.add_router(client_router)

bot.run_forever()
