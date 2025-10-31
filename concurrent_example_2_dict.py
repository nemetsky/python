from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from pprint import pprint
import logging
import netmiko
import yaml
import getpass

logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s: %(message)s", level=logging.DEBUG)       # %(asctime)s  - текущее время

def send_show_command(device, password, command):                           # !!! функция которая подключается к одному устройству, но выполняется будет в потоках, !!!в этой функции лучше не писать выводы куда-то в общие ресурсы!!!
    ip = device["host"]                                             
    logging.info(f"===> Connection: {ip}")
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            output = ssh.send_command(command, read_timeout=20)             #  read_timeout=20 - увеличил для Eltex, так как команда например "sh run | i hostname" долго возвращает результат
            logging.info(f"<=== Received:   {ip}")
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")

def collect_data(devices, command, max_threads=2):                          # функция которая запускает подключение в потоках последовательно, сбор данных с устройств в словарь будет последовательно, по умолчанию количество потоков установили 2
    result_dict = {}
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(
            send_show_command, devices, repeat(password), repeat(command)
        )
        # !!! здесь уже потоки прекратили работу, теперь последовательно записываем наши полученные данные в словарь или в файл
        for dev, output in zip(devices, results):            # zip объеденяет 2 последовательности, они одинаковые (сколько устройств, столько и выводов)       
            result_dict[dev["host"]] = output                # в словаре ключ - это IP, значение - вывод команды
    return result_dict    

   
if __name__ == "__main__": 
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(collect_data(devices, "sh run | i hostname"))
