from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import repeat
import logging
import netmiko
import yaml
import getpass

logging.getLogger("netmiko").setLevel(logging.INFO)
logging.getLogger("paramiko").setLevel(logging.INFO)

logging.basicConfig(format="%(threadName)s %(name)s %(levelname)s: %(message)s", level=logging.DEBUG)

def send_show_command(device, password, command):
    start_msg = "===> {} Connection: {}"
    received_msg = "<=== {} Received: {}"
    ip = device["host"]                                             
    logging.info(start_msg.format(datetime.now().time(), ip))                   # datetime.now().time() - текущее время
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            output = ssh.send_command(command)
            logging.info(received_msg.format(datetime.now().time(), ip))
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")
        
if __name__ == "__main__": 
    command = "sh clock"
    password = getpass.getpass()
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        
#   Пример без контекста
#   здесь раньше был цикл с перебором устройств, теперь он не нужен
    executor = ThreadPoolExecutor(max_workers=2)                                                      # сколько потоков использовать для подключения
#    q = executor.map(send_show_command, devices, repeat(password), ["sh clock", "sh inventory"])
#    q = executor.map(send_show_command, devices, repeat(password), ["sh clock"]*len(devices))        # ["sh clock"]*len(devices)  --- >  ["sh clock", "sh clock"]  # если в словаре 2 устройства
    q = executor.map(send_show_command, devices, repeat(password), repeat(command))#                  # если забыть повторить (repeat) команду, то будет по одному символу из команды на каждое устройство отправляться 
                                                                                                      # с repeat это самый красивый вариант
    for result in q:        
        print(result)           # !!! в result будет вывод в том же порядке как мы на устройства отправляли команды / перебирали devices

