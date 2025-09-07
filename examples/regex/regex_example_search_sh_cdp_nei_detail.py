"""
������ 1. 

����������� � �������� ����� ������� ������� � ������������ (���, �����, ���������, ������)
�� ������ sh cdp nei detail

=== ��������� ===

{'R1': {'ios': {'3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1'},
        'ip': {'10.1.1.1'},
        'platform': {'Cisco 3825'}},
 'R2': {'ios': {'2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1'},
        'ip': {'10.2.2.2'},
        'platform': {'Cisco 2911'}},
 'SW2': {'ios': {'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9'},
         'ip': {'10.1.1.2'},
         'platform': {'cisco WS-C2960-8TC-L'}}}

"""
"""
import re
from pprint import pprint

result = {}

with open("sh_cdp_neighbors_sw1.txt") as f:
    for line in f:
        if line.startswith("Device ID"):
            device = re.search(r"Device ID: (\S+)", line).group(1)      # ������� ���������� ��� ����������, (\S+) - ������ � �������, ����� �� .group(1) ����������� ���������� device 
            result[device] = {}                                         # ������ ��������� ������� {'R1': {}, 'R2': {}, 'SW2': {}}
        elif "IP address" in line:
            ip = re.search(r"IP address: (\S+)", line).group(1)
            result[device]["ip"] = {ip}                                 # ������� ���������� ����� � ������� ���� � ���������� ip �� ��������� ������ {'R1': {'ip': {'10.1.1.1'}}, 'R2': {'ip': {'10.2.2.2'}}, 'SW2': {'ip': {'10.1.1.2'}}}
        elif line.startswith("Platform"):
            platform = re.search(r"Platform: (.+?),", line).group(1)    # ��������� � ������ �������� �� �������, �� ������ ������ ��������� �������� ?, ����� � ������ ����� ��������� �������
            result[device]["platform"] = {platform}                     # ���������� � ���������� ��������� ����������
        elif line.startswith("Cisco IOS"):
            ios = re.search(r"Cisco IOS Software, (.+),", line).group(1)
            result[device]["ios"] = {ios}                 

pprint(result)
"""

# ================================================================================

"""
������ 2. 

��� � ������ 1, ������ ��� ������� ����� ��������� (��� ������ �����), ��� ������ ���������� ��� ����������
"""

import re
from pprint import pprint

regex = (                                # ������� �� �������� ��������� ��� ��������, ��������� � ��������� "���" |
    r"Device ID: (?P<device>\S+)"
    r"|IP address: (?P<ip>\S+)"
    r"|Platform: (?P<platform>.+?),"
    r"|Cisco IOS Software, (?P<ios>.+),"
    r"|Duplex: (?P<duplex>\S+)"                                   # �������� ��� ��������, ��� ����� ��� ������ ��������� � �����, �� ����� �������� ���
    r"|Interface: (?P<local_port>\S+), .+: (?P<remote_port>\S+)"  # ����� �������� ���������, �� �.�. � ������ ��� ���������� (������) � ����� ������, �� ����� ������ ������ ���������� remote_port
)                                                                 # ����� ���� ������� ��������, ����� ������� ��� � local_port

result = {}

with open("sh_cdp_neighbors_sw1.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:
            group = match.lastgroup            # ����������� ���������� group ��� ��������� ������, ��� ��� ����� ����� � ������� (���� ����� � ������� �� ����������, �� ����� �� ������� ������� lastindex)
            value = match.group(group)         # ������� �������� ���� ��������� ������ 
            #print(f"{line=}")
            #print(f"{group=}")                # ������ ��� ���������
            #print(f"{value=}")
            if group == "device":
                result[value] = {}             # ������� ����������
                device = value                 # � ���������� ���������� �� ����������
            elif group == "remote_port":       # ��� ������� ��� ����������� ��������, ��� ���������� � ���������, �.�. 2 ���������� � ����� ������, �� local_port ���� ���� �������
                result[device][group] = value
                result[device]["local_port"] = match.group("local_port")
            else:                                   
                result[device][group] = value  # ���������� � ���������� ����� �� ��������� (������ ����� ��� ������ ���������, �������� ��� ��������� ��������� ���� ������) 
            """                                # ������ 3-� ������ �������, ����� ������� else. � else ��� ������ �.�. ���� �����  � ������� �������� ������, �� ��� ������ � ��������� ���� �������� ���������
            elif group == "ip":                
                result[device]["ip"] = value
            elif group == "platform":
                result[device]["platform"] = value
            elif group == "ios":
                result[device]["ios"] = value
            """
pprint(result)




