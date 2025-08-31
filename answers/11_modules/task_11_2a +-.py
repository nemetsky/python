# -*- coding: utf-8 -*-
"""
Задание 11.2a

> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

С помощью функции create_network_map из задания 11.2 создать словарь topology
с описанием топологии для файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

С помощью функции draw_topology из файла draw_network_graph.py нарисовать
схему для словаря topology, полученного с помощью create_network_map.
Как работать с функцией draw_topology надо разобраться самостоятельно,
почитав описание функции в файле draw_network_graph.py.
Полученная схема будет записана в файл svg - его можно открыть браузером.

С текущим словарем topology на схеме нарисованы лишние соединения. Они
возникают потому что в одном файле CDP (sh_cdp_n_r1.txt) описывается соединение
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
а в другом (sh_cdp_n_sw1.txt)
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

В этом задании надо создать новую функцию unique_network_map, которая из этих
двух соединений будет оставлять только одно, для корректного рисования схемы.
При этом все равно какое из соединений оставить.

У функции unique_network_map должен быть один параметр topology_dict,
который ожидает как аргумент словарь.
Это должен быть словарь полученный в результате выполнения
функции create_network_map из задания 11.2.

Пример словаря:
{
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    ("SW1", "Eth0/5"): ("R6", "Eth0/1"),
}


Функция должна возвращать словарь, который описывает соединения между
устройствами. В словаре надо избавиться от "дублирующих" соединений
и оставлять только одно из них.

Структура итогового словаря такая же, как в задании 11.2:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

После создания функции, попробовать еще раз нарисовать топологию,
теперь уже для словаря, который возвращает функция unique_network_map.

Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg

При этом:
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Не копировать код функций create_network_map и draw_topology.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]


def unique_network_map(topology_dict):
    network_map = {}
    for key, value in topology_dict.items():
        if not network_map.get(value) == key:
            network_map[key] = value
    return network_map


# второй вариант решения
def unique_network_map(topology_dict):
    network_map = {}
    for key, value in topology_dict.items():
        key, value = sorted([key, value])
        network_map[key] = value
    return network_map
    

=========================================================================

### Мое решение ### 

"""
Оставил в словаре только не дублированные записи, т.е. из записей вида:
('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
оставил только одну запись

Долго мучался, но получилось. 
У автора решение по функции unique_network_map намного проще :-), 
Если хорошо подумать и разобраться, то можно понять первое решение автора (функция get берет ключ, но ключ называется как значение, и если оно равно ключу то не записывает в словарь),
Второй вариант посложнения для понимания

Нарисовать схему для словаря помощью функции draw_topology из файла draw_network_graph.py    НЕ ПОЛУЧИЛОСЬ из windows

"""

from pprint import pprint
from my_functions import parse_cdp_neighbors

def unique_network_map(dict_map):
    list1 =[]
    result = dict_map.copy()
    for key, value in dict_map.items():
        if not key in list1:
            for key1, value1 in dict_map.items():
                if key == value1:
                    del result[key1]              # удаляем ключ, если есть такое же значение в словаре как этот ключ
                    list1.append(key1)            # здесь добавляем ключ, значение которого совпало с ключом из верхнего цикла, в список и больше этот ключ проверяться не будет в вернем цикле (if not key in list1:)
    return result

def create_network_map(filenames):
    cdp_map = {}
    for file in filenames:
        with open(file) as f:
            output = parse_cdp_neighbors(f.read())
            cdp_map.update(output)
    return cdp_map

infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

if __name__ == "__main__":
    dict_map = create_network_map(infiles)
    topology_dict = unique_network_map(dict_map)
    pprint(topology_dict)


