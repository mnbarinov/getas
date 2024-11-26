#!/usr/bin/env python3

import subprocess
import ipaddress
import sys
import socket
import argparse
import locale

# Словарь переводов
TRANSLATIONS = {
    "en": {
        "arg_description": "Retrieve AS information and routes.",
        "arg_input": "IP, network, hostname or AS number for analysis.",
        "arg_tolerance": "Bits for merging networks.",
        "arg_retrieve": "Retrieve and merge routes for the found AS.",
        "arg_mask": "Convert the subnet mask to binary format.",
        "arg_lang": "Language for output.",
        "arg_help": "Extended help.",
        "arg_nomerge": "Do not merge networks.",
        "arg_lang_choices": ["English", "Russian"],
        "error_whois": "Error executing whois",
        "whois_not_found": "Whois command not found. Ensure it is installed.",
        "domain_ip_error": "Error: Could not resolve IP for domain",
        "no_routes": "No routes found for AS",
        "invalid_network_format": "Invalid network format",
        "as_info": "\033[1mAS Information:\033[0m",
        "as": "AS:",
        "ip": "IP:",
        "bgp_prefix": "BGP Prefix:",
        "country": "Country:",
        "registry": "Registry:",
        "allocated": "Allocated:",
        "as_name": "AS Name:",
        "merged_networks": "\033[1mMerged Networks:\033[0m",
        "networks": "\033[1mNetworks:\033[0m",
        "nested_networks": "Filtered Networks (without nested):",
        "no_info": "1mNo information found for",
        "please_wait":"\033[3m(Please wait...)\033[0m",
        "usage": """
\033[1mUsage Guide:\033[0m
This script analyzes AS and routes with network aggregation.

\033[1mExamples:\033[0m
  getas 15169
  getas 15169 --tolerance 8
  getas 15169 --no-merge
  getas 15169 --tolerance 8 -m --no-merge
  
  getas 8.8.8.8
  getas 8.8.8.8 -r
  getas 8.8.8.8 -m 
  getas mbarinov.ru -r -m --no-merge

  getas --help
  getas --help --lang ru

getas by Mikhail Barinov, version 1.0.2 (24.11.2024)
    https://mbarinov.ru
    https://github.com/mnbarinov/getas
""",
        "interrupted": "Interrupted by user."
    },
    "ru": {
        "arg_description": "Получение информацию об AS и маршрутах.",
        "arg_input": "IP, сеть, доменное имя или номер AS для анализа.",
        "arg_tolerance": "Биты для объединения сетей.",
        "arg_retrieve": "Получить и объединить маршруты для найденного AS.",
        "arg_lang": "Язык вывода.",
        "arg_help": "Расширенная справка.",
        "arg_nomerge": "Не объединять сети.",
        "arg_mask": "Преобразовать маску подсети в двоичный формат.",
        "arg_lang_choices": ["Английский", "Русский"],
        "error_whois": "Ошибка выполнения whois",
        "whois_not_found": "Команда whois не найдена. Убедитесь, что она установлена.",
        "domain_ip_error": "Ошибка: Не удалось найти IP для домена",
        "no_routes": "Нет маршрутов для AS",
        "invalid_network_format": "Неверный формат сети",
        "as_info": "\033[1mИнформация об AS:\033[0m",
        "as": "AS:",
        "ip": "IP:",
        "bgp_prefix": "BGP Prefix:",
        "country": "Страна:",
        "registry": "Реестр:",
        "allocated": "Выделено:",
        "as_name": "Название AS:",
        "merged_networks": "\033[1mОбъединённые сети:\033[0m",
        "networks": "\033[1mСети:\033[0m",
        "nested_networks": "Сети без вложенных:",
        "no_info": "Нет информации о",
        "please_wait":"\033[3m(Пожалуйста подождите...)\033[0m",
        "usage": """
\033[1mИнструкция:\033[0m
Скрипт анализирует автономные системы (AS) и маршруты с укрупнением сетей.

\033[1mПримеры:\033[0m
  getas 15169
  getas 15169 --tolerance 8
  getas 15169 --no-merge
  getas 15169 --tolerance 8 -m --no-merge
  
  getas 8.8.8.8
  getas 8.8.8.8 -r
  getas 8.8.8.8 -m 
  getas mbarinov.ru -r -m --no-merge

  getas --help
  getas --help --lang en

getas by Mikhail Barinov, version 1.0.2 (24.11.2024)
    https://mbarinov.ru
    https://github.com/mnbarinov/getas
""",
        "interrupted": "Прервано пользователем."
    }
}


