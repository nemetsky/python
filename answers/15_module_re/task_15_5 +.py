# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""
import re


def generate_description_from_cdp(sh_cdp_filename):
    regex = re.compile(
        r"(?P<r_dev>\w+)  +(?P<l_intf>\S+ \S+)"
        r"  +\d+  +[\w ]+  +\S+ +(?P<r_intf>\S+ \S+)"
    )
    intf_desc_map = {}
    with open(sh_cdp_filename) as f:
        for match in regex.finditer(f.read()):
            r_dev, l_intf, r_intf = match.group("r_dev", "l_intf", "r_intf")
            intf_desc_map[l_intf] = f"description Connected to {r_dev} port {r_intf}"
    return intf_desc_map


if __name__ == "__main__":
    print(generate_description_from_cdp("sh_cdp_n_sw1.txt"))


#======================================================================================

### Мое решение ###  (такое же только регулярка отличается, и группы неименованы у меня)

import re
from pprint import pprint

def generate_description_from_cdp(filename):
    regex = re.compile(r"(\S+) +(\S+ [\/\d]+).+ (\S+ [\/\d]+)")               # группа 1 - имя утройства, группа 2 - локальный порт, группа 3 - удаленный порт
    my_dict = {}
    with open(filename) as f:
        match = regex.finditer(f.read())
        for m in match:
            descr = f"description Connected to {m.group(1)} port {m.group(3)}"
            my_dict[m.group(2)] = descr
    return my_dict

pprint(generate_description_from_cdp("sh_cdp_n_sw1.txt"))

"""
Результат

{'Eth 0/1': 'description Connected to R1 port Eth 0/0',
 'Eth 0/2': 'description Connected to R2 port Eth 0/0',
 'Eth 0/3': 'description Connected to R3 port Eth 0/0',
 'Eth 0/5': 'description Connected to R6 port Eth 0/1'}
"""
    