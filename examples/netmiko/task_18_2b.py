import netmiko
import yaml
import getpass
import re
from pprint import pprint


def send_config_commands(device, password, config_commands, log=True):
    ip = device["host"]
    commands_good = {}
    commands_bad = {}
    template_error = 'Комманда "{}" выполнилась с ошибкой "{}" на устройстве {}'
    regex = r"% (.+)"
    if log:
        print(f"Подключаюсь к {ip}...")
    with netmiko.ConnectHandler(password=password, **device) as ssh:
        ssh.enable()
        for command in config_commands:
            result = ssh.send_config_set(command, exit_config_mode=False)
            match = re.search(regex, result)
            if match:
                print(template_error.format(command, match.group(1), ip))
                commands_bad[command] = result
                answer = input("Продолжать выполнять команды? [y]/n: ")
                if answer.lower() in ("n", "no"):
                    break
            else: 
                commands_good[command] = result
        ssh.exit_config_mode()
    return commands_good, commands_bad


if __name__ == "__main__":
    password = getpass.getpass()
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        if dev["device_type"] == "cisco_ios":
            commands_with_errors = ["i", "logginga console error"]
            correct_commands = ["login on-failure log every 2"]
            commands = commands_with_errors + correct_commands
        elif dev["device_type"] == "eltex":
            commands = ["logging file informational", "logging cli-commands"]
            # commands = ["line ssh", "history size 100"]
        #print(send_config_commands(dev, password, commands))
        good, bad = send_config_commands(dev, password, commands)
        print(good.keys())
        print(bad.keys())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
