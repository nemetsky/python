# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler, NetMikoTimeoutException
import yaml


commands = {
    "192.168.100.1": "sh ip int br",
    "192.168.100.2": "sh arp",
    "192.168.100.3": "sh ip int br",
}


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [
            executor.submit(send_show_command, device, commands_dict[device["host"]])
            for device in devices
        ]
        with open(filename, "w") as f:
            for future in as_completed(futures):
                f.write(future.result())


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.load(f)
    send_command_to_devices(devices, commands, "result.txt")


# ================================================================================
# Мое решение #         (такое же, за исключением output = promt + ssh.send_command(command, strip_command=False))

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import netmiko
import yaml
import getpass

logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s: %(message)s", level=logging.DEBUG)

def send_show_command(device, password, command):
    ip = device["host"]                                             
    logging.info(f"===> Connection: {ip}")
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            promt = ssh.find_prompt()
            output = promt + ssh.send_command(command, strip_command=False)
            logging.info(f"<=== Received:   {ip}")
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")
        

def send_command_to_devices(devices, commands_dict, filename, limit=3):
    password = getpass.getpass()
    future_list = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for dev in devices:
            future = executor.submit(send_show_command, dev, password, commands_dict[dev["host"]])
            future_list.append(future)
        
        with open(filename, "w") as f:
            for future in future_list:                  # или так    for future in as_completed(future_list):     если хотим сразу выводить результат, но будет не по порядку
                f.write(future.result() + "\n"*2)


if __name__ == "__main__":
    commands = {
        "172.16.0.1": "sh run | s ^router ospf",
        "172.16.0.2": "sh ip int br",
    }
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, commands, "results.txt") 


""" Результат

c3845-inet-1#sh run | s ^router ospf
router ospf 2
 router-id 172.25.6.102
 log-adjacency-changes
 passive-interface default
 ....

c3845-inet-2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            178.74.181.93   YES NVRAM  up                    up      
FastEthernet0/1            188.254.42.126  YES NVRAM  up                    up      
FastEthernet1/0            172.16.0.2      YES NVRAM  up                    up      
...
"""
