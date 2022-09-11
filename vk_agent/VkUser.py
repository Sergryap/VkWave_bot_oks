import time
import requests
import asyncio
import string

from .VKsearch import VkSearch
# from Data_base.DecorDB import db_insert
import os
import re
import random
# from Selenium_method.main import load_info_client
from FSMstate import FSMQuizTraining
from .verify import Verify
from .key_button import MyKeyButton
from vkwave.bots import SimpleBotEvent


class VkUser(
			VkSearch,
			FSMQuizTraining,
			Verify,
			MyKeyButton,
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
		self.msg_previous = self.msg
		self.user_info = self.get_info_users()
		# self.user_ids = '7352307,448564047,9681859'  # id администраторов сообщества Vk
		self.user_ids = '7352307'  # id администраторов сообщества Vk

	async def send_message(self, some_text, buttons=True):
		"""
		Отправка сообщения пользователю.
		Если buttons=True создается клавиатура
		"""
		params = {
			"message": some_text,
			"keyboard": None}

		for key, func in self.BUTTON_FUNC.items():
			if buttons == key:
				await eval(f'self.{func}(params)')
				break
			elif buttons:
				await self.get_buttons(params)
		try:
			await self.event.answer(**params)
		except requests.exceptions.ConnectionError:
			time.sleep(1)
			await self.send_message(some_text, buttons)

	#@db_insert(table='Message')
	async def handler_msg(self):
		"""Функция-обработчик событий сервера типа MESSAGE_NEW"""

		await self.send_message_to_all_admins()
		if await self.verify_quiz_training():
			return
		if self.verify_hello():
			await self.send_hello()
		for verify, func in self.VERIFY_FUNC.items():
			x = compile(f'self.{verify}()', 'test', 'eval')
			if eval(x):
				await eval(f'self.{func}()')

	async def send_hello(self):  # ,inline=False):

		def good_time():
			tm = time.ctime()
			pattern = re.compile(r"(\d+):\d+:\d+")
			h = int(pattern.search(tm).group(1))
			h = h + 5 if h < 19 else (h + 5) // 24
			if h < 6:
				return "Доброй ночи"
			elif h < 11:
				return "Доброе утро"
			elif h < 18:
				return "Добрый день"
			elif h <= 23:
				return "Добрый вечер"

		d = [
			'\nНапишите, что бы вы хотели или выберите.',
			'\nНапишите мне, что вас интересует или выберите.',
			'\nЧто вас интересует? Напишите пожалуйста или выберите.'
		]

		t = f"""
		Пока менеджеры {'спят' if good_time() == 'Доброй ночи' else  'заняты'} я могу:
		{self.COMMAND}
		"""

		delta = random.choice(d)
		t1 = f"{good_time()}, {self.user_info['first_name']}!\nЯ бот Oksa-studio.\nБуду рад нашему общению.\n"
		t2 = f"{good_time()}, {self.user_info['first_name']}!\nЯ чат-бот Oksa-studio.\nОчень рад видеть Вас у нас.\n"
		t3 = f"{good_time()}, {self.user_info['first_name']}!\nЯ бот этого чата.\nРад видеть Вас у нас в гостях.\n"
		text = random.choice([t1, t2, t3])

		if self.verify_only_hello():
			await self.send_message(some_text=text)
			await self.send_message(some_text=f'{delta}', buttons='start')
		else:
			await self.send_message(some_text=text)

	async def send_link_entry(self):
		text1 = f"""
		{self.user_info['first_name']}, узнать о свободных местах, своих записях и/или записаться можно:\n
		✔️ Самостоятельно: https://dikidi.net/72910
		✔️ По тел. +7(919)442-35-36
		✔️ Через личные сообщения: @id9681859 (Оксана)
		✔ Дождаться сообщения от нашего менеджера\n
		"""
		text2 = "Что вас еще интересует напишите или выберите ниже:"
		await self.send_message(some_text=text1, buttons='entry_link')
		await self.send_message(some_text=text2, buttons='start')

	async def send_last_service_entry(self):
		if self.msg == "r":
			text_request = f"""
			{self.user_info['first_name']},
			напишите Ваш номер телефона, по которому вы записывались, чтобы найти вашу запись.
			
			Либо введите другую команду:
			{self.COMMAND}
			"""
			await self.send_message(some_text=text_request)
		if self.msg_previous == "r" and self.msg != "r":
			await self.send_message(some_text="Немного подождите. Получаю данные...")
			answer = load_info_client(tel_client=self.msg)
			if answer:
				text_answer = f"""
				{self.user_info['first_name']},
				Дата и время вашей последней записи:
				✔{answer} 
				
				Выберите команду:
				{self.COMMAND}
				"""
			else:
				text_answer = f"""
				{self.user_info['first_name']},
				Извините, но я не нашел у вас ни одной записи.
				Возможно вам нужно уточнить номер телефона.
				
				Для продолжения выберите команду:				
				{self.COMMAND}
				"""
			await self.send_message(some_text=text_answer)

	async def send_price(self):
		text = f"""
		{self.user_info['first_name']}, цены на наши услуги можно посмотреть здесь:
		✔️ vk.com/uslugi-142029999\n
		"""
		text2 = "Что вас еще интересует напишите или выберите ниже:"
		await self.send_message(some_text=text)
		await self.send_message(some_text=text2, buttons='start')

	async def send_contact_admin(self):
		text = f"""
		{self.user_info['first_name']}, мы обязательно свяжемся с Вами в ближайшее время.
		Кроме того, для связи с руководством Вы можете воспользоваться следующими контактами:
		✔ https://vk.com/id448564047
		✔ https://vk.com/id9681859
		✔ Email: oksarap@mail.ru
		✔ Тел.: +7(919)442-35-36\n
		"""
		text2 = "Что вас еще интересует напишите или выберите ниже:"
		await self.send_message(some_text=text)
		await self.send_message(some_text=text2, buttons='start')

	async def send_site(self):
		text = f"""
		{self.user_info['first_name']}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
		https://oksa-studio.ru/\n
		"""
		text2 = "Что вас еще интересует напишите или выберите ниже:"
		await self.send_message(some_text=text)
		await self.send_message(some_text=text2, buttons='start')

	async def send_address(self):
		text1 = f"""
		{self.user_info['first_name']}, мы находимся по адресу:\n
		📍 г.Пермь, ул.Тургенева, д.23.\n
		"""
		text2 = f"""
		Это малоэтажное кирпичное здание слева от ТЦ "Агат" 
		Вход через "Идеал-Лик", большой стеклянный тамбур\n
		Что вас еще интересует напишите или выберите ниже.\n
		"""
		await self.send_message(some_text=text1)
		await self.send_photo('photo-195118308_457239030,photo-142029999_457243624')
		await self.send_message(some_text=text2, buttons='start')

	async def send_bay_bay(self):
		text1 = f"До свидания, {self.user_info['first_name']}. Будем рады видеть вас снова!"
		text2 = f"До скорых встреч, {self.user_info['first_name']}. Было приятно с Вами пообщаться. Ждём вас снова!"
		text3 = f"Всего доброго Вам, {self.user_info['first_name']}. Надеюсь мы ответили на Ваши вопросы. Ждём вас снова! До скорых встреч."
		text = random.choice([text1, text2, text3])
		await self.send_message(some_text=text)

	async def send_work_example(self):
		text = f"""
		{self.user_info['first_name']}, больше работ здесь:
		vk.com/albums-142029999
		Что вас еще интересует напишите или выберите ниже.
		"""
		await self.send_photo()
		await self.send_message(some_text=text, buttons='send_photo')

	async def send_photo(self, photo_id=None):
		attachment = photo_id if photo_id else self.get_photos_example()
		await self.event.answer(attachment=attachment)

	async def send_training(self):
		text =\
			f"{self.user_info['first_name']}, получить подробную информацию о предстоящих курсах" \
			f" и/или записаться вы можете, заполнив анкету предварительной записи," \
			f" которая вас ни к чему не обязывает."
		text2 = "Либо выберите ниже:"

		await self.send_message(some_text=text, buttons='training_buttons')
		await self.send_message(some_text=text2, buttons='start')
