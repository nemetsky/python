# ============================================================================================
"""
������ 1:

����� � ���� ������ ����:
011711: May 30 2025 05:40:59.757 MSK: %SW_MATM-4-MACFLAP_NOTIF: Host 0007.b400.6a02 in vlan 106 is flapping between port Po100 and port Po103
� � ������� ��������� ����� ��������� ������ ����� �������� ��������
"""

"""
import re

regex = r"Host (\S+) .+ port (\S+) and port (\S+)"
ports = set()

with open("log.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:                         # �����������, ��� ��� ���� ���������� ���, �� ��������� None, � None ��� ������ groups, ������� ����� ������
            print(match.groups())         # ����� ������ ���� ����� ('0007.b400.a002', 'Po103', 'Po100')
            ports.update(match.group(2,3))
print("\n")
print(ports)                              # ��������� ������ ����� �������� ���������� flapping
"""
"""
���������:
('0007.b400.a002', 'Po103', 'Po100')
('0020.cee2.1da2', 'Po100', 'Po5')
('0020.cee2.1da2', 'Po100', 'Po5')
('0007.b400.a002', 'Po103', 'Po100')
....
{'Gi2/0/37', 'Po103', 'Po5', 'Po101', 'Gi1/0/14', 'Gi1/0/12', 'Po111', 'Po100', 'Po43'}
"""

# ============================================================================================

"""
������ 2:

������ ������� ������ ������ (������� ������ �� ������ show_ip_int_br), ������� ����� ���������:

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
regex = r"(\S+) +([\d.]+) +\S+ +\w+ +(up|down) +(up|down)"             # �������� ������� 6 �������� � 4 ��������� �� ���

with open("sh_ip_int_br.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:                         
            result_list.append(list(match.groups()))
            
pprint(result_list)
"""

"""
���������:
[['FastEthernet0/0', '15.0.15.1', 'up', 'up'],
 ['FastEthernet0/1', '10.0.12.1', 'up', 'up'],
 ['FastEthernet0/2', '10.0.13.1', 'up', 'up'],
 ['FastEthernet0/3', 'unassigned', 'up', 'down'],                 # ([\d.]+)  - � ����� ��������� �� ������� ��� ������
 ['Loopback0', '10.1.1.1', 'up', 'up'],
 ['Loopback100', '100.0.0.1', 'up', 'up']]
"""

# ============================================================================================

"""
������ 3 (��� ������ 2 ����� �������)
"""

"""
import re
from pprint import pprint

def parse_sh_int_br(output):
    result_list = []
    #regex = r"(\S+) +([\d.]+) +\S+ +\w+ +(up|down) +(up|down)"             # �������� ������� 6 �������� � 4 ��������� �� ���
    regex = r"(\S+) +([\d.]+|unassigned) +\S+ +\w+ +(up|down) +(up|down)"   # ([\d.]+|unassigned)  - ��� c IP ��� ��� 
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
������ 4 (��� ������ 3, ������ ���������� �������)
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
            # result_dict.update({intf: ip})      # ����� ��� � ������� ������� ������, �� ����� ��� ������� ����
            result_dict[intf] = ip
    return result_dict

if __name__ == "__main__":    
    with open("sh_ip_int_br.txt") as f:
        content = f.read()
        result = parse_sh_int_br(content)
    pprint(result)

""" 
���������
{'FastEthernet0/0': '15.0.15.1',
 'FastEthernet0/1': '10.0.12.1',
 'FastEthernet0/2': '10.0.13.1',
 'FastEthernet0/3': 'unassigned',
 'Loopback0': '10.1.1.1',
 'Loopback100': '100.0.0.1'}
"""
# ============================================================================================



