from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import repeat
import random
import time
import logging
import netmiko
import yaml
import getpass

logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s: %(message)s", level=logging.DEBUG)       # %(asctime)s  - текущее время

def send_show_command(device, password, command):
    ip = device["host"]                                             
    logging.info(f"===> Connection: {ip}")
    time.sleep(random.random()*3)         # добавили sleep для наглядности того что, подключаемся по порядку, но результаты мы можем получать не попорядку, но в выводе все равно будет все по порядку выведено с устройств       
#     if ip == "10.20.11.45":             # или так для наглядности
#         time.sleep(30)
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            output = ssh.send_command(command, read_timeout=20)             #  read_timeout=20 - увеличил для Eltex, так как команда например "sh run | i hostname" долго возвращает результат
            logging.info(f"<=== Received:   {ip}")
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")
        
if __name__ == "__main__": 
    password = getpass.getpass()
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(send_show_command, devices, repeat(password), ["sh run | i hostname"]*len(devices))      
    for output in results:        
        print(output)   
