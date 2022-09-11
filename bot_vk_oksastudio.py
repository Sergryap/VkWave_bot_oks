from vkwave.bots import SimpleLongPollBot

from handlers import client_router
from FSMstate import fsm_training_router
from password import TOKEN, GROUP_ID
# from middlewares import MatFilterMiddleware

bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
# bot.middleware_manager.add_middleware(MatFilterMiddleware())
# bot.dispatcher.add_router(fsm_training_router)
bot.dispatcher.add_router(client_router)


bot.run_forever()
