import netmiko
import yaml
import getpass
from pprint import pprint

def send_show_command(device_params, password, command):    # пароль в функцию можно отдельно передать, чтобы не хранить в файле со словарями
    ip = device_params["host"]                              # можно так из словаря достать ip-адрес
    print(f"Подключаюсь к {ip}")
    try:
        with netmiko.ConnectHandler(password=password, **device_params) as ssh:
            output = ssh.send_command(command)
            return output
    except netmiko.exceptions.NetmikoTimeoutException:
        print(f"Не получилось подключиться к {ip}")
    except netmiko.exceptions.NetmikoAuthenticationException as error:
        print(error)

if __name__ == "__main__":                                                             
    with open("devices.yaml") as f:                         # в файле "devices.yaml" у нас содержится список словарей с параметрами подключения (тип, адрес, пользователь и т.д)
        devices = yaml.safe_load(f)                         # загружаем список словарей в переменную
        # print(devices)                     
    password = getpass.getpass()                            # пароль отдельно запрашиваем
    for dev in devices:                                     # перебираем словари с нашими устройствами
        out = send_show_command(dev, password, "sh clock")        
        pprint(out, width=120)

   