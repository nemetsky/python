# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""
import yaml
import glob
from task_17_3 import parse_sh_cdp_neighbors


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    topology = {}
    for filename in list_of_files:
        with open(filename) as f:
            topology.update(parse_sh_cdp_neighbors(f.read()))                   # автор использует функцию parse_sh_cdp_neighbors из предыдущей задачи
    if save_to_filename:
        with open(save_to_filename, "w") as f_out:
            yaml.dump(topology, f_out, default_flow_style=False)
    return topology


if __name__ == "__main__":
    f_list = glob.glob("sh_cdp_n_*")
    print(generate_topology_from_cdp(f_list, save_to_filename="topology.yaml"))


# ======================================================================================

### Мое решение ###     (в принципе такое же как у автора, только он использует функцию parse_sh_cdp_neighbors из предыдущей задачи 17_3)
                      # (а я не стал ее использовать и в этой задаче все сделал в фунцкии generate_topology_from_cdp) 

import re
import yaml
from glob import glob
from pprint import pprint

def generate_topology_from_cdp(list_of_files, save_to_filename=None):                       # описание в предыдущем примере
    regex = re.compile(r"(?P<hostname>\S+) +"
                       r"(?P<l_intf>\S+ [0-9\/]+)"
                       r" +\d+ +(?:[\S+ ]+) +\S+ +"
                       r"(?P<r_intf>\S+ [0-9\/]+)")
    topology = {}
    for file in list_of_files:
        with open(file) as f:
            output = f.read()                                                               # считываем содержимое файла в переменную
            match = regex.finditer(output)                                                  # применяем регулярку
            device = re.search(r"(\S+)>sh", output).group(1)                                # находим имя устройства в которого вывод
            cdp_dict = {}
            for m in match:
                hostname, local_potr, remote_port = m.group("hostname", "l_intf", "r_intf") 
                cdp_dict[local_potr] = {hostname: remote_port}                              # делаем подсловари
            topology[device] = cdp_dict                                                     # записываем подсловари в главный словарь
    if save_to_filename:                                                                    # если передан аргумент для вывода в файл YAML, то записываем в файл YAML
        with open(save_to_filename, "w") as f_out:
            yaml.dump(topology, f_out)
    return topology

if __name__ == "__main__":
    files = glob("sh_cdp_n_*")
    pprint(generate_topology_from_cdp(files, "resutls_17_3a.yaml"))
    
"""
Результат: 

{'R1': {'Eth 0/0': {'SW1': 'Eth 0/1'}},
 'R2': {'Eth 0/0': {'SW1': 'Eth 0/2'},
        'Eth 0/1': {'R5': 'Eth 0/0'},
        'Eth 0/2': {'R6': 'Eth 0/1'}},
 'R3': {'Eth 0/0': {'SW1': 'Eth 0/3'}},
 'R4': {'Eth 0/0': {'SW1': 'Eth 0/4'}, 'Eth 0/1': {'R5': 'Eth 0/1'}},
 'R5': {'Eth 0/0': {'R2': 'Eth 0/1'}, 'Eth 0/1': {'R4': 'Eth 0/1'}},
 'R6': {'Eth 0/1': {'R2': 'Eth 0/2'}},
 'SW1': {'Eth 0/1': {'R1': 'Eth 0/0'},
         'Eth 0/2': {'R2': 'Eth 0/0'},
         'Eth 0/3': {'R3': 'Eth 0/0'},
         'Eth 0/5': {'R6': 'Eth 0/1'}}}
  
  
Файл YAML:

R1:
  Eth 0/0:
    SW1: Eth 0/1
R2:
  Eth 0/0:
    SW1: Eth 0/2
  Eth 0/1:
    R5: Eth 0/0
  Eth 0/2:
    R6: Eth 0/1
R3:
  Eth 0/0:
    SW1: Eth 0/3
R4:
  Eth 0/0:
    SW1: Eth 0/4
  Eth 0/1:
    R5: Eth 0/1
R5:
  Eth 0/0:
    R2: Eth 0/1
  Eth 0/1:
    R4: Eth 0/1
R6:
  Eth 0/1:
    R2: Eth 0/2
SW1:
  Eth 0/1:
    R1: Eth 0/0
  Eth 0/2:
    R2: Eth 0/0
  Eth 0/3:
    R3: Eth 0/0
  Eth 0/5:
    R6: Eth 0/1

"""