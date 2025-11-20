import sys
import netmiko
import ipaddress
import getpass
import re
from tabulate import tabulate
from pprint import pprint

def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def parse_cisco_rt_show_ver(output):
    # ^Cisco (\D+) Software.*?Version (\S+),.*\n(\S+) uptime is (.+?)\n.+ (\S+) \(\S+\) processor.*Processor board ID (\S+)
    regex = (
        r"(?P<os>\D+) Software.*?Version (?P<version>\S+),"
        r".*\n(?P<hostname>\S+)"
        r" uptime is (?P<uptime>.+?)\n"
        r".+ (?P<model>\S+) \(\S+\) processor.*Processor board ID (?P<serial>\S+)"
        )
    result = []
    match = re.search(regex, output, re.DOTALL)
    result.append(match.groupdict())
    result_sort = []
    for obj in result:
        result_sort.append({'Hostname': obj['hostname'], 'OS': obj['os'], 'Version': obj['version'], 'Model': obj['model'], 'Serial': obj['serial'], 'Uptime (d,h:m:s)': obj['uptime']})
    print(tabulate(result_sort, headers="keys", tablefmt="orgtbl"))

def parse_eltex_rt_show_sys(output):
    # \: +(?P<os>\D+) (?P<model>\S+) .+?: +(?P<hostname>\S+).+?: +(?P<version>\S+.*?)\[.+uptime.+\): +(?P<uptime>.+?)\n.+number\: +(?P<serial>\S+)
    regex = (
        r"\: +(?P<os>\D+) (?P<model>\S+) .+?:"
        r" +(?P<hostname>\S+).+?:"
        r" +(?P<version>\S+.*?)"
        r"\[.+uptime.+\): +(?P<uptime>.+?)\n"
        r".+number\: +(?P<serial>\S+)"
        )
    result = []
    match = re.search(regex, output, re.DOTALL)
    result.append(match.groupdict())
    result_sort = []
    for obj in result:
        result_sort.append({'Hostname': obj['hostname'], 'OS': obj['os'], 'Version': obj['version'], 'Model': obj['model'], 'Serial': obj['serial'], 'Uptime (d,h:m:s)': obj['uptime']})
    print(tabulate(result_sort, headers="keys", tablefmt="orgtbl"))

def parse_cisco_sw_show_ver(output):
    regex_count_sw = r"(\*)* +(\d) \d+ +"
    regex_master = (
        r"(?P<os>\D+) Software.*?Version (?P<version>\S+),"
        r".*\n(?P<hostname>\S+)"
        r" uptime is (?P<uptime>.+?)\n"
        r".+ (?P<model>\S+) \(\S+\) processor.*Processor board ID (?P<serial>\S+)"
        )
    # Switch (?P<stack>\d+)\n.+?Uptime +: (?P<uptime>.+?) \n.+?Model number +: (?P<model>\S+?)\n.+?System serial number +: (?P<serial>\S+)
    regex_member = (
        r"Switch (?P<stack>\d+)\n.+?"
        r"Uptime +: (?P<uptime>.+?) \n.+?"
        r"Model number +: (?P<model>\S+?)\n.+?"
        r"System serial number +: (?P<serial>\S+)"
        )
    result = []
    result_sort = []
    match_master = re.search(regex_master, output, re.DOTALL)
    dict_all = match_master.groupdict()
    match_count_sw = re.findall(regex_count_sw, output)
    if len(match_count_sw) == 1:
        result.append(dict_all)
        for obj in result:
            result_sort.append({'Hostname': obj['hostname'], 'OS': obj['os'], 'Version': obj['version'], 'Model': obj['model'], 'Serial': obj['serial'], 'Uptime': obj['uptime']})
    elif len(match_count_sw) > 1:
        for master, number in match_count_sw:
            if master == "*":
                dict_all["stack"] = "0" + number + " (master)"
                result.append(dict_all)
        match_member = re.finditer(regex_member, output, re.DOTALL)
        for m in match_member:
            dict_member = m.groupdict()
            dict_member["hostname"] = ""
            dict_member["version"] = ""
            dict_member["os"] = ""
            result.append(dict_member)
        for obj in result:
            result_sort.append({'Hostname': obj['hostname'], 'OS': obj['os'], 'Version': obj['version'], 'Stack': obj['stack'], 'Model': obj['model'], 'Serial': obj['serial'], 'Uptime': obj['uptime']})
    print(tabulate(result_sort, headers="keys", tablefmt="orgtbl"))
 
 
def parse_eltex_sw_show_stack(output):
    regex_stack = r" +(?P<unit>\d) +\S+ +(?P<state>\w+)"
    match_member = re.finditer(regex_stack, output)
    results = [match.groups() for match in match_member]
    return results

def parse_eltex_sw_show_ver(output):
    regex_ver = r"Active-image.*\n +Version: (?P<version>\S+)"
    results = re.search(regex_ver, output).group(1)
    return results

def parse_eltex_sw_show_system_id(output):
    regex_serial = r" +(?P<unit>\d) +\S+ +\S+ +(?P<serial>\S+)"
    match_serial = re.finditer(regex_serial, output)
    results = [match.groups() for match in match_serial]
    return results