def translate(key, lang):
    """Перевод текста на выбранный язык."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def fetch_as_info(ip_or_network):
    """Получает информацию об AS для заданного IP или сети."""
    try:
        result = subprocess.run(
            ['whois', '-h', 'whois.cymru.com', ' -v', ip_or_network],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0 or not result.stdout:
            print(f"{translate('error_whois', args.lang)}: {result.stderr}")
            return None

        as_info = []
        for line in result.stdout.splitlines():
            if line.startswith("AS") and "BGP Prefix" in line:
                continue  # Пропускаем заголовки
            parts = line.split('|')
            if len(parts) >= 7:  # Только строки с достаточным количеством частей
                as_number = parts[0].strip()
                bgp_prefix = parts[2].strip()
                as_name = parts[6].strip()
                cc = parts[3].strip()
                registry = parts[4].strip()
                allocated = parts[5].strip()
                ip = parts[1].strip()
                as_info.append((as_number, bgp_prefix, as_name, cc, registry, allocated, ip))
        return as_info
    except FileNotFoundError:
        print(translate("whois_not_found", args.lang))
        return None


def get_ip_from_hostname(hostname):
    """Проверяет, является ли входное значение доменом и возвращает первый IP-адрес."""
    try:
        ip_addresses = socket.gethostbyname_ex(hostname)
        return ip_addresses[2][0]  # Возвращаем первый IP-адрес
    except socket.gaierror:
        print(f"{translate('domain_ip_error', args.lang)} {hostname}")
        return None


def fetch_routes(as_number):
    """Получение списка сетей через whois."""
    try:
        result = subprocess.run(
            ['whois', '-h', 'whois.radb.net', f' -i origin AS{as_number}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0 or not result.stdout:
            print(f"{translate('error_whois', args.lang)}: {result.stderr}")
            return []

        routes = []
        for line in result.stdout.splitlines():
            if line.lower().startswith("route:"):
                network = line.split(":")[1].strip()
                try:
                    routes.append(ipaddress.ip_network(network))
                except ValueError:
                    print(f"{translate('invalid_network_format', args.lang)}: {network}")
        return routes
    except FileNotFoundError:
        print(translate("whois_not_found", args.lang))
        return []


def print_as_info(as_info, lang="en"):
    """Форматирует и выводит информацию об AS в формате параметр — значение."""
    print("-" * 40)
    print(translate("as_info", lang))
    for as_number, bgp_prefix, as_name, cc, registry, allocated, ip in as_info:
        print(f"{translate('as', lang):<15} {as_number}")
        print(f"{translate('ip', lang):<15} {ip}")
        print(f"{translate('bgp_prefix', lang):<15} {bgp_prefix}")
        print(f"{translate('country', lang):<15} {cc}")
        print(f"{translate('registry', lang):<15} {registry}")
        print(f"{translate('allocated', lang):<15} {allocated}")
        print(f"{translate('as_name', lang):<15} {as_name}")
        print("-" * 40)



def merge_networks(networks, tolerance):
    """Итеративное объединение сетей с учетом допуска."""
    networks = sorted(networks)  # Сортируем сети
    merged = networks[:]

    while True:
        new_merged = []
        skip = set()

        for i, net1 in enumerate(merged):
            if i in skip:
                continue

            combined = False
            for j, net2 in enumerate(merged[i + 1:], start=i + 1):
                if j in skip:
                    continue

                supernet = net1.supernet(new_prefix=net1.prefixlen - 1)
                if net2.subnet_of(supernet):
                    address_diff = abs(net2.num_addresses - net1.num_addresses)
                    if address_diff <= tolerance:
                        new_merged.append(supernet)
                        skip.update({i, j})
                        combined = True
                        break

            if not combined:
                new_merged.append(net1)

        if len(new_merged) == len(merged):
            break

        merged = sorted(new_merged)

    return merged


def filter_nested_networks(networks):
    """Удаляет сети, вложенные в более крупные."""
    filtered = []
    for net in networks:
        if not any(net != other and net.subnet_of(other) for other in networks):
            filtered.append(net)
    return filtered


def print_usage(lang="en"):
    """Вывод справки в зависимости от выбранного языка."""
    print(translate("usage", lang))

def arg_parse(lang="en"):
    """парсинг аргументов"""
    parser = argparse.ArgumentParser(description=translate("arg_description", lang))
    parser.add_argument("input_value", type=str, help=translate("arg_input", lang))
    parser.add_argument("--tolerance", type=int, default=0, help=translate("arg_tolerance", lang))
    parser.add_argument("-r", action="store_true", help=translate("arg_retrieve", lang))
    parser.add_argument("-m", action="store_true", help=translate("arg_mask", lang))
    parser.add_argument("--lang", choices=["ru", "en"], default="en",  help=translate("arg_lang", lang))
    parser.add_argument("help", action="store_true", help=translate("arg_help", lang))
    parser.add_argument("--no-merge", action="store_true", help=translate("arg_nomerge", lang))
    return parser





def get_system_language():
    """Получить текущую локаль системы."""
    locale.setlocale(locale.LC_ALL, '')  # Устанавливаем локаль по умолчанию
    return locale.getlocale()[0]  # Получаем код языка

def get_language_code():
    """Вернуть 'ru' для русскоязычных, белорусскоязычных и украиноязычных систем, иначе 'en'."""
    system_language = get_system_language()
    
    if system_language in ['ru', 'be', 'uk']:
        return 'ru'
    else:
        return 'en'

def get_initial_lang():
    """Получает значение языка из аргументов командной строки."""
    initial_lang = get_language_code()  # Значение по умолчанию
    for i, arg in enumerate(sys.argv):
        if arg == "--lang" and i + 1 < len(sys.argv):
            # Если следующий аргумент существует, считаем его значением для --lang
            return sys.argv[i + 1]
        elif arg.startswith("--lang="):
            # Если аргумент передан в виде --lang=ru
            return arg.split("=")[1]
    return initial_lang

def cidr_to_netmask(cidr: str) -> str:
    # Используем ipaddress для создания сети
    network = ipaddress.IPv4Network(f'0.0.0.0/{cidr}', strict=False)
    # Возвращаем строковое представление маски подсети
    return str(network.netmask)

def main():
    try:
        # parser = argparse.ArgumentParser(description="Retrieve AS information and routes.")
        # parser.add_argument("input_value", type=str, help="IP, network, hostname or AS number for analysis.")
        # parser.add_argument("--tolerance", type=int, default=0, help="Bits for merging networks.")
        # parser.add_argument("-r", action="store_true", help="Retrieve and merge routes for the found AS.")
        # parser.add_argument("--lang", choices=["ru", "en"], default="en", help="Language for output.")

        #
        initial_lang = get_initial_lang()

        #
        
        global args

        parser = arg_parse(lang=initial_lang)
        
        args = parser.parse_args()

        if len(sys.argv) == 1:
            parser.print_help()
            print_usage(args.lang)
            sys.exit(0)

        input_value = args.input_value.strip()

        if input_value.lower() in {"help", "--help", "-h"}:
            print_usage(args.lang)
            sys.exit(0)
        

        if not input_value.isdigit():
            ip = get_ip_from_hostname(input_value)
            if ip:
                input_value = ip

        if input_value.isdigit():
            routes = fetch_routes(input_value)
            if not routes:
                print(f"{translate('no_routes', args.lang)} AS{input_value}.")
                return

            # merged_routes = merge_networks(routes, args.tolerance)
            # filtered_routes = filter_nested_networks(merged_routes)

            if args.no_merge == False:
                merged_routes = merge_networks(routes, args.tolerance)
                filtered_routes = filter_nested_networks(merged_routes)
            else:
                filtered_routes = filter_nested_networks(routes)
                print(translate("networks", args.lang))


            first=filtered_routes[0]
            as_info2 = fetch_as_info(f"{first}")
            if not as_info2:
                print(f"{translate('no_info', args.lang)} {input_value}.")
                return
            print_as_info(as_info2, lang=args.lang)


            if args.no_merge == False:
                print(translate("merged_networks", args.lang))
            else:
                print(translate("networks", args.lang))


            for net in filtered_routes:
                if args.m:
                    ip = str(net.network_address)  # Получаем IP-адрес сети
                    mask = net.prefixlen  # Получаем длину префикса (маску подсети)
                    print(f"{ip}/{cidr_to_netmask(mask)}")  # Печатаем IP-адрес и маску в нужном формате
                else:    
                    print(net)
                    
        else:
            as_info = fetch_as_info(input_value)
            if not as_info:
                print(f"{translate('no_info', args.lang)} {input_value}.")
                return

            print_as_info(as_info, lang=args.lang)

            
            if args.r:
                if args.no_merge == False:
                    print(translate("merged_networks", args.lang))
                else:
                    print(translate("networks", args.lang))


                for as_number, *_ in as_info:
                    routes = fetch_routes(as_number)
                    if(len(routes) > 50):
                        print(translate(f"please_wait", args.lang))
                                        
                    
                    if args.no_merge == False:
                        merged_routes = merge_networks(routes, args.tolerance)
                        filtered_routes = filter_nested_networks(merged_routes)
                    else:
                        filtered_routes = filter_nested_networks(routes)


                    for net in filtered_routes:
                        if args.m:
                            ip = str(net.network_address)  # Получаем IP-адрес сети
                            mask = net.prefixlen  # Получаем длину префикса (маску подсети)
                            print(f"{ip}/{cidr_to_netmask(mask)}")  # Печатаем IP-адрес и маску в нужном формате
                        else:    
                            print(net)

    except KeyboardInterrupt:
        print(f"\n{translate('interrupted', args.lang)}.")
        sys.exit(0)


if __name__ == "__main__":
    main()
