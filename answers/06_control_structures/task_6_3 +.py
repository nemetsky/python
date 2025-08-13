# -*- coding: utf-8 -*-
"""
Задание 6.3

В скрипте сделан генератор конфигурации для access-портов.
Сделать аналогичный генератор конфигурации для портов trunk.

В транках ситуация усложняется тем, что VLANов может быть много, и надо понимать,
что с ними делать (добавлять, удалять, перезаписывать).

Поэтому в соответствии каждому порту стоит список и первый (нулевой) элемент списка
указывает как воспринимать номера VLAN, которые идут дальше.

Пример значения и соответствующей команды:
* ['add', '10', '20'] - команда switchport trunk allowed vlan add 10,20
* ['del', '17'] - команда switchport trunk allowed vlan remove 17
* ['only', '11', '30'] - команда switchport trunk allowed vlan 11,30

Задача для портов 0/1, 0/2, 0/4:
- сгенерировать конфигурацию на основе шаблона trunk_template
- с учетом ключевых слов add, del, only

Код не должен привязываться к конкретным номерам портов. То есть,
если в словаре trunk будут другие номера интерфейсов, код должен работать.

Для данных в словаре trunk_template вывод на
стандартный поток вывода должен быть таким:
interface FastEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan add 10,20
interface FastEthernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 11,30
interface FastEthernet0/4
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan remove 17

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan",
]

access = {"0/12": "10", "0/14": "11", "0/16": "17", "0/17": "150"}
trunk = {"0/1": ["add", "10", "20"], "0/2": ["only", "11", "30"], "0/4": ["del", "17"]}

for intf, value in trunk.items():
    print(f"interface FastEthernet{intf}")
    for command in trunk_template:
        if command.endswith("allowed vlan"):
            action = value[0]
            vlans = ",".join(value[1:])

            if action == "add":
                print(f" {command} add {vlans}")
            elif action == "only":
                print(f" {command} {vlans}")
            elif action == "del":
                print(f" {command} remove {vlans}")
        else:
            print(f" {command}")


# этот вариант использует словарь, вместо if/else
trunk_actions = {"add": " add", "del": " remove", "only": ""}

for intf, value in trunk.items():
    print(f"interface FastEthernet{intf}")

    for command in trunk_template:
        if command.endswith("allowed vlan"):
            action = value[0]
            vlans = ",".join(value[1:])
            print(f" {command}{trunk_actions[action]} {vlans}")
        else:
            print(f" {command}")

# вариант с заменой
for intf, allowed in trunk.items():
    action = (
        allowed[0].replace("only", "").replace("del", " remove").replace("add", " add")
    )
    vlans = ",".join(allowed[1:])

    print(f"interface FastEthernet{intf}")
    for command in trunk_template:
        if command.endswith("allowed vlan"):
            print(f" {command}{action} {vlans}")
        else:
            print(f" {command}")



==============================================================================================

### Мое решение ### (я не использовал срез, а использовал pop). У автора решения со словарем и с заменой интересные

access_template = [
    "switchport mode access",
    "switchport access vlan",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan",
]

access = {"0/12": "10", "0/14": "11", "0/16": "17", "0/17": "150"}
trunk = {
    "0/1": ["add", "10", "20"],
    "0/2": ["only", "11", "30"],
    "0/4": ["del", "17"],
    "0/5": ["add", "10", "21"],
    "0/7": ["only", "30"],
}

# Скрипт для access порта
#
# for intf, vlan in access.items():
#     print("interface FastEthernet" + intf)
#     for command in access_template:
#         if command.endswith("access vlan"):
#             print(f" {command} {vlan}")
#         else:
#             print(f" {command}")

for intf, vlan in trunk.items():                        # распаковываем и перебираем словарь
    print("interface FastEthernet" + intf)              # выводим интерфейс с номером
    for command in trunk_template:                      # перебираем строки в шаблоне (списке)
        if command.endswith("vlan"):                    # если строка заканчивается на vlan
            if vlan[0] == "add":                        # проверяем в словаре первое значение для интерфейса
                s1 = vlan.pop(0)                        # вместо среза использую pop, который удаляет первый элемент списка и присваевает отдельной переменной
                s2 = ",".join(vlan)                     # оставшиесы элементы списка (вланы) присваеваем строке
                print(f" {command} {s1} {s2}")          # выводим команду
            elif vlan[0] == "del":
                vlan.pop(0)
                s2 = ",".join(vlan)
                print(f" {command} remove {s2}")
            else: 
                vlan.pop(0)
                s2 = ",".join(vlan)
                print(f" {command} {s2}")
        else:
            print(f" {command}")
      