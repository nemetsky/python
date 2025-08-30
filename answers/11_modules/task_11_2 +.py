# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну
общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.1:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.1.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from task_11_1 import parse_cdp_neighbors
from pprint import pprint

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]


def create_network_map(filenames):
    network_map = {}

    for filename in filenames:
        with open(filename) as show_command:
            parsed = parse_cdp_neighbors(show_command.read())
            network_map.update(parsed)
    return network_map


if __name__ == "__main__":
    topology = create_network_map(infiles)
    pprint(topology)

=========================================================================

### Мое решение ###   (такое же)

from pprint import pprint
#from my_functions import parse_cdp_neighbors
import my_functions

def create_network_map(filenames):
    cdp_map = {}
    for file in filenames:
        with open(file) as f:
            output = my_functions.parse_cdp_neighbors(f.read())
            cdp_map.update(output)
    return cdp_map

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

if __name__ == "__main__":
    pprint(create_network_map(infiles))


==============================================================================

### Мое усовершенствованное решение ###

"""
Оставил в словаре только не дублированные записи, т.е. из записей вида:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
оставил только одну запись
Долго мучался но получилось

"""
    
from pprint import pprint
#from my_functions import parse_cdp_neighbors
import my_functions

def create_network_map(filenames):
    cdp_map = {}
    for file in filenames:
        with open(file) as f:
            output = my_functions.parse_cdp_neighbors(f.read())
            cdp_map.update(output)
    list1 =[]
    result = cdp_map.copy()
    for key, value in cdp_map.items():
        if not key in list1:
            for key1, value1 in cdp_map.items():
                if key == value1:
                    del result[key1]    # удаляем ключ, если есть такое же значение в словаре как этот ключ
                    list1.append(key1)  # здесь добавляем ключ, значение которого совпало с ключом из верхнего цикла, в список и больше этот ключ проверяться не будет в вернем цикле (if not key in list1:)
    return result

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

if __name__ == "__main__":
    pprint(create_network_map(infiles))