def parse_eltex_sw_show_system(output):
    regex_sys_master = r"Description: +(?P<model>\S+) .*sec\): +(?P<uptime>\S+).*Name: +(?P<hostname>\S+)"
    results = re.search(regex_sys_master, output, re.DOTALL).groups(1)
    return results

def parse_eltex_sw_show_system_unit(output):
    regex_sys_backup = r"Description: +(?P<model>\S+) .*sec\): +(?P<uptime>\S+)" 
    results = re.search(regex_sys_backup, output, re.DOTALL).groups(1)
    return results
    
def main_parse_eltex_sw(eltex_sw_ver, eltex_sw_serial, eltex_sw_system, eltex_stack_sw):
    result = []
    dict_sw = {}
    eltex_count_sw = len(eltex_stack_sw)
    if eltex_count_sw == 1:
        dict_sw["Hostname"] = eltex_sw_system[2]
        dict_sw["OS"] = "Eltex"
        dict_sw["Version"] = eltex_sw_ver
        dict_sw["Model"] = eltex_sw_system[0]
        dict_sw["Serial"] = eltex_sw_serial[0][1]
        dict_sw["Uptime (d,h:m:s)"] = eltex_sw_system[1]
        result.append(dict_sw)
    elif eltex_count_sw > 1:
        for number, state in eltex_stack_sw:
            dict_serial = dict(eltex_sw_serial)             # из кортежа делаем словарь
            if state == 'master':
                dict_sw = {}
                dict_sw["Hostname"] = eltex_sw_system[2]
                dict_sw["OS"] = "Eltex"
                dict_sw["Version"] = eltex_sw_ver
                dict_sw["Stack"] = f"{number} ({state})"
                dict_sw["Model"] = eltex_sw_system[0]
                dict_sw["Serial"] = dict_serial[number]
                dict_sw["Uptime (d,h:m:s)"] = eltex_sw_system[1]
                result.append(dict_sw)
            elif state == 'backup':
                with open(f"show_system_unit_eltex_sw.txt") as f:
                    output = f.read()
                    eltex_sw_system_unit = parse_eltex_sw_show_system_unit(output)
                dict_sw = {}
                dict_sw["Hostname"] = ""
                dict_sw["OS"] = ""
                dict_sw["Version"] = ""
                dict_sw["Stack"] = f"{number} ({state})"
                dict_sw["Model"] = eltex_sw_system_unit[0]
                dict_sw["Serial"] = dict_serial[number]
                dict_sw["Uptime (d,h:m:s)"] = eltex_sw_system_unit[1]
                result.append(dict_sw)
    return result
    
# model = input("Введите производителя оборудования (1. Cisco или 2. Eltex): ")
# if model.lower() == "cisco" or model == "1":
#     device_type = "cisco_ios"
# elif model.lower() == "eltex" or model == "2":
#     device_type = "eltex"
# else:
#     print("Введен неподдерживаемый производитель")
#     sys.exit(0)
# ip = input("Введите IP-адрес или имя устройства: ")
# ip_verify = check_ip(ip)
# if not ip_verify:
#    print("Введен некорректный IP-адрес")
#    sys.exit(0)
# print(f"Подключение к {ip}...")
# user = input("Введите имя пользователя: ")
# password = getpass.getpass(prompt="Введите пароль: ")
try:
    # with netmiko.ConnectHandler(device_type=device_type, timeout=5, host=ip, username=user, password=password) as ssh:
    with netmiko.ConnectHandler(device_type="cisco_ios", timeout=5, host="172.16.0.1", username="cisco", password="cisco") as ssh:
        output = ssh.send_command("show version")
        if "inet" in ssh.find_prompt():
            parse_cisco_rt_show_ver(output)
except netmiko.exceptions.NetmikoAuthenticationException:
    print("Ошибка аутентификации")
except netmiko.exceptions.NetmikoTimeoutException:
    print(f"IP-адрес {ip} недоступен")
print("\n")

with open("show_system_eltex_rt.txt") as f:
    output = f.read()
    parse_eltex_rt_show_sys(output)
print("\n")

with open("show_ver_sw_cisco.txt") as f:
    output = f.read()
    parse_cisco_sw_show_ver(output)
print("\n") 

   
#########################################3

with open("show_ver_eltex_sw.txt") as f:
    output = f.read()
    eltex_sw_ver = parse_eltex_sw_show_ver(output)
    
with open("show_system_id_eltex_sw.txt") as f:
    output = f.read()
    eltex_sw_serial = parse_eltex_sw_show_system_id(output)
    
with open("show_system_eltex_sw.txt") as f:
    output = f.read()
    eltex_sw_system = parse_eltex_sw_show_system(output)

with open("show_stack_eltex_sw.txt") as f:
    output = f.read()
    eltex_stack_sw = parse_eltex_sw_show_stack(output)

result = main_parse_eltex_sw(eltex_sw_ver, eltex_sw_serial, eltex_sw_system, eltex_stack_sw)    
print(tabulate(result, headers="keys", tablefmt="orgtbl"))   
            
