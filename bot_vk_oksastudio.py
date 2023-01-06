from vkwave.bots import SimpleLongPollBot
from environs import Env
from handlers import client_router
from FSMstate import fsm_training_router
# from middlewares import MatFilterMiddleware


if __name__ == '__main__':
    env = Env()
    env.read_env()
    TOKEN = env('TOKEN')
    GROUP_ID = env('GROUP_ID')
    bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)
    # bot.middleware_manager.add_middleware(MatFilterMiddleware())
    # bot.dispatcher.add_router(fsm_training_router)
    bot.dispatcher.add_router(client_router)
    bot.run_forever()
