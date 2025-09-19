# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re

# первый способ

def get_ints_without_description(config):
    regex = re.compile(r"!\ninterface (?P<intf>\S+)\n"
                       r"(?P<descr> description \S+)?")
    with open(config) as src:
        match = regex.finditer(src.read())
        result = [m.group('intf') for m in match if m.lastgroup == 'intf']
        return result

# второй способ

def get_ints_without_description(filename):
    result_list = []
    regex = r"^interface (?P<intf>\S+)|^ description (.+)\n"
    with open(filename) as f:
        for line in f:
            match_line = re.search(regex, line)
            if match_line:
                if match_line.lastgroup == "intf":
                    intf = match_line.group("intf")
                    result_list.append(intf)
                else:
                    result_list.remove(intf)
    return result_list
    
    
# ===============================================================

### Мое решение ###   (мое решение совсем другое, и на мой взгляд намного проще)

import re

def get_ints_without_description(filename):
    regex = r"^interface (\S+)\n (\S+)"
    result = []   
    with open(filename) as f:
        match = re.finditer(regex, f.read(), re.MULTILINE)          # re.MULTILINE - чтобы в ркгулярке работал ^ к каждой строке
        for m in match:
            if m.group(2) != "description":
                result.append(m.group(1))
    return result    
            
if __name__ == "__main__":
    print(get_ints_without_description("config_r1.txt"))
    
    
# Результат: ['Loopback0', 'Tunnel0', 'Ethernet0/1', 'Ethernet0/3.100', 'Ethernet1/0']  
    

