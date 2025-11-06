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
            promt = ssh.find_prompt()
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
                    # return False                                          # если не хотим выводить никакое сообщение, а просто сделать исключение  
            """

if __name__ == "__main__": 
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    send_show_command_to_devices(devices, "sh ip int bri", "results.txt") 

