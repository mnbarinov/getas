#!/usr/bin/env python3

import ipaddress
import sys
import socket
import argparse
import locale
import io
import shutil
import json

# Словарь переводов
TRANSLATIONS = {
    "en": {
        "arg_description": "Retrieve AS information and routes.",
        "arg_input": "IP, network, hostname or AS number(s).",
        "arg_retrieve": "Retrieve and merge routes (for IP/Domain input).",
        "arg_who": "Show only owner information (skip routes).",
        "arg_mask": "Show mask in dotted decimal format (IPv4).",
        "arg_table": "Output routes in a table format.",
        "arg_nopager": "Disable pager.",
        "arg_nomerge": "Disable network merging.",
        "arg_ipv4": "Show only IPv4.",
        "arg_ipv6": "Show only IPv6.",
        "arg_lang": "Force language (ru, en).",
        "arg_json": "Output in JSON format.",
        "error_domain": "Error: Could not resolve hostname:",
        "error_invalid_ip": "Error: Invalid IP format:",
        "no_info": "No information found for:",
        "no_routes": "No routes found for AS",
        "networks": "\033[1mNetworks (aggregated):\033[0m",
        "networks_raw": "\033[1mNetworks (raw):\033[0m",
        "table_net": "Network", "table_mask": "Mask/Prefix", "table_ver": "Ver", "table_type": "Typ",
        "total": "Total networks found:",
        "pager_prompt": "\033[7m-- Press Enter for more or 'q' to quit --\033[0m ",
        "interrupted": "Interrupted by user."
    },
    "ru": {
        "arg_description": "Получение информации об AS и маршрутах.",
        "arg_input": "IP, сеть, домен или номер(а) AS.",
        "arg_retrieve": "Получить и объединить маршруты (нужно для ввода IP/Домена).",
        "arg_who": "Показать только владельца (без списка сетей).",
        "arg_mask": "Показывать маску в десятичном формате (IPv4).",
        "arg_table": "Выводить маршруты в виде таблицы.",
        "arg_nopager": "Отключить пейджер.",
        "arg_nomerge": "Отключить объединение сетей.",
        "arg_ipv4": "Только IPv4.",
        "arg_ipv6": "Только IPv6.",
        "arg_lang": "Принудительный язык (ru, en).",
        "arg_json": "Вывод в формате JSON.",
        "error_domain": "Ошибка: Не удалось разрешить домен:",
        "error_invalid_ip": "Ошибка: Неверный формат IP:",
        "no_info": "Информация не найдена для:",
        "no_routes": "Нет маршрутов для AS",
        "networks": "\033[1mСети (агрегированные):\033[0m",
        "networks_raw": "\033[1mСети (исходные):\033[0m",
        "table_net": "Сеть", "table_mask": "Маска/Префикс", "table_ver": "Вер", "table_type": "Тип",
        "total": "Всего сетей найдено:",
        "pager_prompt": "\033[7m-- Нажмите Enter для продолжения или 'q' для выхода --\033[0m ",
        "interrupted": "Прервано пользователем."
    }
}

