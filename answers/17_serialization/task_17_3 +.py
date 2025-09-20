# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re


def parse_sh_cdp_neighbors(command_output):
    regex = re.compile(
        r"(?P<r_dev>\w+)  +(?P<l_intf>\S+ \S+)"
        r"  +\d+  +[\w ]+  +\S+ +(?P<r_intf>\S+ \S+)"
    )
    connect_dict = {}
    l_dev = re.search(r"(\S+)[>#]", command_output).group(1)
    connect_dict[l_dev] = {}
    for match in regex.finditer(command_output):
        r_dev, l_intf, r_intf = match.group("r_dev", "l_intf", "r_intf")
        connect_dict[l_dev][l_intf] = {r_dev: r_intf}
    return connect_dict


if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        print(parse_sh_cdp_neighbors(f.read()))

#===========================================================================

### Мое решение ###  (в принципе такое же)

import re
import csv
from glob import glob
from pprint import pprint

def pparse_sh_cdp_neighbors(output):
    regex = re.compile(r"(?P<hostname>\S+) +"                                       # регулярка отличается немного
                       r"(?P<l_intf>\S+ [0-9\/]+)"
                       r" +\d+ +(?:[\S+ ]+) +\S+ +"
                       r"(?P<r_intf>\S+ [0-9\/]+)")
    device = re.search(r"(\S+)>sh", output).group(1)                                # находим имя устройства с которого снят вывод
    cdp_dict = {}                                                                   # делаем пустой словарь
    match = regex.finditer(output)                                                  # регуляркой ищем нужные совпадения
    for m in match:                                                                 # перебираем наши совпадения
        hostname, local_potr, remote_port = m.group("hostname", "l_intf", "r_intf") # распаковываем совпадения
        cdp_dict[local_potr] = {hostname: remote_port}                              # делаем словари с подсловарями вида {'Eth 0/1': {'R1': 'Eth 0/0'}}
    return {device: cdp_dict}                                                       # делаем головной словарь с значением подсловарей, которые сделали раньше и возвращаем его

if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        pprint(pparse_sh_cdp_neighbors(f.read()))
  
"""  
Результат:
  
{'SW1': {'Eth 0/1': {'R1': 'Eth 0/0'},
         'Eth 0/2': {'R2': 'Eth 0/0'},
         'Eth 0/3': {'R3': 'Eth 0/0'},
         'Eth 0/5': {'R6': 'Eth 0/1'}}}
"""