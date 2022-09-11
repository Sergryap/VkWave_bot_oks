from vkwave.bots.utils.keyboards.keyboard import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor


class MyKeyButton:

	BUTTON_FUNC = {
		'send_photo': 'get_button_send_photo',
		'fsm_quiz': 'get_button_fsm_quiz',
		'training_buttons': 'get_button_training',
		'break': 'get_button_break',
		'practic_extention': 'get_practic_extention',
		'what_job': 'get_what_job',
		'entry_link': 'get_entry_link',
		'pass': 'get_button_pass',
		'start': 'get_start',
	}

	@staticmethod
	async def get_buttons(params: dict):

		keyboard = Keyboard(one_time=False, inline=False)
		buttons = ['Записаться', 'Start', 'Обучение', 'Примеры работ']
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
		buttons_color = ButtonColor.PRIMARY
		keyboard.add_text_button('Смoтреть еще', buttons_color)
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
	async def get_button_training(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons_color = ButtonColor.PRIMARY
		keyboard.add_text_button('Заполнить анкету', buttons_color)
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_button_break(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		buttons = ['Отменить', 'Пропустить']
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
			'Записатьcя - "z"',
			'Price - "p"',
			'Наш адрес - "h"',
			'Наши работы - "ex"',
			'Администрация - "ad"',
			'Наши курсы - "ed"',
		]
		btn_color = ButtonColor.SECONDARY
		for i, btn in enumerate(buttons, start=1):
			keyboard.add_text_button(btn, btn_color)
			if i != len(buttons):
				keyboard.add_row()
		params['keyboard'] = keyboard.get_keyboard()

	@staticmethod
	async def get_entry_link(params: dict):
		keyboard = Keyboard(one_time=False, inline=True)
		keyboard.add_link_button(text='Запишись ONLINE', link='https://vk.com/app5688600_-142029999/')
		params['keyboard'] = keyboard.get_keyboard()

