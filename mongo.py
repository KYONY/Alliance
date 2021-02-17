import os
import ssl
from datetime import datetime

import pymongo as pymongo
from credentails import MONGO_URL

client = pymongo.MongoClient(MONGO_URL, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client['Alliance']

collection_additives = db['Additives']  # Данные о добавках и ключевых словах
collection_stucture = db['Structure']  # Описание продактов предоставленное производителями
collection_raport = db['Raport']  # Данные для обработки перед записью в excel


def finish(command: str):
	os.system(f'say {command}')


def search_by_phrase(collection: str, field: str, language: str, keyword: str):
	"""производит поиск соответствия ключевой фразы по коллекции. Принимает:
	collection - название коллекции в БД (collection=collection_stucture)
	field - название поля коллекции в котором будет производиться поиск field='content'
	language - язык на котором будет производиться поиск (language='russian')(language='english')
	keyword - поисковое слово или фраза по которой будет вестись поиск keyword='спирт'
	Пример:
	search(collection=collection_stucture, field='content',language='russian', keyword='спирт')
	"""
	collection.create_index([(field, 'text')], default_language=language)
	"""создаем индекс для поиска в БД"""
	for i in collection_stucture.find(
			{"$text": {"$search": keyword}},
			{'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})]):
		print(i)
	collection.drop_index([(field, 'text')])
	"""по окончании поиска/ перед началом поиска по следующему ключевому слову индуекс следует удалить, 
	иначе будет ошибка!!!"""
	"""{'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})]) - параметр, обеспечивающий
	сортировку по реличантности вхождения поисковой фразы"""


def search_by_keyword(collection: str, field: str, language: str, keyword: str):
	collection.create_index([(field, 'text')], default_language=language)
	for i in collection_stucture.find({"$text": {"$search": keyword}}):
		print(i)
	collection.drop_index([(field, 'text')])


class Consolidated(object):
	def __init__(self) -> None:
		self.id = None
		self.list_e_index = {}
		self.list_product_id = {}
		self.list_keywords = {}
		self.list_verified_keywords = {}
		self.list_not_verified_keywords = {}
		self.total_list_e_indexes = {}
		self.one_e_index = None
		self.one_product_id = None
		self.keyword_additive = None
		self.full_description = None
		self.rest_of_description = None


consolidated = Consolidated()


def drop_index(field_of_document_for_search: str):
	collection_stucture.drop_index([(field_of_document_for_search, 'text')])


def timeit(func):
	"""Декоратор для определения времени выполнения функции"""

	def wrapper(*args, **kwargs):
		start = datetime.now()
		result = func(*args, **kwargs)
		print('')
		print('Duration - ', datetime.now() - start)
		return result

	return wrapper


def search_file_in_dir(incoming_dir: str):
	"""Определяет путь к первому файлу в дирректории"""
	path_dir = os.listdir(incoming_dir)[0]
	path_file = incoming_dir + '/' + path_dir
	return path_file
