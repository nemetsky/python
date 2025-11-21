import netmiko
import yaml
import getpass

def send_show_command(device, password, command):                 # отправка команд show
    ip = device["host"]                                             
    print(f"Подключаюсь к {ip}")
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            output = ssh.send_command(command)
            return output
    # except netmiko.exceptions.NetmikoAuthenticationException:   # исключение при ошибке аутентификации
    #     print("Ошибка аутентификации")
    # except netmiko.exceptions.NetmikoTimeoutException:          # исключение при таймауте подключения
    #     print(f"IP-адрес {ip} недоступен")
    except netmiko.exceptions.SSHException as error:              # вместо 2-х исключение можно указать одно общее, которое включает в себя оба исключения
        print(error)


def send_config_commands(device, password, config_commands, log=True):          # отправка команд конфигурации
    ip = device["host"]
    if log:
        print(f"Подключаюсь к {ip}...")
    with netmiko.ConnectHandler(password=password, **device) as ssh:
        result = ssh.send_config_set(config_commands)
    return result

 
if __name__ == "__main__":                                        # отправка команд show
    command = "show version"
    password = getpass.getpass()
    with open("devices_work.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        print(send_show_command(dev, password, command))

"""
if __name__ == "__main__":                                        # отправка команд конфигурации
    password = getpass.getpass()
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        if dev["device_type"] == "cisco_ios":
            # commands = ["logging console error", "login on-failure log every 2"]
            commands = ["archive", "log config", "logging size 200"]
        elif dev["device_type"] == "eltex":
            # commands = ["logging file informational", "logging cli-commands"]
            commands = ["line ssh", "history size 100"]
        print(send_config_commands(dev, password, commands))
"""        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
