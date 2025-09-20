# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re


def convert_ios_nat_to_asa(cisco_ios, cisco_asa):
    regex = (
        "tcp (?P<local_ip>\S+) +(?P<lport>\d+) +interface +\S+ (?P<outside_port>\d+)"
    )
    asa_template = (
        "object network LOCAL_{local_ip}\n"
        " host {local_ip}\n"
        " nat (inside,outside) static interface service tcp {lport} {outside_port}\n"
    )
    with open(cisco_ios) as f, open(cisco_asa, "w") as asa_nat_cfg:
        data = re.finditer(regex, f.read())
        for match in data:
            asa_nat_cfg.write(asa_template.format(**match.groupdict()))               # ** - арументы передать в виде словаря, match.groupdict() делает как раз словарь из совпадений - "имя группы" : значение
                                                                                      # так имя группы совпадает с именем в шаблоне, то значение подставляется в шаблон


if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "cisco_asa_config.txt")


# ==========================================================================================

### Мое решение ### (сделано может и некрасиво, но работает точно также)

import re

def convert_ios_nat_to_asa(filename_ios, filename_asa):
    template = """                                                                    # некрасивый шаблон у меня, но зато индексы применил)
object network LOCAL_{0}
 host {0}
 nat (inside,outside) static interface service tcp {1} {2}
""" 
    regex = (r"tcp (?P<ip>[\d.]+) (?P<port_1>\d+) \S+ \S+ (?P<port_2>\d+)")           # имена групп можно было и не делать, я их не использовал дальше
    with open(filename_ios) as f1:
        nat_list = f1.readlines()                                                     # считал строки файли в лист
    with open(filename_asa, "w") as f2:
        for s in nat_list:
            m = re.search(regex,s)                                                    # находим совпадения по регулярке                                  
            ip, port_local, port_global = m.groups()
            result = template.format(ip, port_local, port_global).lstrip()            # передаем в шаблон ранее распакованные переменные из найденных групп, удаляем лишний пробел в начале шалона
            f2.write(result)
            
if __name__ == "__main__":
    convert_ios_nat_to_asa("cisco_nat_config.txt", "asa_nat_config.txt")
    











