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
            output = ssh.send_command(command, read_timeout=60)
            logging.info(f"<=== Received:   {ip}")
            return output
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"Устройство {ip} недоступно")


def collect_configs(devices, command, output_file, max_threads=4):             
    password = getpass.getpass()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(
            send_show_command, devices, repeat(password), repeat(command)
        )
    for dev, output in zip(devices, results): 
        with open(output_file.format(dev["host"]), "w") as f:
            f.write(output)                                     
            
if __name__ == "__main__":
    command = "show run"
    with open("devices_work.yaml") as f:
        devices = yaml.safe_load(f)
    collect_configs(devices, command, "{}_config.txt")
 