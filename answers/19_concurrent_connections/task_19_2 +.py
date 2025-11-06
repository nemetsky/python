# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from netmiko import ConnectHandler
import yaml


def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"


def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(send_show_command, devices, repeat(command))
        with open(filename, "w") as f:
            for output in results:
                f.write(output)


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_command_to_devices(devices, command, "result.txt")


# ==============================================================================
# Мое решение #  (в отличие от автора я использовал: promt = ssh.find_prompt())

from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from pprint import pprint
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
            promt = ssh.find_prompt()                                        # добавил promt в вывод таким образом, у автора по другому
            output = promt + ssh.send_command(command, strip_command=False)
            logging.info(f"<=== Received:   {ip}")
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")
        

def send_show_command_to_devices(devices, command, filename, limit=2):
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(
            send_show_command, devices, repeat(password), repeat(command)
        )
        with open(filename, "w") as f:
            for output in results:
                f.write(output + "\n"*2)
                
            """
            # Можно сделать исключение, если вывод не получен #
            for dev, output in zip(devices, results):
                f.write(output + "\n"*2)
                try:
                    f.write(output + "\n"*2)
                except TypeError:
                    logging.warning(f"Вывод с {dev["host"]} не получен")
                    # return False                                          # можно так, если не хотим выводить никакое сообщение, а просто сделать исключение  
            """

if __name__ == "__main__": 
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_command_to_devices(devices, "sh ip int bri", "results.txt") 



######### Результат ##########

"""
c3845-inet-1#sh ip int bri
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            178.74.181.92   YES NVRAM  up                    up      
FastEthernet0/1            188.43.5.121    YES NVRAM  up                    up      
FastEthernet1/0            172.16.0.1      YES NVRAM  up                    up      
FastEthernet2/0            unassigned      YES NVRAM  administratively down down    
Loopback0                  172.25.6.102    YES NVRAM  up                    up      
Loopback11                 5.5.5.5         YES NVRAM  up                    up      
Loopback12                 5.5.5.6         YES NVRAM  up                    up      
Loopback100                100.100.100.100 YES NVRAM  up                    up      
Loopback1000               1.1.1.1         YES NVRAM  administratively down down    
Loopback1001               1.1.1.2         YES NVRAM  administratively down down    

c3845-inet-2#sh ip int bri
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            178.74.181.93   YES NVRAM  up                    up      
FastEthernet0/1            188.254.42.126  YES NVRAM  up                    up      
FastEthernet1/0            172.16.0.2      YES NVRAM  up                    up      
FastEthernet2/0            10.10.10.1      YES NVRAM  up                    up      
Loopback0                  172.25.6.103    YES NVRAM  up                    up      
Loopback11                 5.5.5.5         YES NVRAM  up                    up      
Loopback12                 5.5.5.6         YES NVRAM  up                    up      
Loopback100                100.100.100.100 YES NVRAM  administratively down down    
Loopback1000               1.1.1.1         YES NVRAM  administratively down down    
Loopback1001               1.1.1.2         YES NVRAM  administratively down down    

"""