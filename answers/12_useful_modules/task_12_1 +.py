# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess


def ping_ip_addresses(ip_addresses):
    reachable = []
    unreachable = []

    for ip in ip_addresses:
        result = subprocess.run(
            ["ping", "-c", "3", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            reachable.append(ip)
        else:
            unreachable.append(ip)

    return reachable, unreachable


if __name__ == "__main__":
    print(ping_ip_addresses(["10.1.1.1", "8.8.8.8"]))

===============================================================

### Мое решение ###  (такое же)

import subprocess

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

ip_list = ["172.16.50.177", "10.15.17.254", "8.8.8.8"]

if __name__ == "__main__":
    success_list, fail_list = ping_ip_addresses(ip_list)
    print(success_list, '- успешный ping')
    print(fail_list, '- неуспешный ping')
    
 