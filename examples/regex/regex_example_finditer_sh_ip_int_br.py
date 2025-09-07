"""
������ 1. 

����������� ������� ��� ���������� � ����� sh_ip_int_br

=== ��������� ===

[('FastEthernet0/0', '15.0.15.1', 'up', 'up')
('FastEthernet0/1', '10.0.12.1', 'up', 'up')
('Loopback100', '100.0.0.1', 'up', 'up')]

"""

import re
from pprint import pprint

def parse_sh_ip_int_br(output):
    regex = r"(\S+) +(\S+) +\w+ +\w+ +(up|down) +(up|down)" 
    all_match = re.finditer(regex, output)                    # ��������� finditer �� ����� �����
    results = [match.groups() for match in all_match]         # ��� ��� ��� ��������, �� ���������� � ����� (� ������ ������ � ������� ����������)
    return results
    
if __name__ == "__main__": 
    with open("sh_ip_int_br.txt") as f:
        content = f.read()
        pprint(parse_sh_ip_int_br(content))
    
    