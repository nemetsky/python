import netmiko
import getpass
from pprint import pprint

def send_show_command(ip, user, password, command):
    print(f"Подключаюсь к {ip}")
    try:
        with netmiko.ConnectHandler(device_type="cisco_ios", timeout=5, host=ip, username=user, password=password) as ssh:
            output = ssh.send_command(command)
            return output
    except netmiko.exceptions.NetmikoTimeoutException:
        print(f"Не получилось подключиться к {ip}")
    except netmiko.exceptions.NetmikoAuthenticationException as error:
        print(error)
    # except ValueError as error:       # это исключение если используем парольна enable и неправильно ввели его (можно объеденить с предыдущим исключением т.к. там используем тоже as error)
        # print(error)

if __name__ == "__main__":                                                             
    ip_list = ["10.11.10.107", "192.168.11.11"]
    password = getpass.getpass()
    for ip in ip_list:
        out = send_show_command(ip, "nemetskiy-sv", password, "sh clock")     
        pprint(out, width=120)

   