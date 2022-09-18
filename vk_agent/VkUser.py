import asyncio
import string

# from Data_base.DecorDB import db_insert
# from Selenium_method.main import load_info_client
from FSMstate import FSMQuiz, HandlerFSM
from .vk_api import VkApi
from .verify import Verify
from .send_msg import SendMSG
from .key_button import MyKeyButton
from vkwave.bots import SimpleBotEvent


class VkUser(
			VkApi,
			FSMQuiz,
			Verify,
			SendMSG,
			MyKeyButton,
			HandlerFSM,
):
	"""
	Основной класс взаимодействия пользователя и бота
	"""

	COMMAND = f"""
	✔️ Помочь записатьcя - "z"
	✔️️ Сориентировать по ценам - "p"
	✔️️ Наш адрес - "h"
	✔️️ Показать наши работы - "ex"
	✔️️ Связаться с администрацией - "ad"
	✔️️ Про наши курсы - "ed"
	✔️️ Начать с начала - "start"
	"""

	def __init__(self, event: SimpleBotEvent):
		super().__init__()
		self.event = event
		self.user_id = event.user_id
		text = event.text.split('@')[0] if event.text[0] == '/' else event.text
		self.msg = text.lower().translate(str.maketrans('', '', string.punctuation))
		self.msg_previous = self.__dict__.get('msg_previous', self.msg)
		self.user_info = False
		self.fsm_training = False
		self.fsm_discount = False
		# FSMQuiz.__init__(self)
		# self.user_ids = [7352307, 448564047, 9681859]  # id администраторов сообщества Vk
		self.user_ids = 7352307  # id администраторов сообщества Vk

	#@db_insert(table='Message')
	async def handler_msg(self, context=False):
		"""Функция-обработчик событий сервера типа MESSAGE_NEW"""
		if not self.user_info:
			self.user_info = await self.get_info_users()
		if context:
			return await self.handler_msg_fsm(context)
		await self.send_message_to_all_admins()

		if await self.fsm_state():
			return

		if self.verify_hello():
			await self.send_hello()

		for verify, func in self.get_verify_func().items():
			if verify():
				await func()
