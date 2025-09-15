# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re


def get_ip_from_cfg(filename):
    result = {}
    regex = (r"^interface (?P<intf>\S+)"
             r"|address (?P<ip>\S+) (?P<mask>\S+)")                 # применяется "или"

    with open(filename) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
                if match.lastgroup == "intf":
                    intf = match.group(match.lastgroup)
                elif match.lastgroup == "mask":
                    result.setdefault(intf, [])                     # setdefault добавляет ключ (в нашем случае интерфейс) в словарь со значением (в нашем случае пустой список), если ключ отсутсвует, 
                                                                    # если такой ключ уже есть, то ничего не делает (значение не перезапишет)
                    result[intf].append(match.group("ip", "mask"))  # добавление в словарь
    return result


# еще один вариант решения

def get_ip_from_cfg(filename):
    result = {}
    with open(filename) as f:
        # сначала отбираем нужные куски конфигурации
        match = re.finditer(
            "interface (\S+)\n"
            "(?: .*\n)*"
            " ip address \S+ \S+\n"
            "( ip address \S+ \S+ secondary\n)*",
            f.read(),
        )
        # потом в этих частях находим все IP-адреса
        for m in match:
            result[m.group(1)] = re.findall("ip address (\S+) (\S+)", m.group())
    return result

# =====================================================================

### Мое решение ###  (решение взял у автора, 2-ой вариант, просто разобрал его)

import re
from pprint import pprint

def get_ip_from_cfg(filename):
    regex = (
        r"interface (\S+)\n"                    # такая же регулярка как и в прошлом задании
        r"(?: .*\n)*"
        r" ip address (\S+) (\S+)"
        r"( ip address \S+ \S+ secondary)*"     # добавили что может быть еще адрес
    )                                           
    dict_ip = {}
    with open(filename) as f:
        config = f.read()
        match = re.finditer(regex, config)                              # находим все совпадения 
        for m in match:                                                 # перебираем куски с совпадениями
            interface = m.group(1)                                      # берем интерфейс
            ip_list = re.findall("ip address (\S+) (\S+)", m.group())   # теперь в каждом совпадении отбираем адреса с помощью findall, она же делает список
            dict_ip[interface] = ip_list                                # записываем в словарь
    return dict_ip

dict_ip = get_ip_from_cfg("config_r2.txt")
pprint(dict_ip)