def translate(key, lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def query_whois(server, query):
    try:
        with socket.create_connection((server, 43), timeout=7) as s:
            s.sendall(f"{query}\r\n".encode("utf-8"))
            response = b""
            while True:
                data = s.recv(4096)
                if not data: break
                response += data
            return response.decode("utf-8", errors="replace")
    except: return None

def fetch_as_name_only(as_number):
    raw = query_whois('whois.cymru.com', f'-v AS{as_number}')
    if not raw: return "Unknown"
    for line in raw.splitlines():
        if "|" in line and not line.strip().lower().startswith("as"):
            parts = [p.strip() for p in line.split('|')]
            as_n = parts[0].upper().replace("AS", "")
            if as_n == str(as_number):
                return parts[-1]
    return "Unknown"

def fetch_as_info(ip_or_network):
    raw_data = query_whois('whois.cymru.com', f'-v {ip_or_network}')
    if not raw_data: return None
    as_info = []
    for line in raw_data.splitlines():
        if "|" in line and not line.strip().lower().startswith("as"):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                as_info.append({"as": parts[0], "ip": parts[1], "prefix": parts[2], "cc": parts[3], "name": parts[6]})
    return as_info

def fetch_routes(as_number, ipv4_only=False, ipv6_only=False):
    raw_data = query_whois('whois.radb.net', f'-i origin AS{as_number}')
    if not raw_data: return []
    routes = []
    for line in raw_data.splitlines():
        l = line.lower().strip()
        if l.startswith("route:") or l.startswith("route6:"):
            try:
                net_str = line.split(":", 1)[1].strip().split("#")[0].strip()
                net_obj = ipaddress.ip_network(net_str)
                if ipv4_only and net_obj.version == 6: continue
                if ipv6_only and net_obj.version == 4: continue
                routes.append(net_obj)
            except: continue
    return sorted(list(set(routes)), key=lambda n: (n.version, n.network_address))

def filter_nested_networks(networks):
    if not networks: return []
    networks = sorted(networks, key=lambda n: n.prefixlen)
    filtered = []
    for net in networks:
        if not any(net.subnet_of(other) for other in filtered if net != other):
            filtered.append(net)
    return filtered

def custom_pager(text, lang):
    lines = text.splitlines()
    term_height = shutil.get_terminal_size((80, 24)).lines
    chunk_size = term_height - 1

    for i in range(0, len(lines), chunk_size):
        print('\n'.join(lines[i:i+chunk_size]))
        if i + chunk_size < len(lines):
            try:
                reply = input(translate("pager_prompt", lang))
                sys.stdout.write("\033[1A\033[2K\r")
                if reply.strip().lower() == 'q':
                    break
            except (KeyboardInterrupt, EOFError):
                sys.stdout.write("\033[1A\033[2K\r")
                print(f"\n{translate('interrupted', lang)}")
                break

def main():
    # 1. Language Init
    try:
        locale.setlocale(locale.LC_ALL, '')
        sys_lang = (locale.getlocale()[0] or "en")[:2].lower()
    except: sys_lang = "en"
    lang = "ru" if sys_lang in ["ru", "be", "uk"] else "en"

    # 2. Pre-parse for --lang
    temp_parser = argparse.ArgumentParser(add_help=False)
    temp_parser.add_argument("--lang", choices=["ru", "en"])
    temp_args, _ = temp_parser.parse_known_args()
    if temp_args.lang:
        lang = temp_args.lang

    # 3. Main Parser
    parser = argparse.ArgumentParser(
        description=translate("arg_description", lang), 
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-v", "--version", action="version", version="getas 1.1.1")
    parser.add_argument("input_values", nargs="*", help=translate("arg_input", lang))
    parser.add_argument("-w", "--who", action="store_true", help=translate("arg_who", lang))
    parser.add_argument("-r", action="store_true", help=translate("arg_retrieve", lang))
    parser.add_argument("-m", action="store_true", help=translate("arg_mask", lang))
    parser.add_argument("-t", action="store_true", help=translate("arg_table", lang))
    parser.add_argument("-4", dest="ipv4", action="store_true", help=translate("arg_ipv4", lang))
    parser.add_argument("-6", dest="ipv6", action="store_true", help=translate("arg_ipv6", lang))
    parser.add_argument("--no-merge", action="store_true", help=translate("arg_nomerge", lang))
    parser.add_argument("--no-pager", action="store_true", help=translate("arg_nopager", lang))
    parser.add_argument("--lang", choices=["ru", "en"], help=translate("arg_lang", lang))
    parser.add_argument("--json", action="store_true", help=translate("arg_json", lang))

    args = parser.parse_args()
    if not args.input_values:
        parser.print_help(); sys.exit(0)

    json_output = []
    text_buffer = io.StringIO()

    try:
        for val in args.input_values:
            val = val.strip()
            is_as_direct = val.isdigit() or val.upper().startswith("AS")
            current_targets = [] # List of {asn, name, detail_info}

            if is_as_direct:
                as_n = val.upper().replace("AS", "")
                current_targets.append({"asn": as_n, "name": fetch_as_name_only(as_n), "info": None})
                fetch_now = not args.who
            else:
                target_ip = None
                try:
                    target_ip = str(ipaddress.ip_network(val, strict=False).network_address) if "/" in val else str(ipaddress.ip_address(val))
                except ValueError:
                    try: target_ip = socket.gethostbyname(val)
                    except: 
                        if not args.json: print(f"{translate('error_domain', lang)} {val}")
                        continue

                info = fetch_as_info(target_ip)
                if not info:
                    if not args.json: print(f"{translate('no_info', lang)} {val}")
                    continue
                for i in info:
                    current_targets.append({"asn": i['as'].replace("AS", ""), "name": i['name'], "info": i})
                fetch_now = args.r and not args.who

            # Process targets
            for target in current_targets:
                asn = target["asn"]
                as_entry = {
                    "input": val,
                    "asn": f"AS{asn}",
                    "name": target["name"],
                    "info": target["info"],
                    "routes": []
                }

                if not args.json:
                    text_buffer.write("-" * 45 + "\n")
                    if target["info"]:
                        i = target["info"]
                        text_buffer.write(f"{'AS:':<15} {i['as']}\n{'IP:':<15} {i['ip']}\n{'Prefix:':<15} {i['prefix']}\n{'Name:':<15} {i['name']}\n")
                    else:
                        text_buffer.write(f"{'AS:':<15} AS{asn}\n{'Name:':<15} {target['name']}\n")

                if fetch_now:
                    raw_rt = fetch_routes(asn, args.ipv4, args.ipv6)
                    raw_strings = {str(n) for n in raw_rt} # For M/S bug fix

                    if raw_rt:
                        if args.no_merge:
                            f_rt = raw_rt
                        else:
                            v4 = filter_nested_networks([n for n in raw_rt if n.version == 4])
                            v6 = filter_nested_networks([n for n in raw_rt if n.version == 6])
                            f_rt = list(ipaddress.collapse_addresses(v4)) + list(ipaddress.collapse_addresses(v6))
                            f_rt.sort(key=lambda n: (n.version, n.network_address))

                        # Build Routes Output
                        if args.json:
                            for n in f_rt:
                                as_entry["routes"].append({
                                    "network": str(n.network_address),
                                    "mask": str(n.netmask),
                                    "prefix_len": n.prefixlen,
                                    "version": n.version,
                                    "type": "M" if str(n) not in raw_strings else "S"
                                })
                        else:
                            header_key = "networks_raw" if args.no_merge else "networks"
                            text_buffer.write(f"\n{translate(header_key, lang)}\n")
                            if args.t:
                                cols = [translate(k, lang) for k in ["table_net", "table_mask", "table_ver", "table_type"]]
                                h_line = f"| {cols[0]:<35} | {cols[1]:<18} | {cols[2]:<3} | {cols[3]:<4} |"
                                sep = "-" * len(h_line)
                                text_buffer.write(f"{sep}\n{h_line}\n{sep}\n")
                                for n in f_rt:
                                    m_val = str(n.netmask) if args.m and n.version == 4 else f"/{n.prefixlen}"
                                    rtype = "M" if str(n) not in raw_strings else "S"
                                    text_buffer.write(f"| {str(n.network_address):<35} | {m_val:<18} | v{n.version:<2} | {rtype:<4} |\n")
                                text_buffer.write(f"{sep}\n{translate('total', lang)} {len(f_rt)}\n")
                            else:
                                for n in f_rt:
                                    text_buffer.write(f"{n.network_address}/{n.netmask}\n" if args.m and n.version == 4 else f"{n}\n")
                    else:
                        if not args.json: text_buffer.write(f"\n{translate('no_routes', lang)} AS{asn}\n")
                
                json_output.append(as_entry)

        # Final Output Logic
        if args.json:
            print(json.dumps(json_output, indent=4, ensure_ascii=False))
        else:
            final_text = text_buffer.getvalue()
            if not final_text.strip(): return
            
            term_height = shutil.get_terminal_size((80, 24)).lines
            if args.no_pager or not sys.stdout.isatty() or final_text.count('\n') < term_height:
                print(final_text, end="")
            else:
                custom_pager(final_text, lang)

    except KeyboardInterrupt:
        if not args.json: print(f"\n{translate('interrupted', lang)}")

if __name__ == "__main__":
    main()