import re


class Verify:

	VERIFY_FUNC = {
		'verify_address': 'send_address',
		'verify_entry': 'send_link_entry',
		'verify_price': 'send_price',
		'verify_contact_admin': 'send_contact_admin',
		'verify_thank_you': 'send_bay_bay',
		'verify_our_site': 'send_site',
		'verify_work_example': 'send_work_example',
		'verify_last_service_entry': 'send_last_service_entry',
		'verify_training': 'send_training',
	}

	def verify_hello(self):
		"""Проверка сообщения на приветствие"""
		pattern = re.compile(r'\b(?:приве?т|здрав?ств?уй|добрый|доброго\s*времени|рад[а?]\s*видеть|start)\w*')
		return bool(pattern.findall(self.msg))

	def verify_only_hello(self):
		"""Проверка на то, что пользователь отправил только приветствие"""
		verify_all = bool(
			self.verify_entry() or
			self.verify_price() or
			self.verify_contact_admin() or
			self.verify_address() or
			self.verify_our_site()
		)
		return bool(self.verify_hello() and not verify_all)

	def verify_last_service_entry(self):
		b1 = bool(self.msg == "r")
		b2 = bool(self.msg_previous == "r")
		b3 = bool(self.msg not in ["z", "r", "p", "h", "ex", "ad", "start"])
		return b1 or b2 and b3

	def verify_entry(self):
		"""Проверка сообщения на вхождение запроса о записи на услугу"""
		pattern = re.compile(r'\b(?:запис|окош|окн[ао]|свобод|хочу\s*нар[ао]стить)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'z')

	def verify_price(self):
		"""Проверка сообщения на запрос прайса на услуги"""
		pattern = re.compile(r'\b(?:прайс|цен[аы]|стоит|стоимост|price)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'p' or self.msg == 'р')

	def verify_contact_admin(self):
		"""Проверка сообщения на запрос связи с администратором"""
		pattern = re.compile(r'\b(?:админ|руковод|директор|начальств|начальник)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'ad')

	def verify_address(self):
		pattern = re.compile(r'\b(?:адрес|вас\s*найти|найти\s*вас|находитесь|добрать?ся|контакты|где\s*ваш\s*офис)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'h')

	def verify_work_example(self):
		pattern = re.compile(r'\b(?:примеры?\s*рабо?т|посмотреть\s*рабо?ты|ваших?\s*рабо?ты?|качество\s*рабо?т|наши работы|смoтреть еще)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'ex')

	def verify_thank_you(self):
		pattern = re.compile(r'\b(?:спасибо|спс|благодар|до\s*свидан|пока)\w*')
		return bool(pattern.findall(self.msg))

	def verify_our_site(self):
		return bool(self.msg == 'наш сайт' or self.msg == 'site')

	def verify_training(self):
		pattern = re.compile(r'\b(?:обучен|обучить?ся|выучить?ся|научить?ся|курс)\w*')
		return bool(pattern.findall(self.msg) or self.msg == 'ed')

	def verify_fsm_quiz_on(self, on_fsm=True):
		pattern_on = re.compile(r'\b(?:анкета|заполнить анкету)\w*')
		pattern_off = re.compile(r'\b(?:отмена|отменить|стоп|stop)\w*')
		if on_fsm:
			return bool(pattern_on.findall(self.msg) and not self.fsm_quiz)
		else:
			return bool(pattern_off.findall(self.msg) and self.fsm_quiz)

	def verify_phone(self):
		pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
		return bool(pattern.findall(self.msg))
