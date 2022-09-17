from .fsm import FSMIterator, FSMQuiz
import asyncio


class FSMQuizDiscount:

	TEXT_OFF = 'Вы можете продолжить в любое время. Просто отправьте "получить скидку"'
	OUT_TEXT_PREFIX = "СКИДКА НА ПЕРВОЕ ПОСЕЩЕНИЕ"

	def __init__(self):
		self.data_quiz = {}
		self.data_quiz_list = []
		self.fsm_quiz = False
		self.fsm_discount = True

	def get_steps_quiz_discount(self):
		return [
			(
				f"1. {self.user_info['first_name']}, оставьте пожалуйста ваш контактный номер телефона:",
				"Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты",
				self.verify_phone,
				'phone',
				{'buttons': 'fsm_quiz'},

			),
			(
				"2. Введите ваше имя",
				'name',
				{'buttons': 'fsm_quiz'},

			),
			(
				"3. Как вы нас нашли? Выберите ниже, либо напишите свой вариант",
				f"{self.user_info['first_name']}, данный пункт обязателен к заполнению. Укажите вариант, либо отмените заполнение анкеты",
				lambda: self.msg != "пропустить",
				'search',
				{'buttons': 'search'},
			),
			(
				"4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.",
				'work',
				{'buttons': 'what_job'},
			),
			(
				"5. Укажите ваш возраст, либо пропустите данный пункт.",
				f'{self.user_info["first_name"]}, укажите правильное значение, либо пропустите данный пункт, или отмените '
				f'заполнение анкеты.',
				lambda: bool(self.msg == "пропустить" or (self.msg.isdigit() and 10 < int(self.msg) < 100)),
				'age',
				{'buttons': 'fsm_quiz'},

			),
			(
				f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами,'
				f' сообщим всю необходимую информацию и подберем удобное время для записи со скидкой.',
				{'buttons': 'fsm_quiz'},
			),
		]

	async def set_fsm_quiz_discount(self):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""
		#  Проверка на включение:
		if self.verify_fsm_quiz_on(on_fsm=True):
			self.fsm_quiz = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=self.get_steps_quiz_discount())
			self.iter_quiz = iter(self.step_text)

		#  Проверка на выключение:
		elif self.verify_fsm_quiz_on(on_fsm=False):
			self.fsm_quiz = False
			self.data_quiz_list = []
			# если была отмена, то отправляем сообщенние пользователю
			text_off = f'Спасибо, {self.user_info["first_name"]}. {self.TEXT_OFF}.'
			await self.send_message(some_text=text_off, buttons=True)

	async def send_step_msg(self, buttons, verify=False):
		"""
		Обработка конкретного шага при прохождении фильтра
		"""
		if not verify:
			self.step_count += 1
			buttons = buttons if self.fsm_quiz else True
			self.data_quiz_list.append(self.msg)
		text = next(self.iter_quiz)
		await self.send_message(some_text=text, buttons=buttons)

	async def send_msg_fsm_quiz_discount(self):
		"""
		Пошаговая отправка сообщений опроса
		"""
		if self.step_count == len(self.get_steps_quiz_discount()):
			self.fsm_quiz = False
			self.fsm_discount = False

		for i, step in enumerate(self.get_steps_quiz_discount(), start=1):
			if self.step_count == i + 1 and len(step) > 3 and not step[2]():
				await self.send_step_msg(buttons='break', verify=True)
				self.fsm_quiz = True
				self.fsm_discount = True
				break
			elif self.step_count == i:
				await self.send_step_msg(**step[-1])
				break

		if not self.fsm_quiz:
			self.data_quiz_list.append(self.msg)
			data_quiz = [i[-2] for i in self.get_steps_quiz_discount()[:-1]]
			self.data_quiz = dict(zip(data_quiz, self.data_quiz_list[1:]))
			self.data_quiz_list.clear()
			text = "СКИДКА НА ПЕРВОЕ ПОСЕЩЕНИЕ\n"
			for key, value in self.data_quiz.items():
				text += f'{key}: {value}\n'
			await self.send_message_to_all_admins(text=text)

	async def handler_fsm_quiz_discount(self):
		# назначаем или проверяем флаг состояния машины состояния перед каждым шагом
		await self.set_fsm_quiz_discount()
		if self.fsm_quiz:
			await self.send_msg_fsm_quiz_discount()
			return True
