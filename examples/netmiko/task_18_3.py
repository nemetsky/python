import yaml
import getpass
from task_18_2a import send_show_command
from task_18_2b import send_config_commands


def send_commands(device, password, *, show=None, config=None):
    if show and config:
        raise ValueError("Можно передавать только один из аргументов show/config")
    elif show:
        return send_show_command(device, password, show)                            # если передана команда show то вызываем функцию send_show_command
    elif config:
        return send_config_commands(device, password, config)                       # если передана команда config то вызываем функцию config_show_command

if __name__ == "__main__":
    password = getpass.getpass()
    command = "show inventory"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        if dev["device_type"] == "cisco_ios":
            commands = ["logging console warning", "login on-failure log every 2"]
            print(send_commands(dev, password, config=commands))                    # передаем команду config
        elif dev["device_type"] == "eltex":
            commands = ["logging file informational", "logging cli-commands"]   
            print(send_commands(dev, password, show=command))                       # передаем команду show
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
