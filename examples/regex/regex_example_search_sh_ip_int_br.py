# ============================================================================================
"""
Задача 1:

Найти в логе записи вида:
011711: May 30 2025 05:40:59.757 MSK: %SW_MATM-4-MACFLAP_NOTIF: Host 0007.b400.6a02 in vlan 106 is flapping between port Po100 and port Po103
и с помощью регул€рок найти множество портов между которыми флаппинг
"""

"""
import re

regex = r"Host (\S+) .+ port (\S+) and port (\S+)"
ports = set()

with open("log.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:                         # об€зательно, так как если совпадени€ нет, то результат None, а None нет метода groups, поэтому будет ошибка
            print(match.groups())         # вывод такого вида будет ('0007.b400.a002', 'Po103', 'Po100')
            ports.update(match.group(2,3))
print("\n")
print(ports)                              # множество портов между которыми происходит flapping
"""
"""
–езультат:
('0007.b400.a002', 'Po103', 'Po100')
('0020.cee2.1da2', 'Po100', 'Po5')
('0020.cee2.1da2', 'Po100', 'Po5')
('0007.b400.a002', 'Po103', 'Po100')
....
{'Gi2/0/37', 'Po103', 'Po5', 'Po101', 'Gi1/0/14', 'Gi1/0/12', 'Po111', 'Po100', 'Po43'}
"""

# ============================================================================================

"""
Задача 2:

задачу которую решали раньше (сделать список из вывода show_ip_int_br), сделать через регул€рки:

from pprint import pprint
result_list = []
with open("sh_ip_int_br.txt", "r") as f:            
    for line in f:                                  
        line_list = line.split()                    
        if line_list and line_list[0][-1].isdigit():
            intf_ip_list = line_list[:2] + line_list[-2:]
            result_list.append(intf_ip_list)
pprint(result_list)
"""

"""
import re
from pprint import pprint

result_list = []
regex = r"(\S+) +([\d.]+) +\S+ +\w+ +(up|down) +(up|down)"             # рег€ркой описали 6 столбцов и 4 запомнили из них

with open("sh_ip_int_br.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:                         
            result_list.append(list(match.groups()))
            
pprint(result_list)
"""

"""
Результат:
[['FastEthernet0/0', '15.0.15.1', 'up', 'up'],
 ['FastEthernet0/1', '10.0.12.1', 'up', 'up'],
 ['FastEthernet0/2', '10.0.13.1', 'up', 'up'],
 ['FastEthernet0/3', 'unassigned', 'up', 'down'],                 # ([\d.]+)  - в такой регул€рке не попадет эта строка
 ['Loopback0', '10.1.1.1', 'up', 'up'],
 ['Loopback100', '100.0.0.1', 'up', 'up']]
"""

# ============================================================================================

"""
Задача 3 (это «адача 2 через функцию)
"""

"""
import re
from pprint import pprint

def parse_sh_int_br(output):
    result_list = []
    #regex = r"(\S+) +([\d.]+) +\S+ +\w+ +(up|down) +(up|down)"             # рег€ркой описали 6 столбцов и 4 запомнили из них
    regex = r"(\S+) +([\d.]+|unassigned) +\S+ +\w+ +(up|down) +(up|down)"   # ([\d.]+|unassigned)  - или c IP или без 
    for line in output.split("\n"):
        match = re.search(regex, line)
        if match:                         
            result_list.append(list(match.groups()))
    return result_list

if __name__ == "__main__":    
    with open("sh_ip_int_br.txt") as f:
        content = f.read()
        result = parse_sh_int_br(content)
    pprint(result)
"""

# ============================================================================================

"""
Задача 4 (это «адача 3, только используем словарь)
"""

import re
from pprint import pprint

def parse_sh_int_br(output):
    result_dict = {}
    regex = r"^(\S+) +([\d.]+|unassigned)"
    for line in output.split("\n"):
        match = re.search(regex, line)
        if match:  
            intf = match.group(1)
            ip =  match.group(2)
            # result_dict.update({intf: ip})      # можно так в словарь занести запись, но лучше как сделано ниже
            result_dict[intf] = ip
    return result_dict

if __name__ == "__main__":    
    with open("sh_ip_int_br.txt") as f:
        content = f.read()
        result = parse_sh_int_br(content)
    pprint(result)

""" 
Результат
{'FastEthernet0/0': '15.0.15.1',
 'FastEthernet0/1': '10.0.12.1',
 'FastEthernet0/2': '10.0.13.1',
 'FastEthernet0/3': 'unassigned',
 'Loopback0': '10.1.1.1',
 'Loopback100': '100.0.0.1'}
"""
# ============================================================================================



