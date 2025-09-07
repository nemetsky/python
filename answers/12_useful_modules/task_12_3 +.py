# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from tabulate import tabulate


def print_ip_table(reach_ip, unreach_ip):
    table = {"Reachable": reach_ip, "Unreachable": unreach_ip}
    print(tabulate(table, headers="keys"))


if __name__ == "__main__":
    reach_ip = ["10.1.1.1", "10.1.1.2"]
    unreach_ip = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]
    print_ip_table(reach_ip, unreach_ip)


=====================================================================

### Мое решение ###

# Работу функции print_ip_table проверить не удалось, так как надо ставить модуль tabulate, поэтому рещение по фунцкии подсмотрел у автора

import subprocess
import ipaddress
from tabulate import tabulate

def convert_ranges_to_ip_list(ip_range):
    ip_list = []
    for ip in ip_range:
        if "-" in ip:
            list1 = ip.split("-")                             
            list2 = list1[0].split(".")                       
            list3 = list1[1].split(".")                       
            ip_start = ipaddress.ip_address(list1[0])         
            for i in range(int(list2[3]), int(list3[-1])+1):  
                ip_list.append(str(ip_start))                 
                ip_start = ip_start +1                        
        else:
            ip_list.append(ip)                                
    return ip_list
                
def ping_ip_addresses(ip_list):
    success_list = []
    fail_list = []
    for ip in ip_list:
        check_ip = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check_ip.returncode == 0:
            success_list.append(ip)
        else:
            fail_list.append(ip)
    return success_list, fail_list

def print_ip_table(success_list, fail_list):                                                    # задание на эту функцию, остальные функции расписаны в предыдущих заданиях
    table = {"Reachable": success_list, "Unreachable": fail_list}
    print(tabulate(table, headers="keys"))

ip_range = ["172.16.50.177-172.16.50.181", "172.25.1.142", "8.8.8.8-9", "10.15.17.254"]    

if __name__ == "__main__":
    ip_list = convert_ranges_to_ip_list(ip_range)
    success_list, fail_list = ping_ip_addresses(ip_list)
    print_ip_table(success_list, fail_list)

"""
=== Результат ===


Reachable    Unreachable
-----------  -------------
8.8.8.8      172.16.50.177
             172.16.50.178
             172.25.1.142
             8.8.8.9
"""