import netmiko
import getpass
from pprint import pprint

def send_show_command(ip, user, password, command):
    print(f"Подключаюсь к {ip}")
    with netmiko.ConnectHandler(device_type="cisco_ios", timeout=5, host=ip, username=user, password=password) as ssh:
        output = ssh.send_command(command)
        return output

if __name__ == "__main__":                                                             
    ip_list = ["10.11.10.107"]
    password = getpass.getpass()
    for ip in ip_list:
        out = send_show_command(ip, "nemetskiy-sv", password, "sh int descr")     
        pprint(out, width=120)

    
"""
device_params = {"device_type": "cisco_ios", 
                 "host": "10.11.10.107",
                 "username": "nemetskiy-sv",
                 "password": "SegNemVlad#3"}
"""                 