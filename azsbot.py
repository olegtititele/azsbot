import telebot
from telebot import *
import random
import os
from extra.yoomoneypayment import YooMoney
from extra.create_hatch import Stroke
from extra.qiwi_data import Qiwi
import extra.main_data as md
import uuid
import time



apihelper.proxy = {'https':'socks5h://' + md.PROXY}


bot = telebot.TeleBot(md.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
	photo = open('backgrn.jpg', 'rb')
	markup = types.InlineKeyboardMarkup()
	item = types.InlineKeyboardButton('‼️Информация‼️', callback_data='info')
	markup.add(item)
	for key in md.goods_dict:
		callback_data = key
		item = types.InlineKeyboardButton(key, callback_data=callback_data)
		markup.add(item)
	bot.send_photo(message.chat.id, photo, caption="*Добро пожаловать в нашего бота*", reply_markup=markup, parse_mode="Markdown")




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	
	try:
		if call.message:

			# Первый шаг
			for key in md.goods_dict:
				if call.data == key:
					for i in md.goods_dict[key]:
						return inline_keyboard(call, md.goods_dict[key])


			# Второй шаг
			for key in md.goods_dict:
				for i in md.goods_dict[key]:
					if call.data == i:
						for y in md.price_dict:
							return inline_keyboard(call, md.price_dict)		


			# Информация
			if call.data == 'info':
				photo = open('backgrn.jpg', 'rb')
				markup = types.InlineKeyboardMarkup()
				item = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
				markup.add(item)
				bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo,parse_mode="Markdown", caption = "*Хочешь экономить на продуктах и бензине?\nБаллы пятёрочки, перекрёстка, магнита с помощью которых вы можете купить товар за копейки.\nБаллы лукойла и роснефти с помощью которых можно покупать бензин в 2 раза дешевле!!!! Балансы от 200р до 7000р за 40-50% от номинала!*\n_‼️Валид 100%, все АШ проверяются в момент выдачи‼️\n‼️Подробное описание и правила использования.‼️\n‼️Оповещение о скидках и раздачах на товар‼️\n‼️Часто выпадают балансы больше заявленного‼️_"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

			# Вернуться в меню
			elif call.data == 'back':
				back_to_meny(call, md.goods_dict)


			# Переход в меню после оплаты
			elif call.data == 'back_new_mess':
				photo = open('backgrn.jpg', 'rb')
				markup = types.InlineKeyboardMarkup()
				item = types.InlineKeyboardButton('‼️Информация‼️', callback_data='info')
				markup.add(item)
				for key in md.goods_dict:
					callback_data = key
					item = types.InlineKeyboardButton(key, callback_data=callback_data)
					markup.add(item)
				bot.send_photo(call.message.chat.id, photo, caption="*Вы перешли в меню*",reply_markup=markup, parse_mode="Markdown")	

			# Цены за товары
			for key in md.price_dict:
				if call.data == key:
					return pay_petrol(call, key, md.price_dict, md.price_dict[key])
			
			# Покупка товаровuuid.uuid4().hexstr(random.randint(100000000000,999999999999))
			for key in md.price_dict:
				if call.data == md.price_dict[key]:
					random_label = uuid.uuid4().hex
					summ = int(md.price_dict[key])
					check = YooMoney(random_label)
					make_p = check.make_payment(summ)
					checkqiwi = Qiwi(random_label, summ)
					make_qiwi = checkqiwi.make_payment()
					photo = open('backgrn.jpg', 'rb')
					markup = types.InlineKeyboardMarkup()
					item1 = types.InlineKeyboardButton('ЯндексДеньги', url=make_p)
					item2 = types.InlineKeyboardButton('QIWI', url=make_qiwi)
					back_item = types.InlineKeyboardButton('⚙️Вернуться в меню⚙️', callback_data='back')
					markup.add(item1, item2)
					markup.add(back_item)
					msg = bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, parse_mode="Markdown", caption = "*Оплатите "+ md.price_dict[key]+"₽* _(Оплата подтвердится автоматически)_\n"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
					bot.register_next_step_handler(msg, check_status(call, random_label, md.price_dict[key], make_p, key, summ))


	except Exception as e:
		print(repr(e))

# Проверка статуса заказа
def check_status(call, label, value, url, key, summ):

	check = YooMoney(label)
	checkqiwi = Qiwi(label, summ)
	photo = open('backgrn.jpg', 'rb')
	markup = types.InlineKeyboardMarkup()
	item = types.InlineKeyboardButton('⚙️Вернуться в меню⚙️', callback_data='back')
	markup.add(item)
	if check.check_payment() == 'success' or checkqiwi.check_payment() == 'PAID':
		create_qr(call, key)
	else:
		time.sleep(5)
		check_status(call, label, value, url, key, summ)

# Вернуться в меню(изменить сообщение)
def back_to_meny(call, arr):
	photo = open('backgrn.jpg', 'rb')
	markup = types.InlineKeyboardMarkup()
	item = types.InlineKeyboardButton('‼️Информация‼️', callback_data='info')
	markup.add(item)
	for i in arr:
		callback_data = i
		item = types.InlineKeyboardButton(i, callback_data=callback_data)
		markup.add(item)
	bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, parse_mode="Markdown", caption = "*Вы перешли в меню*"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


# Для покупки
def pay_petrol(call, key, arr, price):
	photo = open('backgrn.jpg', 'rb')
	markup = types.InlineKeyboardMarkup()
	callback_data = price
	item = types.InlineKeyboardButton("Оплатить " + callback_data + '₽', callback_data=callback_data)
	item1 = types.InlineKeyboardButton('⚙️Вернуться в меню⚙️', callback_data='back')
	markup.add(item)
	markup.add(item1)
	bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, parse_mode="Markdown", caption = "*Вы выбрали " + key + "*"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# Инлайн клавиатура
def inline_keyboard(call, arr):
	photo = open('backgrn.jpg', 'rb')
	markup = types.InlineKeyboardMarkup()
	for i in arr:
		callback_data = i
		item = types.InlineKeyboardButton(i, callback_data=callback_data)
		markup.add(item)
	item = types.InlineKeyboardButton('⚙️Вернуться в меню⚙️', callback_data='back')
	markup.add(item)
	bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, parse_mode="Markdown", caption = "*Выберите из списка нужный товар:*"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# Отправка QR

def create_qr(call, key):
	try:
		markup = types.InlineKeyboardMarkup()
		item = types.InlineKeyboardButton('⚙️Вернуться в меню⚙️', callback_data='back_new_mess')
		markup.add(item)
		price = key.split('(')[0]
		lineCode = str(random.randint(100000000000,999999999999))
		stoke = Stroke('qrcode/', lineCode, ".png")
		photo = stoke.create_rand_hatch()
		bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, parse_mode="Markdown", caption = "*Оплата прошла - " + price + "*\n_‼️Покажите на кассе штрихкод и скажите, что хотите списать баллы‼️_"), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
		photo.close()
		os.remove('qrcode/'+lineCode+".png")
	except Exception as e:
		print(repr(e))


bot.infinity_polling()
