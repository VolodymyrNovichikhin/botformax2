import telebot #імпортували набір інструментів
from telebot import types # інструменти для кнопок


token='6506341574:AAG6IW3RDPmsEYGw29714iCyZMUzg-71w-0' #токен бота

vovka=telebot.TeleBot(token)  #створення помічника Вовка (обєкту класа Telebot)

keyboard_menu=types.ReplyKeyboardMarkup(resize_keyboard=True)
tovar=types.KeyboardButton('Товари📦')
cart=types.KeyboardButton('Кошик🧺')
contacts=types.KeyboardButton('Контакти📞')
keyboard_menu.add(tovar, cart, contacts)

@vovka.message_handler(commands=['start'])
def start(message):
    vovka.send_message(message.chat.id, 'Меню:',reply_markup=keyboard_menu)
    new_order = open(f'orders/new_order_{message.chat.id}.txt', 'w')
    new_order.close()


@vovka.message_handler(content_types=['text'])# вчимо Вовку обробляти текстові повідомлення
def menu_check(message): # Функція обробки
#Умови
#   if message.text=='Hello':
#      vovka.send_message(message.chat.id, "Hello, user")
    #if message.text=='Hello':
       # print(message.chat.id)
        #vovka.send_message(message.chat.id,'Hello')
    if message.text=='Товари📦':
        keyboard_category=types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone=types.KeyboardButton('Телефони📱')
        tv=types.KeyboardButton('Телевізори📺')

        menu=types.KeyboardButton('🔙Меню')

        keyboard_category.add(phone,tv,menu)
        vovka.send_message(message.chat.id,'Оберіть категорію:',reply_markup=keyboard_category)
    if message.text=='Кошик🧺':
        file_cart=open(f'orders/new_order_{message.chat.id}.txt','r')
        cart=file_cart.read().split('\n')
        file_cart.close()
        message_text=''
        total_price=0
        for element in cart:
            if element:
                text_pass = element.split(';')
                total_price=total_price+int(text_pass[2].replace('$',''))#Додаємо до загальної суми вартість товару
                message_text=message_text+f'{text_pass[0]} - {text_pass[1]}, ціна:{text_pass[2]}\n'#Гарно виводимо дані у текст повідомлення
        message_text=message_text+f'Загальна сума:{total_price}$'
        orders_keyboard=types.InlineKeyboardMarkup()
        orders_button=types.InlineKeyboardButton(text='Оформити замовлення',callback_data='Оформити')
        orders_keyboard.add(orders_button)
        vovka.send_message(message.chat.id, message_text,reply_markup=orders_keyboard)

    if message.text=='Контакти📞':
        vovka.send_message(message.chat.id,'м.Київ\nвул.Хрещатик,23\nтел.(050) 583-33-45\ne-mail:firstbot@i.ua')
    if message.text=='🔙Меню':
        vovka.send_message(message.chat.id, 'Меню:',reply_markup=keyboard_menu)
    if message.text=='Телефони📱':
        file_phone=open('phone.txt','r')
        db_phone=file_phone.read().split('\n')
        file_phone.close()
        phone_keyboard = types.InlineKeyboardMarkup()
        for schumacher in db_phone:
            text_pass=schumacher.split(';')#Iphone 15 128gb 1100$
            button=types.InlineKeyboardButton(text=f'{text_pass[0]} - {text_pass[1]}, ціна:{text_pass[2]}',callback_data=schumacher)
            phone_keyboard.add(button)
        vovka.send_message(message.chat.id, 'Категорія Телефони📱:',reply_markup=phone_keyboard)
    if message.text=='Телевізори📺':
        file_phone=open('tv.txt','r')
        db_phone=file_phone.read().split('\n')
        file_phone.close()
        phone_keyboard = types.InlineKeyboardMarkup()
        for schumacher in db_phone:
            text_pass=schumacher.split(';')
            button=types.InlineKeyboardButton(text=f'{text_pass[0]} - {text_pass[1]}, ціна:{text_pass[2]}',callback_data=schumacher)
            phone_keyboard.add(button)
        vovka.send_message(message.chat.id, 'Категорія Телевізори📺:',reply_markup=phone_keyboard)



@vovka.callback_query_handler(func=lambda call:True)
def call_data_me(call):
    if call.data:
        if call.data=='Оформити':
            user_number=vovka.send_message(call.message.chat.id,'Залишіть свій номер телефону для дзвінка менеджера')
            vovka.register_next_step_handler(user_number,check_order)
        else:
            new_order=open(f'orders/new_order_{call.message.chat.id}.txt','a')
            new_order.write(call.data+'\n')
            new_order.close()
            text_pass = call.data.split(';')
            vovka.send_message(call.message.chat.id,f'{text_pass[0]}-{text_pass[1]} Додано до кошика!')
def check_order(message):
    file_cart = open(f'orders/new_order_{message.chat.id}.txt', 'r')
    cart = file_cart.read().split('\n')
    file_cart.close()
    message_text = ''
    total_price = 0
    for element in cart:
        if element:
            text_pass = element.split(';')
            total_price = total_price + int(text_pass[2].replace('$', ''))  # Додаємо до загальної суми вартість товару
            message_text = message_text + f'{text_pass[0]} - {text_pass[1]}, ціна:{text_pass[2]}\n'  # Гарно виводимо дані у текст повідомлення
    message_text = message_text + f'Загальна сума:{total_price}$'
    vovka.send_message(-4002230783,f'Нове замовлення.\n{message_text}\nНомер телефону: {message.text}')


vovka.polling(none_stop=True, interval=0)#  Графік роботи Вовки



