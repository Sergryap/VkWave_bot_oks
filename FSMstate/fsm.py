import re
import asyncio

from .fsm_iterator import FSMIterator


class FSMQuiz:
	"""
	Класс машины состояния
	"""


	def __init__(self):
		self.data_quiz = {}
		self.data_quiz_list = []
		self.fsm_quiz = False  # флаг состояния машины состояния
		self.verify_quiz = self.verify_fsm_quiz_on  # функция условия вкл/выкл машины состояния

	def get_steps_quiz_training(self):
		"""
		Пункты анкеты на запись на курс
		"""
		return [
			(
				f"1. {self.user_info['first_name']}, оставьте пожалуйста ваш контактный номер телефона:",
				"Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты",
				self.verify_phone,
				'phone',
				{'buttons': 'break'},
				{'buttons': 'fsm_quiz'},
			),
			(
				"2. Введите ваше имя",
				'name',
				{'buttons': 'fsm_quiz_inline'},

			),
			(
				"3. Вы уже имеете опыт в наращивании ресниц?",
				'practice',
				{'buttons': 'practic_extention'},
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
				(lambda: bool(self.msg == "пропустить" or (self.msg.isdigit() and 10 < int(self.msg) < 100))),
				'age',
				{'buttons': 'fsm_quiz_inline'},

			),
			(
				f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами и сообщим всю необходимую информацию.',
				{'buttons': 'fsm_quiz_inline'},
			),
		]

	def get_steps_quiz_discount(self):
		"""
		Пункты анкеты на запись со скидкой
		"""
		return [
			(
				f"1. {self.user_info['first_name']}, оставьте пожалуйста ваш контактный номер телефона:",
				"Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты",
				self.verify_phone,
				'phone',
				{'buttons': 'break'},
				{'buttons': 'fsm_quiz'},
			),
			(
				"2. Введите ваше имя",
				'name',
				{'buttons': 'fsm_quiz_inline'},

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
				{'buttons': 'fsm_quiz_inline'},

			),
			(
				f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами,'
				f' сообщим всю необходимую информацию и подберем удобное время для записи со скидкой.',
				{'buttons': 'fsm_quiz_inline'},
			),
		]

	async def set_fsm_quiz(self, flag_fsm, text_off, steps_quiz):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""
		#  Проверка на включение:
		if self.verify_quiz(on_fsm=True):
			self.fsm_quiz = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=steps_quiz())
			self.iter_quiz = iter(self.step_text)
			setattr(self, flag_fsm, True)

		#  Проверка на выключение:
		elif self.verify_quiz(on_fsm=False):
			self.fsm_quiz = False
			self.data_quiz_list = []
			setattr(self, flag_fsm, False)
			# если была отмена, то отправляем сообщенние пользователю
			text_off = f'Спасибо, {self.user_info["first_name"]}. {text_off}.'
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

	async def send_msg_fsm_quiz(self, flag_fsm, out_text_prefix, steps_quiz):
		"""
		Пошаговая отправка сообщений опроса
		"""
		if self.step_count == len(steps_quiz()):
			self.fsm_quiz = False
			setattr(self, flag_fsm, False)

		for i, step in enumerate(steps_quiz(), start=1):
			if self.step_count == i + 1 and len(step) > 3 and not step[2]():
				await self.send_step_msg(**(step[-2] if len(step) > 5 else step[-1]), verify=True)
				self.fsm_quiz = True
				setattr(self, flag_fsm, True)

				break
			elif self.step_count == i:
				await self.send_step_msg(**step[-1])
				break

		if not self.fsm_quiz:
			self.data_quiz_list.append(self.msg)
			data_quiz = [i[-2] if len(i) < 6 else i[-3] for i in steps_quiz()[:-1]]
			self.data_quiz = dict(zip(data_quiz, self.data_quiz_list[1:]))
			self.data_quiz_list.clear()
			text = f'{out_text_prefix}:\nuser: vk.com/id{self.user_id}\n'
			for key, value in self.data_quiz.items():
				text += f'{key}: {value}\n'
			await self.send_message_to_all_admins(text=text)

	async def handler_fsm_quiz(
			self,
			verify_func,
			steps_quiz,
			flag_fsm: str,
			text_off: str,
			out_text_prefix: str,
	) -> bool:
		# проверяем находимся ли в режиме машины состояния:
		if verify_func(previous=True) or getattr(self, flag_fsm):
			# назначаем и/или проверяем флаг состояния машины состояния перед каждым шагом
			await self.set_fsm_quiz(flag_fsm, text_off, steps_quiz)
			if self.fsm_quiz:
				await self.send_msg_fsm_quiz(flag_fsm, out_text_prefix, steps_quiz)
				return True

	async def fsm_state(self):
		if await self.handler_fsm_quiz(
			verify_func=self.verify_training,
			steps_quiz=self.get_steps_quiz_training,
			flag_fsm='fsm_training',
			text_off='Вы можете продолжить в любое время. Просто отправьте "обучение" или "ed"',
			out_text_prefix="ЗАЯВКА НА ОБУЧЕНИЕ",
		):
			return True

		if await self.handler_fsm_quiz(
			verify_func=self.verify_discount,
			steps_quiz=self.get_steps_quiz_discount,
			flag_fsm='fsm_discount',
			text_off='Вы можете продолжить в любое время. Просто отправьте "получить скидку"',
			out_text_prefix="СКИДКА НА ПЕРВОЕ ПОСЕЩЕНИЕ",
		):
			return True
