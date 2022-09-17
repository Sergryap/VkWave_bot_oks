import asyncio
import string

from datetime import datetime
from vk_agent import VkUser
from vkwave.bots import SimpleBotEvent

USERS = {}


async def users_update(user_id, msg_previous, user_class: VkUser):
	"""
	Добавление экземпляра класса пользователя в глобальный словарь для повторного использования
	"""
	global USERS
	USERS.update({
		f'id_{user_id}': {'user_class': user_class, 'msg_previous': msg_previous, 'time_create': datetime.now()}
	})
	if len(USERS) == 50:
		min_date = min([USERS[user]['time_create'] for user in USERS])
		user_delete = [user for user in USERS if USERS[user]['time_create'] == min_date][0]
		del USERS[user_delete]


async def global_handler(event: SimpleBotEvent, context=False):
	"""
	Обработка сообщений пользователя
	"""
	global USERS
	user_id = event.user_id

	if f'id_{user_id}' not in USERS:
		msg = event.text.split('@')[0] if event.text[0] == '/' else event.text
		text = msg.lower().translate(str.maketrans('', '', string.punctuation))
		await users_update(user_id, user_class=VkUser(event), msg_previous=text)
		f = await USERS[f'id_{user_id}']['user_class'].handler_msg(context)

	else:
		msg = event.text.split('@')[0] if event.text[0] == '/' else event.text
		text = msg.lower().translate(str.maketrans('', '', string.punctuation))
		USERS[f'id_{user_id}']['user_class'].msg = text
		USERS[f'id_{user_id}']['user_class'].event = event
		# if USERS[f'id_{user_id}']['user_class'].verify_discount(previous=True) or USERS[f'id_{user_id}']['user_class'].verify_training(previous=True):
		# 	await users_update(user_id, user_class=VkUser(event), msg_previous=USERS[f'id_{user_id}']['msg_previous'])
		# 	USERS[f'id_{user_id}']['user_class'].msg_previous = USERS[f'id_{user_id}']['msg_previous']
		f = await USERS[f'id_{user_id}']['user_class'].handler_msg(context)
		USERS[f'id_{user_id}']['user_class'].msg_previous = text
		USERS[f'id_{user_id}']['msg_previous'] = text

	if context:
		return f
