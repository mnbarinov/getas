# GetAS
<img src="getas_banner.jpg" alt="getas by Mikhail Barinov - Retrieve AS information and routes" width=100% align=center >

`getas` — это удобный инструмент для анализа информации об `автономных системах` (AS), маршрутах и `объединении сетей`. Скрипт поддерживает работу как с IP-адресами и сетями, так и с доменными именами или номерами AS. Основные функции включают возможность получения детальной информации об `AS`, агрегацию сетей и форматированный вывод на `русском` и `английском` языках.

Этот инструмент разработан для сетевых инженеров, аналитиков и всех, кто интересуется анализом маршрутов в Интернете.

*Актуальные данные о сетях, связанных с различными организациями, стали особенно востребованными в условиях блокировки ряда сайтов. Например, чтобы получить полный список сетей, ассоциированных с YouTube (Google), достаточно выполнить следующую команду:*
```
getas youtube.com -r
```

## Установка
### Загрузка

#### Скачайте последнюю версию `getas` с `GitHub`:
```
git clone https://github.com/mnbarinov/getas.git
cd getas
```
### Установка зависимостей

Для работы скрипта требуются Python 3 и команды whois. Установите их, если они отсутствуют:

#### Debian/Ubuntu:
```
sudo apt update
sudo apt install python3 python3-pip whois
```

#### RHEL/CentOS:
```
sudo dnf install python3 python3-pip whois
```

### Установка скрипта

Для удобства использования создайте символическую ссылку:
```
sudo ln -s $(pwd)/getas.py /usr/local/bin/getas
```
Теперь вы можете запускать скрипт командой `getas`.

### Рекомендуемая настройка языка

По умолчанию вывод скрипта отображается на английском языке. Чтобы использовать русский язык по умолчанию, добавьте следующий алиас в свой файл `.bashrc`:
```
echo "alias getas='getas --lang ru'" >> ~/.bashrc
source ~/.bashrc
```

## Примеры использования

### Получение информации об автономной системе по номеру AS, и сетей анонсируемых AS:
```
getas 15169
```
### Задать допуск при объединении сетей:
```
getas 15169 --tolerance 8 
```
### Не объединять сети:
```
getas 15169 --no-merge
```
### Получение информации об автономной системе по IP-адресу:
```
getas 8.8.8.8
```
### Получение информации об автономной системе по IP-адресу, и сетей анонсируемых AS:
```
getas 8.8.8.8 -r
```
### Преобразовать маски подсети в двоичный формат:
```
getas 8.8.8.8 -m -r
```
### Получение информации об автономной системе на основе доменного имени:
``
getas example.com
``
### Изменить язык вывода информации
```
getas mbarinov.ru -r --lang {ru,en}
```
### Справка:
```
getas --help
getas help
```
## Снимки экрана

<img src="getas_screenshot1.png" alt="getas by Mikhail Barinov - Retrieve AS information and routes" width=100% align=center >

<img src="getas_screenshot2.png" alt="getas by Mikhail Barinov - Retrieve AS information and routes" width=100% align=center >

<img src="getas_screenshot3.png" alt="getas by Mikhail Barinov - Retrieve AS information and routes" width=100% align=center >

## Автор

Михаил Баринов

 - GitHub: https://github.com/mnbarinov

 - Сайт: https://mbarinov.ru
