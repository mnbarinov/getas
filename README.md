# Getas Tool

A lightweight, fast, and dependency-free CLI utility to retrieve Autonomous System (AS) information and BGP routes directly from WHOIS servers (Cymru and RADB).

## Features
- **Fast AS Lookup**: Get owner information by IP, Domain, or ASN.
- **Route Aggregation**: Automatically merges adjacent networks for a cleaner view (can be disabled).
- **Smart Paging**: Built-in terminal-aware pager that doesn't feel like a separate app.
- **Zero Dependencies**: Uses only Python standard libraries.
- **Table Mode**: Clean tabular output for better readability.

---

# getas-tool

Легкая и быстрая консольная утилита без внешних зависимостей для получения информации об Автономных Системах (AS) и маршрутах BGP напрямую из WHOIS-серверов (Cymru и RADB).

## Особенности
- **Быстрый поиск**: Получение информации о владельце по IP, домену или номеру AS.
- **Агрегация маршрутов**: Автоматическое объединение смежных сетей для удобства (можно отключить).
- **Умный пейджер**: Встроенная постраничная навигация, учитывающая высоту терминала.
- **Без зависимостей**: Использует только стандартную библиотеку Python.
- **Табличный режим**: Форматированный вывод данных для удобного чтения.

## Usage / Использование

### 🔍 Basic Information / Основная информация
Get information about an IP address, domain, or AS number.
*Получение информации об IP-адресе, домене или номере AS.*

```bash
# Get AS info for an IP / Инфо об AS для конкретного IP
getas 8.8.8.8 -w

# Get info for a domain / Инфо по домену
getas google.com -w

# Get info by AS number / Инфо по номеру автономной системы
getas AS15169 -w
```

### 🛣 Working with Routes / Работа с маршрутами
Retrieve and display BGP routes.
Загрузка и отображение BGP маршрутов.
```bash
# Get all routes for an AS (Table mode)
# Все маршруты AS в виде таблицы
getas AS13335 -t

# Get routes for an IP's owner (Manual trigger)
# Загрузить маршруты владельца IP (флаг -r обязателен для IP/доменов)
getas 1.1.1.1 -r -t

# Filter by IP version (IPv4 or IPv6 only)
# Фильтрация по версии протокола (только IPv4 или IPv6)
getas AS15169 -t -4
getas AS15169 -t -6
```

### ⚙️ Advanced Options / Продвинутые опции

Fine-tune the output formatting.
Тонкая настройка вывода.
```bash
# Disable route merging (show raw prefixes)
# Отключить объединение сетей (показать исходные префиксы)
getas AS13335 -t --no-merge

# Show IPv4 mask in decimal format (255.255.255.0 instead of /24)
# Показать маску в десятичном формате
getas AS13335 -t -m

# Force interface language (English or Russian)
# Принудительная смена языка (en или ru)
getas 8.8.8.8 --lang en
getas 8.8.8.8 --lang ru

# Disable built-in pager (useful for scripts)
# Отключить встроенный пейджер (полезно для перенаправления вывода)
getas AS13335 --no-pager > routes.txt
```

#### Examples / Примеры
| Task / Задача | Command / Команда |
| :--- | :--- |
| Simple lookup | getas 1.1.1.1 -w |
| Full table (EN) | getas AS13335 -t --lang en |
| All IPv6 routes | getas AS15169 -t -6 |
| Raw data export | getas AS13335 --no-merge --no-pager |


## Options / Параметры

| Flag | Description | Описание |
| :--- | :--- | :--- |
| `-h` | Help | Справка |
| `-w` | Whois only (no routes) | Только информация о владельце |
| `-t` | Table output | Вывод в виде таблицы |
| `-m` | Show netmask (decimal) | Показать маску в десятичном виде |
| `-4` | Show only IPv4 routes | Показывать только маршруты IPv4 |
| `-6` | Show only IPv6 routes | Показывать только маршруты IPv6 |
| `--no-merge` | Disable route merging | Отключить объединение сетей |
| `--no-pager` | Disable pagination | Отключить разбивку на страницы |
| `--lang {ru, en}` | Language for output | Язык для вывода |


## Installation / Установка

### 📦 Download Ready-to-Use Packages (Recommended)
You can download the latest pre-built packages for your distribution from the [Releases](https://github.com/mnbarinov/getas/releases) page.

#### For Debian, Ubuntu, Astra Linux, Mint (.deb):
```bash
sudo dpkg -i getas_1.0.0_all.deb
# If there are missing dependencies:
sudo apt-get install -f

#### For ALT Linux, Fedora, CentOS, RedOS (.rpm):
```bash
# ALT Linux:
sudo apt-get install ./getas-1.0.0-1.noarch.rpm
# Fedora / CentOS:
sudo dnf install ./getas-1.0.0-1.noarch.rpm
```

#### Via Python Pip (Universal)
If you have Python installed, you can install the tool directly from the source:
```bash
git clone [https://github.com/mnbarinov/getas.git](https://github.com/mnbarinov/getas.git)
cd getas
pip install .
```
*Note: This will create a getas command in your PATH.*

#### Arch Linux (AUR)
If you are using Arch Linux, you can build the package using the provided PKGBUILD:
```bash
git clone [https://github.com/mnbarinov/getas.git](https://github.com/mnbarinov/getas.git)
cd getas
makepkg -si
```

#### Manual Installation (Single file)
If you just want the script without any package management:
```bash
sudo curl -L [https://raw.githubusercontent.com/mnbarinov/getas/master/getas/main.py](https://raw.githubusercontent.com/mnbarinov/getas/master/getas/main.py) -o /usr/bin/getas
sudo chmod +x /usr/bin/getas
```

