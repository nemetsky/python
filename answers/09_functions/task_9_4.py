# -*- coding: utf-8 -*-
"""
Задание 9.4

Создать функцию convert_config_to_dict, которая обрабатывает конфигурационный
файл коммутатора и возвращает словарь:
* Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
* Если у команды верхнего уровня есть подкоманды, они должны быть в значении
  у соответствующего ключа, в виде списка (пробелы в начале строки надо удалить).
* Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются
с '!', а также строки в которых содержатся слова из списка ignore.

Для проверки надо ли игнорировать строку, использовать функцию ignore_command.

Часть словаря, который должна возвращать функция (полный вывод можно посмотреть
в тесте test_task_9_4.py):
{
    "version 15.0": [],
    "service timestamps debug datetime msec": [],
    "service timestamps log datetime msec": [],
    "no service password-encryption": [],
    "hostname sw1": [],
    "interface FastEthernet0/0": [
        "switchport mode access",
        "switchport access vlan 10",
    ],
    "interface FastEthernet0/1": [
        "switchport trunk encapsulation dot1q",
        "switchport trunk allowed vlan 100,200",
        "switchport mode trunk",
    ],
    "interface FastEthernet0/2": [
        "switchport mode access",
        "switchport access vlan 20",
    ],
}

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ignore = ["duplex", "alias", "configuration"]


def ignore_command(command, ignore):
    """
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    """
    ignore_status = False
    for word in ignore:
        if word in command:
            ignore_status = True
    return ignore_status


def convert_config_to_dict(config_filename):
    config_dict = {}
    with open(config_filename) as f:
        for line in f:
            line = line.rstrip()
            if line and not (line.startswith("!") or ignore_command(line, ignore)):
                if line[0].isalnum():
                    section = line
                    config_dict[section] = []
                else:
                    config_dict[section].append(line.strip())
    return config_dict

=======================================================================================

### Мое решение ###   (идея у меня была такая же как у автора, но не получалось решить задачу, 3 строки подсмотрел у автора)

from pprint import pprint

ignore = ["duplex", "alias", "configuration"]

def ignore_command(command, ignore):
    """
    Функция проверяет содержится ли в команде слово из списка ignore.
    command - строка. Команда, которую надо проверить
    ignore - список. Список слов
    Возвращает:
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    """
    ignore_status = False
    for word in ignore:
        if word in command:
            ignore_status = True
    return ignore_status

def convert_config_to_dict(filename):
    config_dict = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if not line or "!" in line or ignore_command(line, ignore):
                continue
            elif not line.startswith(" "):                      # у автора в этом месте используется функция isalnum(), которая проверяет символ, что он буквенно-цифровой 
                section = line                                  # решение подсмотрел у автора
                config_dict[section] = []                       # решение подсмотрел у автора
            else:
                config_dict[section].append(line.strip())       # решение подсмотрел у автора
    return config_dict

config_dict = convert_config_to_dict("config_sw1.txt")
pprint(config_dict, sort_dicts=False)                           # почему-то включена по умолчанию сортировка, хотя не должна быть включена, принудительно выключил


