from .fsm import FSMQuiz


class FSMQuizTraining(FSMQuiz):

	def __init__(self):
		super().__init__()
		self.verify_quiz = self.verify_fsm_quiz_on

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
				'name',
				{'buttons': 'fsm_quiz'},

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
				{'buttons': 'fsm_quiz'},

			),
			(
				f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами и сообщим всю необходимую информацию.',
				{'buttons': 'fsm_quiz'},
			),
		]