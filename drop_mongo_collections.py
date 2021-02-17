import os

from mongo import collection_additives, collection_stucture, collection_raport

chenge_action = int(input('1 - очистка, 2 - удаление : '))

print(
	'Введите номер соответствующий коллекции: \n '
	'1 - Добавки (общая)  db[Additives]\n '
	'2 - Описания товаров db[Structure]\n '
	'3 - Коллекция отчета db[Raport]\n '
)

number_collection = int(input('Введите номер : '))


def remove_collections(number_collection):
	if number_collection == 1:
		collection_additives.remove()
		os.system('say Коллекция {collection_additives} очищена')
		print('Collections {collection_additives} was removed!')

	elif number_collection == 2:
		collection_stucture.remove()
		os.system('say Коллекция {collection_stucture} очищена')
		print('Collections {collection_stucture} was removed!')

	elif number_collection == 3:
		collection_raport.remove()
		os.system('say Коллекция {collection_raport} очищена')
		print('Collections {collection_raport} was removed!')
	else:
		os.system('say Введите номер коллекции')


def drop_collections(number_collection):
	if number_collection == 1:
		collection_additives.drop()
		os.system('say Коллекция {collection_additives} удалена')
		print('Collections {collection_additives} was Droped!')

	elif number_collection == 2:
		collection_stucture.drop()
		os.system('say Коллекция {collection_stucture} удалена')
		print('Collections {collection_stucture} was Droped!')

	elif number_collection == 3:
		collection_raport.drop()
		os.system('say Коллекция {collection_raport} удалена')
		print('Collections {collection_raport} was Droped!')
	else:
		os.system('say Введите номер коллекции')


def change(chenge_action, number_collection):
	if chenge_action == 1:
		remove_collections(number_collection)
	elif chenge_action == 2:
		drop_collections(number_collection)
	else:
		os.system('say Введите номер')


if __name__ == "__main__":
	change(chenge_action, number_collection)
