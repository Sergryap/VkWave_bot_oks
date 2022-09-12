import asyncio


class HandlerFSM:

	async def handler_msg_fsm(self, context):

		steps_fsm = {
			'phone': {
				'msg': {
					'on': f"1. {self.user_info['first_name']}, оставьте пожалуйста ваш контактный номер телефона:",
					'off': "Укажите номер телефона в верном формате, например: 7(999)999-99-99. Либо отмените заполнение анкеты",
				},
				'buttons': {
					'on': 'fsm_quiz',
					'off': 'break'
				}
			},
			'name': {
				'msg': {
					'on': '2. Введите ваше имя',
					'off': None,
				},
				'buttons': {
					'on': 'fsm_quiz',
					'off': None
				}
			},
			'practice': {
				'msg': {
					'on': '3. Вы уже имеете опыт в наращивании ресниц?',
					'off': None,
				},
				'buttons': {
					'on': 'practic_extention',
					'off': None
				}
			},
			'work': {
				'msg': {
					'on': '4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.',
					'off': None,
				},
				'buttons': {
					'on': 'what_job',
					'off': None
				}
			},
			'age': {
				'msg': {
					'on': '5. Укажите ваш возраст, либо пропустите данный пункт.',
					'off': f'{self.user_info["first_name"]}, укажите правильное значение, либо пропустите данный пункт, или отмените заполнение анкеты',
				},
				'buttons': {
					'on': 'fsm_quiz',
					'off': 'break'
				}
			},
			'finish': {
				'msg': {
					'on': f'Спасибо, {self.user_info["first_name"]}, мы обязательно свяжемся с вами и сообщим всю необходимую информацию.',
					'off': None,
				},
				'buttons': {
					'on': True,
					'off': None
				}
			},
			'break': {
				'msg': {
					'on': f'Спасибо, {self.user_info["first_name"]}, вы можете продолжить в любое время.',
					'off': None,
				},
				'buttons': {
					'on': True,
					'off': None
				}
			},
		}

		params = {
			"message": steps_fsm[context['step']]['msg'][context['status']],
			"keyboard": None}

		buttons = steps_fsm[context['step']]['buttons'][context['status']]

		for key, func in self.BUTTON_FUNC.items():
			if buttons == key:
				await eval(f'self.{func}(params)')
				break
			elif buttons:
				await self.get_buttons(params)

		return params

