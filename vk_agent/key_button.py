from vkwave.bots.utils.keyboards.keyboard import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor


class MyKeyButton:

	async def get_button_func(self):
		return {
			'send_photo': self.get_button_send_photo,
			'fsm_quiz': self.get_button_fsm_quiz,
			'fsm_quiz_inline': self.get_button_fsm_quiz_inline,
			'training_buttons': self.get_button_training,
			'break': self.get_button_break,
			'practic_extention': self.get_practic_extention,
			'what_job': self.get_what_job,
			'entry_link': self.get_entry_link,
			'pass': self.get_button_pass,
			'start': self.get_start,
			'search': self.get_search_our,
			'menu': self.menu,
		}

	@staticmethod
	async def get_buttons(params: dict):

		keyboard = Keyboard(one_time=False, inline=False)
		buttons = ['Записаться', '☰ Menu', 'Обучение', 'Примеры работ']
		buttons_color = [
			ButtonColor.PRIMARY,
			ButtonColor.PRIMARY,
			ButtonColor.SECONDARY,
			ButtonColor.SECONDARY
		]
		for btn, btn_color in zip(buttons[:2], buttons_color[:2]):
			keyboard.add_text_button(btn, btn_color)
		keyboard.add_row()
		for btn, btn_color in zip(buttons[2:], buttons_color[2:]):
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_send_photo(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = ['Смoтреть еще', '☰ MENU']
		btn_color = ButtonColor.PRIMARY
		for btn in buttons:
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_fsm_quiz(params: dict):
		keyboard = Keyboard(one_time=False, inline=False)
		buttons = ['Отмена', 'Пропустить']
		btn_color = ButtonColor.PRIMARY
		for btn in buttons:
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_fsm_quiz_inline(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = ['Пропустить']
		btn_color = ButtonColor.PRIMARY
		for btn in buttons:
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_training(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		keyboard.add_text_button('Заполнить анкету', ButtonColor.PRIMARY)
		keyboard.add_row()
		keyboard.add_text_button('☰ MENU', ButtonColor.SECONDARY)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_break(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = ['Отменить']
		btn_color = ButtonColor.PRIMARY
		for btn in buttons:
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_pass(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons_color = ButtonColor.PRIMARY
		keyboard.add_text_button('Пропустить', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_practic_extention(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = ['Да', 'Нет']
		btn_color = ButtonColor.PRIMARY
		for btn in buttons:
			keyboard.add_text_button(btn, btn_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_what_job(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = [
			'Работаю в сфере красоты',
			'Медицинский работник',
			'Работаю в другой сфере',
			'Домохозяйка',
			'Учусь',
		]
		btn_color = ButtonColor.SECONDARY
		for i, btn in enumerate(buttons, start=1):
			keyboard.add_text_button(btn, btn_color)
			if i != len(buttons):
				keyboard.add_row()
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_start(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = [
			'Записатьcя',
			'Price',
			'Наш адрес',
			'Наши работы',
			'Админ.',
			'Наши курсы',
			'Скидка новичкам'
		]
		btn_color = ButtonColor.SECONDARY
		btn_finish = ButtonColor.PRIMARY
		for i, btn in enumerate(buttons, start=1):
			if i != len(buttons):
				keyboard.add_text_button(btn, btn_color)
			else:
				keyboard.add_text_button(btn, btn_finish)
			if i != len(buttons) and i % 2 == 0:
				keyboard.add_row()
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_entry_link(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		keyboard.add_link_button(text='Запишись ONLINE', link='https://vk.com/app5688600_-142029999/')
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_search_our(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = [
			'По рекомендации',
			'Через Google',
			'Через Yandex',
			'Нашла в 2Gis',
			'Нашла в ВК',
			'Нашла в Instagram'
		]
		btn_color = ButtonColor.SECONDARY
		for i, btn in enumerate(buttons, start=1):
			keyboard.add_text_button(btn, btn_color)
			if i != len(buttons):
				keyboard.add_row()
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def menu(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons_color = ButtonColor.PRIMARY
		keyboard.add_text_button('☰ MENU', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

