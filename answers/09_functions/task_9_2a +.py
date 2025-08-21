# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо
  выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

def generate_trunk_config(intf_vlan_mapping, trunk_template):
    trunk_conf = {}
    for port, vlans in intf_vlan_mapping.items():
        commands = []
        for command in trunk_template:
            if command.endswith("allowed vlan"):
                vlans_str = ",".join([str(vl) for vl in vlans])
                commands.append(f"{command} {vlans_str}")
            else:
                commands.append(command)
        trunk_conf[port] = commands
    return trunk_conf

=================================================================================

### Мое решение ###    (такое же, только преобразование списка vlan из чисел в список vlan из строк и соединение строк сделал в два действия)

from pprint import pprint

trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}

def generate_trunk_config(intf_vlan_mapping, trunk_template):
    """
    intf_vlan_mapping - словарь с соответствием интерфейс-VLAN такого вида:
        {'FastEthernet0/12':10,
         'FastEthernet0/14':11,
         'FastEthernet0/16':17}
    trunk_template - список команд для порта в режиме trunk
    Возвращает словарь всех портов в режиме trunk с конфигурацией на основе шаблона
    """
    result_dict = {}
    for intf, vlans in intf_vlan_mapping.items():
        commands = []
        vlans_str = [str(vl) for vl in vlans]                   # преобразование списка vlan из чисел в список vlan из строк с помощью генератора списка
        vlans_str = " ".join(vlans_str)                         # объединение списка vlan в одну строку
        for cmd in trunk_template:
            if cmd.endswith("allowed vlan"):
                commands.append(f" {cmd} {vlans_str}")
            else:
                commands.append(f" {cmd}")
        result_dict[intf] = commands
    return result_dict

config = generate_trunk_config(trunk_config, trunk_mode_template)
pprint(config)

print(config)

