import random
import time
import re


class SendMSG:

	async def send_message(self, some_text, buttons=True):
		"""
		Отправка сообщения пользователю.
		Если buttons=True создается клавиатура
		"""
		params = {
			"message": some_text,
			"keyboard": None}
		button_func = await self.get_button_func()
		for key, func in button_func.items():
			if buttons == key:
				await func(params)
				break
			elif buttons:
				await self.get_buttons(params)
		try:
			await self.event.answer(**params)
		except requests.exceptions.ConnectionError:
			time.sleep(1)
			await self.send_message(some_text, buttons)

	async def send_hello(self):

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
		Пока менеджеры {'спят' if good_time() == 'Доброй ночи' else 'заняты'} я могу:
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
		await self.send_message(some_text=text2, buttons='menu')

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
		await self.send_message(some_text=text2, buttons='menu')

	async def send_site(self):
		text = f"""
		{self.user_info['first_name']}, много полезной информации о наращивании ресниц смотрите на нашем сайте:
		https://oksa-studio.ru/\n
		"""
		text2 = "Что вас еще интересует напишите или выберите ниже:"
		await self.send_message(some_text=text)
		await self.send_message(some_text=text2, buttons='menu')

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
		await self.send_message(some_text=text2, buttons='menu')

	async def send_bay_bay(self):
		text1 = f"До свидания, {self.user_info['first_name']}. Будем рады видеть вас снова!"
		text2 = f"До скорых встреч, {self.user_info['first_name']}. Было приятно с Вами пообщаться. Ждём вас снова!"
		text3 = f"Всего доброго Вам, {self.user_info['first_name']}. Надеюсь мы ответили на Ваши вопросы. Ждём вас снова! До скорых встреч."
		text = random.choice([text1, text2, text3])
		await self.send_message(some_text=text, buttons='menu')

	async def send_work_example(self):
		text = f"""
		{self.user_info['first_name']}, больше работ здесь:
		vk.com/albums-142029999
		Что вас еще интересует напишите или выберите ниже.
		"""
		await self.send_photo()
		await self.send_message(some_text=text, buttons='send_photo')

	async def send_photo(self, photo_id=None):
		attachment = photo_id if photo_id else await self.get_photos_example()
		await self.event.answer(attachment=attachment)

	async def send_training(self):
		text = \
			f"{self.user_info['first_name']}, получить подробную информацию о предстоящих курсах" \
			f" и/или записаться вы можете, заполнив анкету предварительной записи," \
			f" которая вас ни к чему не обязывает."

		await self.send_message(some_text=text, buttons='training_buttons')

	async def send_discount(self):
		text = \
			f"{self.user_info['first_name']}, заполните анкету и получите скидку на первое посещение 15%.\n" \
			f"Скидка доступна только для первой записи в нашу студию.\n" \
			f"Будем рады вас видеть!"

		await self.send_message(some_text=text, buttons='training_buttons')

	async def send_menu(self):
		text = "Выберите ниже:"
		await self.send_message(some_text=text, buttons='start')
