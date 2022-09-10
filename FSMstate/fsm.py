import re
import asyncio

# from vk_agent import Verify


class FSMIterator:
	"""
	Класс итератора шагов квиза
	steps: итерируемый список из кортежей по типу функции self.get_steps_quiz.
	Содержащий:
	- вопрос;
	- ответ в случае не прохождения фильтра;
	- функцию-фильтр.
	"""
	def __init__(
			self,
			steps: list,
	):
		self.steps = steps

	def __iter__(self):
		self.ind = 0
		self.ind_into = True
		return self

	def __next__(self):
		if self.ind == len(self.steps):
			raise StopIteration

		if self.ind > 0 and len(self.steps[self.ind - 1]) > 3:
			verify = self.steps[self.ind - 1][2]()
			if not verify:
				self.ind -= 1
				value = self.steps[self.ind][1]
				self.ind += 1
				return value

		value = self.steps[self.ind][0]
		self.ind += 1
		return value


class FSMQuiz:
	"""
	Класс квиза записи на курс
	"""

	def __init__(self):
		self.data_quiz = {}
		self.data_quiz_list = []
		self.fsm_quiz = False

	def get_steps_quiz(self):
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
				'first_name',
				{'buttons': 'fsm_quiz'},

			),
			(
				"3. Введите вашу фамилию",
				'last_name',
				{'buttons': 'fsm_quiz'},

			),
			(
				"4. Вы уже имеете опыт в наращивании ресниц?",
				'practice',
				{'buttons': 'practic_extention'},
			),
			(
				"5. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите ваш вариант.",
				'work',
				{'buttons': 'what_job'},
			),
			(
				"6. Укажите ваш возраст, либо пропустите данный пункт.",
				f'{self.user_info["first_name"]}, укажите правильное значение, либо пропустите данный пункт, или отмените '
				f'заполнение анкеты.',
				(lambda: bool(self.msg == "пропустить" or (self.msg.isdigit() and 10 < int(self.msg) < 100))),
				'age',
				{'buttons': 'fsm_quiz'},

			),
			(
				f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами и сообщим всю необходимую информацию.',
				{'buttons': 'fsm_quiz'},
			),
		]

	async def set_fsm_quiz(self):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""

		if self.verify_fsm_quiz_on(on_fsm=True):
			self.fsm_quiz = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=self.get_steps_quiz())
			self.iter_quiz = iter(self.step_text)
		elif self.verify_fsm_quiz_on(on_fsm=False):
			self.fsm_quiz = False
			self.data_quiz_list = []
			text_off = f'Спасибо, {self.user_info["first_name"]}. Вы можете продолжить в любое время. Просто отправьте "обучение" или "ed".'
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

	async def send_msg_fsm_quiz(self):
		"""
		Пошаговая отправка сообщений опроса
		"""
		if self.step_count == len(self.get_steps_quiz()):
			self.fsm_quiz = False

		for i, step in enumerate(self.get_steps_quiz(), start=1):
			if self.step_count == i + 1 and len(step) > 3 and not step[2]():
				await self.send_step_msg(buttons='break', verify=True)
				self.fsm_quiz = True
				break
			elif self.step_count == i:
				await self.send_step_msg(**step[-1])
				break

		# if self.step_count == 2 and not self.verify_phone():
		# 	await self.send_step_msg(buttons='break', verify=True)
		# elif self.step_count == 4:
		# 	await self.send_step_msg(buttons='practic_extention')
		# elif self.step_count == 5:
		# 	await self.send_step_msg(buttons='what_job')
		# else:
		# 	await self.send_step_msg(buttons='fsm_quiz')

		if not self.fsm_quiz:
			self.data_quiz_list.append(self.msg)
			data_quiz = [i[-2] for i in self.get_steps_quiz()[:-1]]
			self.data_quiz = dict(zip(data_quiz, self.data_quiz_list[1:]))
			self.data_quiz_list.clear()
			print(self.data_quiz)
			print(self.data_quiz_list)

	async def handler_fsm_quiz(self):
		await self.set_fsm_quiz()
		if self.fsm_quiz:
			await self.send_msg_fsm_quiz()
			return True
