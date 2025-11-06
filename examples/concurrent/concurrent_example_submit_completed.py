from concurrent.futures import ThreadPoolExecutor, as_completed
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
            output = ssh.send_command(command, read_timeout=20)       
            logging.info(f"<=== Received:   {ip}")
            return ip, output                                # Здесь лучше тогда вернуть кортедж из адреса и вывода (host, result), 
                                                             # так как мы с as_completed уже не можем применить zip, т.к. порядок возвращения результатов произвольный   
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"IP-адрес {ip} недоступен")


def collect_data(devices, command, max_threads=2):                        
    result_dict = {}
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:          
        future_list = [executor.submit(send_show_command, dev, password, command)  # применили генератор списков, в предыдущем примере есть пояснения к submit
                      for dev in devices]  
        for future in as_completed(future_list):                    # в данном случае результаты будут уже не по порядку возвращены, а в произвольном порядке    
            print(future.result())                                  # как только future отрабатывает так возвращается его результат
            
            ip, output = future.result()                # можно теперь распоковать (т.к. в send_show_command возвращаем кортедж) и записать в словарь результат
            result_dict[ip] = output
            
    return result_dict 

   
if __name__ == "__main__": 
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    pprint(collect_data(devices, "sh run | i hostname"))

""" Результат
concurrent_example_submit_completed.py
Password:
2025-11-03 15:17:41,384 ThreadPoolExecutor-0_0 INFO: ===> Connection: 172.16.0.1
2025-11-03 15:17:41,385 ThreadPoolExecutor-0_1 INFO: ===> Connection: 172.16.0.2
2025-11-03 15:17:44,870 ThreadPoolExecutor-0_1 INFO: <=== Received:   172.16.0.2    
('172.16.0.2', 'hostname c3845-inet-2')                                             # видим что не по порядку вернулись результаты
2025-11-03 15:17:45,217 ThreadPoolExecutor-0_0 INFO: <=== Received:   172.16.0.1
('172.16.0.1', 'hostname c3845-inet-1')

{'172.16.0.1': 'hostname c3845-inet-1', '172.16.0.2': 'hostname c3845-inet-2'}

"""