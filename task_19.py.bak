# """
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
            for command in commands_dict[dev["host"]]:
                future = executor.submit(send_show_command, dev, password, command)
                future_list.append(future)
        
        with open(filename, "w") as f:
            for future in future_list:                  # или так    for future in as_completed(future_list):     если хотим сразу выводить результат, но будет не по порядку
                f.write(future.result() + "\n"*2)


if __name__ == "__main__":
    commands = {
        "172.16.0.1": ["sh run | s ^router ospf", "sh inventory", "sh clock"],
        "172.16.0.2": ["sh ip int br", "sh run | i hostname"]
    }
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, commands, "results.txt") 


""" 

from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler, NetMikoTimeoutException
import yaml
import logging

logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s: %(message)s", level=logging.DEBUG)


commands = {
    "172.16.0.1": ["sh run | s ^router ospf", "sh inventory", "sh clock"],
    "172.16.0.2": ["sh ip int br", "sh run | i hostname"]
}


def send_show_command(device, commands):
    output = ""
    ip = device["host"]                                             
    logging.info(f"===> Connection: {ip}")
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        for command in commands:
            result = ssh.send_command(command)
            prompt = ssh.find_prompt()
            output += f"{prompt}{command}\n{result}\n"
            logging.info(f"<=== Received:   {ip}")
    return output


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = []
        for device in devices:
            ip = device["host"]
            command = commands_dict[ip]
            futures.append(executor.submit(send_show_command, device, command))
        with open(filename, "w") as f:
            for future in as_completed(futures):
                f.write(future.result())


if __name__ == "__main__":
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    send_command_to_devices(devices, commands, "result.txt")
"""