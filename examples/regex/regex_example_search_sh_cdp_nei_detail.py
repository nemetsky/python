"""
Задача 1. 

Регулярками и методами строк сделать словарь с устройствами (имя, адрес, платформа, версия)
из вывода sh cdp nei detail

=== Результат ===

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
            device = re.search(r"Device ID: (\S+)", line).group(1)      # находим регуляркой имя устройства, (\S+) - группа с адресом, потом ее .group(1) присваеваем переменной device 
            result[device] = {}                                         # делаем вложенный словарь {'R1': {}, 'R2': {}, 'SW2': {}}
        elif "IP address" in line:
            ip = re.search(r"IP address: (\S+)", line).group(1)
            result[device]["ip"] = {ip}                                 # находим регуляркой адрес и создаем ключ в подсловаре ip со значением адреса {'R1': {'ip': {'10.1.1.1'}}, 'R2': {'ip': {'10.2.2.2'}}, 'SW2': {'ip': {'10.1.1.2'}}}
        elif line.startswith("Platform"):
            platform = re.search(r"Platform: (.+?),", line).group(1)    # считываем в группу значение до запятой, на всякий случай отключили жадность ?, вдруг в строке будет несколько запятых
            result[device]["platform"] = {platform}                     # записываем в подсловарь платформу устройства
        elif line.startswith("Cisco IOS"):
            ios = re.search(r"Cisco IOS Software, (.+),", line).group(1)
            result[device]["ios"] = {ios}                 

pprint(result)
"""

# ================================================================================

"""
Задача 2. 

Как и задача 1, только все сделать через регулярки (без метода строк), еще вывели интерфейсы для усложнения
"""

import re
from pprint import pprint

regex = (                                # разбили на литералы регулярку для удобства, применяем в регулярке "или" |
    r"Device ID: (?P<device>\S+)"
    r"|IP address: (?P<ip>\S+)"
    r"|Platform: (?P<platform>.+?),"
    r"|Cisco IOS Software, (?P<ios>.+),"
    r"|Duplex: (?P<duplex>\S+)"                                   # добавили для проверки, что можем что угодно добавлять в вывод, не меняя основной код
    r"|Interface: (?P<local_port>\S+), .+: (?P<remote_port>\S+)"  # можно добавить интерфейс, но т.к. в выводе два совпадения (группы) в одной строке, то будет всегда второе совпадение remote_port
)                                                                 # тогда надо условие добавить, чтобы вывести еще и local_port

result = {}

with open("sh_cdp_neighbors_sw1.txt") as f:
    for line in f:
        match = re.search(regex, line)
        if match:
            group = match.lastgroup            # присваеваем переменной group имя совпавшей группы, это для имени ключа в словаре (если имена в группах не используем, то можно по индексу матчить lastindex)
            value = match.group(group)         # находим значение этой совпавшей группы 
            #print(f"{line=}")
            #print(f"{group=}")                # выводы для понимания
            #print(f"{value=}")
            if group == "device":
                result[value] = {}             # создаем подсловарь
                device = value                 # в переменную записываем им устройства
            elif group == "remote_port":       # это условие для интерфейсов добавили, для усложнения и понимания, т.к. 2 совпадения в одной строке, то local_port надо тоже вывести
                result[device][group] = value
                result[device]["local_port"] = match.group("local_port")
            else:                                   
                result[device][group] = value  # записываем в подсловарь ключи со значением (ключом будеи имя группы совпавшей, значение это результат регурярки этой группы) 
            """                                # вместо 3-х нижних условий, можно сделать else. С else тут удобно т.к. если хотим  в словарь добавить данные, то нам только в регулярке надо добавить изменения
            elif group == "ip":                
                result[device]["ip"] = value
            elif group == "platform":
                result[device]["platform"] = value
            elif group == "ios":
                result[device]["ios"] = value
            """
pprint(result)




