# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re

def get_ip_from_cfg(config):
    with open(config) as f:
        regex = re.compile(
            r"interface (?P<intf>\S+)\n"
            r"( .*\n)*"
            r" ip address (?P<ip>\S+) (?P<mask>\S+)"
        )
        match = regex.finditer(f.read())

    result = {m.group("intf"): m.group("ip", "mask") for m in match}
    return result


# ========================================================================

### Мое решение (вариант 1 через re.search) ###

import re
from pprint import pprint

def get_ip_from_cfg(filename):
    regex_1 = r"^interface (\S+)"
    regex_2 = r"ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)"
    dict_ip = {}
    with open(filename) as f:
        for line in f:
            match_intf = re.search(regex_1, line)
            match_ip = re.search(regex_2, line)
            if match_intf:
                interface = match_intf.group(1)
            elif match_ip:
                dict_ip[interface] = match_ip.groups()
    return dict_ip

dict_ip = get_ip_from_cfg("config_r1.txt")
pprint(dict_ip)

# ========================================================================

### Мое решение (вариант 2 через re.finditer) ### (ркгулярку подсмотрел, не получалось)

import re
from pprint import pprint

def get_ip_from_cfg(filename):
    regex = (
        r"interface (\S+)\n"
        r"(?: .*\n)*"
        r" ip address (\S+) (\S+)"
    )
    dict_ip = {}
    with open(filename) as f:
        config = f.read()
        match = re.finditer(regex, config)
        for m in match:
            interface = m.group(1)
            dict_ip[interface] = m.group(2, 3) 
        # dict_ip = {m.group(1): m.group(2, 3) for m in match}      # с помощью генератора словаря
    return dict_ip

dict_ip = get_ip_from_cfg("config_r1.txt")
pprint(dict_ip)
  














   