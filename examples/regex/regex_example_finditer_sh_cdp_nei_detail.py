"""
Задача 1. 

Регулярками с функцией finditer вывести все совпадения в файле sh_cdp_nei_detail

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
=== Набор строк, которые надо описать регуляркой ===

 'Device ID: SW2\n'
 'Entry address(es):\n'
 '  IP address: 10.1.1.2\n'
 'Platform: cisco WS-C2960-8TC-L,  Capabilities: Switch IGMP\n'
 'Interface: GigabitEthernet1/0/16,  Port ID (outgoing port): '
 'GigabitEthernet0/1\n'
 'Holdtime : 164 sec\n'
 '\n'
 'Version :\n'
 'Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9, '
 'RELEASE SOFTWARE (fc1)\n'
"""

import re
from pprint import pprint

def parse_sh_cdp_nei_det(output):
    regex = (                                  # регулярное выражение описывает набор строк (литералы (строки в регулярку) лучше добавлять по одной и проверять совпадения)
        r"Device ID: (?P<device>\S+)\n"
        r".*\n"                                # любая строка
        r" +IP address: (?P<ip>\S+)\n"
        r"Platform: (?P<platform>.+?),.*\n"
        r"(?:.*\n)+?"                          # любое количество пустых и непустых строк (.*\n), плюс отключили жадность "?" и плюс указали что эти группы не запоминать "?:"
        r"Cisco IOS Software, (?P<ios>.+),"
    )
    regex_with_dotall = (                      # вариант 2, если включаем DOTALL (когда "точка" захватывает перевод строки \n)          
        r"Device ID: (?P<device>\S+)"
        r".*?"                            
        r"IP address: (?P<ip>\S+)\s+"          # везде убираем \n где .*, но тут надо оставить или к примеру указать \s+
        r"Platform: (?P<platform>.+?),"
        r".*?"                      
        r"Cisco IOS Software, (?P<ios>.+?), RELEASE"    # здесь тогда надо указать где группа заканчивается (перед , RELEASE) и отключить жадность
    )
    result = {}
    m_all = re.finditer(regex, output)
    m_all_2 = re.finditer(regex_with_dotall, output, re.DOTALL)
    for m in m_all_2:
        # print(m.groups())
        # print(m.groupdict())
        m_dict = m.groupdict()                  # получаем словарь из наших групп спомошью метода groupdict (это плоский словарь, маленько не подходит нам, нам надо вложенные словари)
        device = m_dict.pop("device")           # чтобы сделать подсловари, удаляем ключ device и запоминаем его
        result[device] = m_dict                 # и делаем словарь где ключи это имена устройств, а подловари будут - это наши словари из groupdict
    return result
    
if __name__ == "__main__": 
    with open("sh_cdp_neighbors_sw1.txt") as f:
        content = f.read()
        # pprint(content)                       # подсмотреть полный вывод, чтобы потом регулярку подгонять
        pprint(parse_sh_cdp_nei_det(content))
