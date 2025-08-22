# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    access_port_dict = {}
    trunk_port_dict = {}
    with open(config_filename) as f:
        for line in f:
            if line.startswith("interface FastEthernet"):
                current_interface = line.split()[-1]
                # Сразу указываем, что интерфейсу
                # соответствует 1 влан в access_port_dict
                access_port_dict[current_interface] = 1
            elif "switchport access vlan" in line:
                # если нашлось другое значение VLAN,
                # оно перепишет предыдущее соответствие
                access_port_dict[current_interface] = int(line.split()[-1])
            elif "switchport trunk allowed vlan" in line:
                vlans = [int(i) for i in line.split()[-1].split(",")]
                trunk_port_dict[current_interface] = vlans
                # если встретилась команда trunk allowed vlan
                # надо удалить интерфейс из словаря access_port_dict
                del access_port_dict[current_interface]
    return access_port_dict, trunk_port_dict


===============================================================================

### Мое решение ###    (на мой взгляд решение проще и разумнее)


def get_int_vlan_map(filename):
    dict_intf_access = {}
    dict_intf_trunk = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("interface"):
                intf = line.split()[1]
            elif "switchport mode access" in line:                      # просто добавил новое условие и если это access-порт, то присвоить ему сначала 1, а дальше если есть команда с другим vlan, то она перезапишет значение в словаре  
                dict_intf_access[intf] = 1                              # и не надо потом ничего удалять как у автора
            elif "switchport access vlan" in line:
                dict_intf_access[intf] = int(line.split()[-1])
            elif "switchport trunk allowed vlan" in line:
                line = line.split(" ")[-1].rstrip()
                dict_intf_trunk[intf] = list(map(int, line.split(",")))
        return dict_intf_access, dict_intf_trunk

dict_intf_access, dict_intf_trunk = get_int_vlan_map("config_sw2.txt")
print(dict_intf_access, dict_intf_trunk)