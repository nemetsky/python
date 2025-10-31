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


# Сбор выводов в один файл

"""
def collect_data(devices, command, output_file, max_threads=2):             # функция которая запускает подключение в потоках последовательно, сбор данных с устройств в файл будет последовательно, по умолчанию количество потоков установили 2
    result_dict = {}
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(
            send_show_command, devices, repeat(password), repeat(command)
        )
        with open(output_file, "w") as f:
            for dev, output in zip(devices, results):                        
                f.write(dev["host"] + "\n")
                f.write(output + "\n")
"""


# Сбор выводов в разные файлы

def collect_data(devices, command, output_file, max_threads=2):             
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(
            send_show_command, devices, repeat(password), repeat(command)
        )
    for dev, output in zip(devices, results): 
        with open(output_file.format(dev["host"]), "w") as f:                  # имя файлов будет формата results_10.20.11.43.txt
            f.write(output)                                                    # в выводе будет show run
            # f.write(output.replace("hostname ", ""))                         # в файле просто имя устройства будет
            
if __name__ == "__main__": 
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    collect_data(devices, "sh run", "results_{}.txt")                          # "results_{}.txt" - имя файла типа как шаблон передаем
    # collect_data(devices, "sh run | i hostname", "results_{}.txt")
    

 
    
"""    
### Сбор выводов в разные файлы, но имя файла - это имя устройства ### (сам придумал)

def collect_data(devices, command1, command2, output_file, max_threads=2):             
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results_1 = executor.map(
            send_show_command, devices, repeat(password), repeat(command1)          # отправили "sh run | i hostname", чтобы вычислить имя устройства вставить его в название файла
        )
    with ThreadPoolExecutor(max_workers=max_threads) as executor:               
        results_2 = executor.map(
            send_show_command, devices, repeat(password), repeat(command2)          # отправили "sh run", чтобы записать вывод в файл соответствующий
        )    
    for hostname, output in zip(results_1, results_2):
        filename = hostname.replace("hostname ", "")
        with open(output_file.format(filename), "w") as f:    
            f.write(output)   
           
if __name__ == "__main__": 
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    collect_data(devices, "sh run | i hostname", "sh run", "{}.txt")  
"""
        
    
    
    
    
    
    
    
    
