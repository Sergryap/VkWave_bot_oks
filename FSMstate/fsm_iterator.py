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
