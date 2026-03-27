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

```bash
# Basic AS info / Информация об AS
getas 1.1.1.1 -w

# Get all routes (Table mode) / Все маршруты в виде таблицы
getas AS13335 -t

# Search by domain with no route merging / Поиск по домену без объединения сетей
getas google.com --no-merge
```

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
