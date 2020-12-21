import re

import requests
import telebot

# Сайт, который предоставляет API по распознанию музыки https://dashboard.audd.io/ Сайт, с которого берется музыка(на
# нём представлены не все песни, но с него просто легче скачивать) т.е на запросы с некоторыми современными или
# популярными песнями, бот будет отправлять другую песню(первую из запроса на этом сайте) https://rus.megapesni.com/


token = "1405707075:AAFxjfjO1ggUnSsVRnhcQ41JQPkawiVwJ88"

# токен с сайта https://dashboard.audd.io/ для распознания музыки
data = {
    'api_token': 'ceb25777b3aa56cf03c97a5d99ee78c3'
}

bot = telebot.TeleBot(token)

# Параметры позволяющие (частично) имитировать работу браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Добро пожаловать!\nНаш бот умеет определять песни, для зтого отправьте нам голосовое или аудио "
                 "сообщение..")


@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message, "Згарбов Артём Вадимович, группа БСБО-06-18")

#главный метод обрабатывающий приходящие голосовые и аудио сообщения
@bot.message_handler(content_types=['audio', 'voice'])
def handle_file(message):
    try:
        # ID чата
        chat_id = message.chat.id
        # Тип  сообщения
        content = message.content_type
        if content == "audio":
            # Имя входящего файла
            filename = message.json['audio']['file_name']
            # Объект предоставляющий информацию о файле по его id(file_id)
            file_info = bot.get_file(message.audio.file_id)
        else:
            # Имя входящего файла
            filename = str(message.chat.id) + ".ogg"
            # Объект предоставляющий информацию о файле по его id(file_id)
            file_info = bot.get_file(message.voice.file_id)

        downloaded_file = bot.download_file(file_info.file_path)
        # Имя и расположение нового файла
        src = filename
        # Создаем новый файл
        with open(src, 'wb') as new_file:
            # Вводим в файл входящие данные
            new_file.write(downloaded_file)
        # Просим немного подождать..
        bot.reply_to(message, "Секундочку...")

        # Отрываем наш вновь соэданный айдио-файл
        files = {
            'file': open(filename, 'rb'),

        }
        # Делаем эапрос и получаем данные о песни
        result = requests.post('https://api.audd.io/', data=data, files=files)
        print(result.json())

        # в ответ нам присылат ответ в формаете json, теперь мы по нему выводим ответ
        bot.send_message(message.chat.id, 'Исполнитель : ' + result.json()["result"]["artist"])
        bot.send_message(message.chat.id, 'Альбом : ' + result.json()["result"]["album"])
        bot.send_message(message.chat.id, 'Название песни : ' + result.json()["result"]["title"])
        bot.send_message(message.chat.id, 'Дата выхода : ' + result.json()["result"]["release_date"])

        # Формируем запрос оставленный из названия песни
        title = result.json()["result"]["title"].split("(")[0]
        artist = result.json()["result"]["artist"].split("(")[0]
        zaproc = (title + "%20" + artist).replace(" ", "%20")

        # Приписываем нашу строку к адрессу
        http = "https://rus.megapesni.com/?do=search&subaction=search&story=" + zaproc
        # Делаем запрос
        response = requests.get(http, headers=headers)

        # Нам прийдет html-код всей страницы, с помощью регялрных выражений находим нужную нам информацию,
        # в дааном случае эта ссылка скачивае
        ret1 = re.findall(r'https://dnl.megapesni.com/get/online/[^"]+.mp3', response.text)

        # если не нашёл нужную песню
        if ret1:
            # то берём первую из поиска
            audio = ret1[0]

            # скачиваем песню
            response = requests.get(audio, headers=headers)

            # Сохраняем персню в файл
            f = open(str(message.chat.id) + '.mp3', "wb")  # открываем файл для записи, в режиме wb
            f.write(response.content)  # записываем содержимое в файл;
            f.close()

            # Отправка песни польэователю
            audio = open(str(message.chat.id) + '.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            audio.close()

    except Exception as e:
        bot.reply_to(message, 'Ошибка!')


bot.polling()
