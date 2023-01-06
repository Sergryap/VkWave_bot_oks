import requests
import json
import os
import random

# from Data_base.DecorDB import db_insert
# from Data_base.DecorDB import DBConnect
from .photos import photos


class VkApi: #  (DBConnect):
    """Класс методов из api VK"""

    url = 'https://api.vk.com/method/'
    with open(os.path.join("vk_agent", ".token"), encoding='utf-8') as file:
        token = [t.strip() for t in file.readlines()]

    def __init__(self):
        super().__init__()
        self.params = {'access_token': self.token[0], 'v': '5.131'}
        self.author = 0

    def __set_params(self, zero=True):
        """Установка параметров для get запроса при неудачном запросе"""
        self.author = 0 if zero else self.author + 1
        print(f'Токен заменен на >>> {self.author}!')
        self.params = {'access_token': self.token[self.author], 'v': '5.131'}

    def get_stability(self, method, params_delta, i=0):
        """
        Метод get запроса с защитой на случай блокировки токена
        При неудачном запросе делается рекурсивный вызов
        с другим токеном и установкой этого токена по умолчанию
        через функцию __set_params
        Для работы функции необходим текстовый файл .token с построчно записанными токенами
        В первую строку заносится токен от чат-бота.
        """
        print(f'Глубина рекурсии: {i}/токен: {self.author}')
        method_url = self.url + method
        response = requests.get(method_url, params={**self.params, **params_delta}).json()
        if 'response' in response:
            return response
        elif i == len(self.token) - 1:
            return False
        elif self.author < len(self.token) - 1:
            self.__set_params(zero=False)
        elif self.author == len(self.token) - 1:
            self.__set_params()
        count = i + 1  # счетчик стэков вызова
        return self.get_stability(method, params_delta, i=count)

    # @db_insert(table="Client")
    # def get_info_users(self):
    #     """
    #     Получение данных о пользователе по его id
    #     :return: словарь с данными по пользователю
    #     """
    #     print(f"Получение данных о пользователе: {self.user_id}")
    #     params_delta = {'user_ids': self.user_id, 'fields': 'country,city,bdate,sex'}
    #     response = self.get_stability('users.get', params_delta)
    #     if response:
    #         birth_date = self.get_birth_date(response)
    #         return {
    #             'user_id': self.user_id,
    #             'city_id': None if not response['response'][0].get('city') else response['response'][0]['city'].get('id'),
    #             'sex': response['response'][0]['sex'],
    #             'first_name': response['response'][0]['first_name'],
    #             'last_name': response['response'][0]['last_name'],
    #             'bdate': birth_date,
    #         }

    async def get_info_users(self):
        """
        Получение данных о пользователе по его id
        :return: словарь с данными по пользователю
        """
        print(f"Получение данных о пользователе: {self.user_id}")
        api = self.event.api_ctx
        user_info = (await api.users.get(user_ids=self.user_id, fields='country,city,bdate,sex')).response[0]
        return {
           'user_id': self.user_id,
           'city_id': None if not user_info.city else user_info.city.id,
           'first_name': user_info.first_name,
           'last_name': user_info.last_name,
           'bdate': user_info.bdate,
       }

    @staticmethod
    def get_birth_date(res: dict):
        """
        Получение данных о возрасте пользователя
        :return: кортеж с датой: str и годом рождения: int
        """
        birth_date = None if 'bdate' not in res['response'][0] else res['response'][0]['bdate']
        if birth_date:
            birth_date = None if len(birth_date.split('.')) < 3 else birth_date
        return birth_date

    def __albums_id(self, owner_id):
        """
        Cоздает список, содержащий id альбомов пользователя
        """
        params_delta = {'owner_id': owner_id, 'need_system': ''}
        response = self.get_stability('photos.getAlbums', params_delta)
        if response and response['response']['items']:
            albums_id = []
            for item in response['response']['items']:
                albums_id.append(item['id'])
            return albums_id

    def __photos_get(self, owner_id, album_id):
        """
        Получение данных по фотографиям из одного альбома (album_id) пользователя (owner_id)
        :return: список содержащий id photo
        """
        params_delta = {'owner_id': owner_id, 'album_id': album_id, 'extended': 1}
        response = self.get_stability('photos.get', params_delta)
        if response:
            photos_info = []
            for item in response['response']['items']:
                photos_info.append(f"photo{owner_id}_{item['id']}")
            return photos_info

    def get_photos_total(self):
        albums = self.__albums_id('-142029999')
        all_photos = []
        for album in albums:
            all_photos += self.__photos_get('-142029999', album)
        return all_photos

    @staticmethod
    async def get_photos_example():
        attachment = ''
        for photo in random.sample(photos, 5):
            attachment += f"{photo},"
        return attachment[:-1]

    async def send_message_to_all_admins(self, msg_error=None, text=False):
        """
        Отправка сообщений всем админам из self.user_ids
        """

        if msg_error:
            text = f"Ошибка в работе бота oksa_studio: {msg_error}"
        elif not text:
            text = f"""
            Сообщение от пользователя https://vk.com/id{self.user_id} в чате https://vk.com/gim142029999 "{self.msg}"
            """
        # params = {
        #     "user_ids": self.user_ids,
        #     "message": text,
        #     "random_id": 0,
        #     'access_token': TOKEN, 'v': '5.131'
        # }
        # method_url = self.url + 'messages.send'
        # requests.get(method_url, params=params)

        api = self.event.api_ctx
        params = {
            "user_ids": self.user_ids,
            "message": text,
            "random_id": 0
        }
        await api.messages.send(**params)


