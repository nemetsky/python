# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""
import ipaddress


def convert_ranges_to_ip_list(ip_addresses):
    ip_list = []
    for ip_address in ip_addresses:
        if "-" in ip_address:
            start_ip, stop_ip = ip_address.split("-")
            if "." not in stop_ip:
                stop_ip = ".".join(start_ip.split(".")[:-1] + [stop_ip])
            start_ip = ipaddress.ip_address(start_ip)
            stop_ip = ipaddress.ip_address(stop_ip)
            for ip in range(int(start_ip), int(stop_ip) + 1):
                ip_list.append(str(ipaddress.ip_address(ip)))
        else:
            ip_list.append(ip_address)
    return ip_list


===============================================================================
### Мое решение ###  (Мое решение отличается) 

# У автора, если последний IP не полный, то автор находит его путем применения join по точке стартового IP и среза + последний октет
# Далее автор переводит IP в объекты, вычисляет их числовые (десятичные) значения (int) и перебирает в цикле этот диапазон числовых значений, 
# а потом снова переводи числовое значение в объект ipaddress.ip_address(ip) и потом как я переводит oбъект IP в строковый IP и добавляет в список


import subprocess
import ipaddress

def convert_ranges_to_ip_list(ip_range):
    ip_list = []
    for ip in ip_range:
        if "-" in ip:
            list1 = ip.split("-")                             # сначала разбил диапазон на 2 диапазона по "-" 
            list2 = list1[0].split(".")                       # потом разбил первый полученный диапазон по точкам
            list3 = list1[1].split(".")                       # и разбил второй полученный диапазон по точкам, если во втором нет точек (только одна цифра), то ничего не произойдет (второй диапазон будет состоять из одной цифры)
            ip_start = ipaddress.ip_address(list1[0])         # нашел первый адрес и применил функцию ip_address. Теперь IP-start - это объект      
            for i in range(int(list2[3]), int(list3[-1])+1):  # далее перебираем диапазон адресов, сам диапазон находим с помощью вычисления 4-го октета из первого диапазона и последнего октета из второго диапазона  
                ip_list.append(str(ip_start))                 # добавляем в наш искомый список первый адрес, применив к объекту str
                ip_start = ip_start +1                        # увеличиваем наш IP-адрес на 1, и так далее в цикле его последующие адреса
        else:
            ip_list.append(ip)                                # иначе просто наш строковый IP-адрес 
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

ip_range = ["172.16.50.177-172.16.50.181", "172.25.1.142", "8.8.8.8-9", "10.15.17.254"]      # почему-то некоторые адреса не пингуются, но возвращается returncode=0 (для адресов которые "Заданный узел недоступен")

if __name__ == "__main__":
    ip_list = convert_ranges_to_ip_list(ip_range)
    success_list, fail_list = ping_ip_addresses(ip_list)
    print(success_list, '- успешный ping')
    print(fail_list, '- неуспешный ping')





