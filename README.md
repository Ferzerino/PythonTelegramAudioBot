# PythonTelegramAudioBot

<h1>Необходимые библиотеки:</h1>

  1. requests(Библиотека позволяющаяя делать запросы в интернет)

    pip install requeusts

  2. PyTelegramBotAPI(предоставляет возможность управлять нашим ботом)

    pip install PyTelegramBotAPI


Для работы бота нужно:

  1) Токен бота в телеграме
  2) Токен с сайта https://dashboard.audd.io (он принимает сообщение и выдает json файл со всей информацией по найденной композиции(300 запросов в пробной версии))
  3) Доступ в интернет с устройства, на котором будет запускаться бот(либо можно загрузить бота на севрер)

<h1>Реализация</h1>
    Целью было создать бота, который принимает голосовое сообщение и выдаёт всю нужную информацию:
    
      1. Название композиции
      
      2. Имя исполнителя
      
  Данную возможность предоставляет AudD API Dashboard. Нужно зарегистрироваться на сайте, используя свой телеграм аккаунт, отправить свой контакт для подтверждения
  и получить пробный период на 300 запросов и токен, который позже будет использован в коде, для доступа к своему аккаунту.
  
  После того как данное API, нашло композицию, боту отправляется json файл, в котором содержатся переменные:
      
      artist(исполнитель композиции(если несколько то через ;)
      title(название композиции)
      album(альбом)
      release_date(Официальная дата выхода композиции)
      label(Лейбл на котором состоит исполнитель)
      timecode(Таймкод композиции, с которого пользователь начал запись)
      
  Из них нам нужны первые 4(остальная информация лишняя)
  
  После того, как бот отправил их пользователю, формируется http запрос на сайт rus.megapesni.com.
  Запрос формируется вот так: http = "https://rus.megapesni.com/?do=search&subaction=search&story="+zaproc
  переменная zaproc состоит из переменных title+artist
  
  Если после запроса, нужная композиция не была найдена(т.к база на этом сайте не очень большая) берётся первая из найденных.
  Далее она скачивается, записывается в файл и отправляется пользователю.
 

<h1>Скриншоты</h1>
      
