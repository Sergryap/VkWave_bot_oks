import json
import string
import time

from vkwave.bots import simple_bot_message_handler, SimpleBotEvent, DefaultRouter
from .global_handler import global_handler

client_router = DefaultRouter()


@simple_bot_message_handler(client_router)
async def basic_send(event: SimpleBotEvent):
	# await event.answer("got hello")
	await global_handler(event)
