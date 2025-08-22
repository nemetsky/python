# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    access_dict = {}
    trunk_dict = {}

    with open(config_filename) as cfg:
        for line in cfg:
            line = line.rstrip()
            if line.startswith("interface"):
                intf = line.split()[1]
            elif "access vlan" in line:
                access_dict[intf] = int(line.split()[-1])
            elif "trunk allowed" in line:
                trunk_dict[intf] = [int(v) for v in line.split()[-1].split(",")]
        return access_dict, trunk_dict

=========================================================================================

### Мое решение ###    (почти такое же, применил фунцию map вместо генератора списков при переводе строки в число для vlan)

def get_int_vlan_map(filename):
    dict_intf_access = {}
    dict_intf_trunk = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("interface"):
                intf = line.split()[1]                                    # разделили строку и взяли номер наименование интерфейса
            elif "switchport access vlan" in line:
                dict_intf_access[intf] = int(line.split()[-1])            # если порт access то добавили в словарь ключ (интерфейс который выше взязи) и значение (номер Vlan выдернутый из строки)
            elif "switchport trunk allowed vlan" in line:
                line = line.split(" ")[-1].rstrip()                       # если порт trunk то сначала разделили строку и вязи список vlan, удалив в конце перевод строки (\n) 
                dict_intf_trunk[intf] = list(map(int, line.split(",")))   # добавили в другой словарь ключ (интерфейс который выше взязи) и значение (список Vlan, которые получили путем разделения строки и применив фунцкцию map перевили в числа)
        return dict_intf_access, dict_intf_trunk

dict_intf_access, dict_intf_trunk = get_int_vlan_map("config_sw1.txt")
print(dict_intf_access, dict_intf_trunk)
