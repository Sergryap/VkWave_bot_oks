import re
import asyncio
from .fsm_iterator import FSMIterator


class FSMQuiz:
	"""
	Базовый класс квиза
	"""

	TEXT_OFF = 'Вы можете продолжить в любое время. Просто отправьте "обучение" или "ed"'

	def __init__(self):
		self.data_quiz = {}
		self.data_quiz_list = []
		self.fsm_quiz = False
		self.verify_quiz = self.verify_fsm_quiz_on

	def get_steps_quiz(self):
		pass

	async def set_fsm_quiz(self):
		"""
		Включение/выключение машины состояния опроса записи на обучающий курс
		"""

		if self.verify_quiz(on_fsm=True):
			self.fsm_quiz = True
			self.step_count = 1
			self.step_text = FSMIterator(steps=self.get_steps_quiz())
			self.iter_quiz = iter(self.step_text)
		elif self.verify_quiz(on_fsm=False):
			self.fsm_quiz = False
			self.data_quiz_list = []
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

	async def handler_fsm_quiz_training(self):
		await self.set_fsm_quiz()
		if self.fsm_quiz:
			await self.send_msg_fsm_quiz()
			return True
