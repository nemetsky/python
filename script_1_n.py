import sys
import netmiko
import ipaddress
import getpass
import re
from tabulate import tabulate


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def parse_cisco_rt_show_ver(output):
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
                eltex_sw_system_unit = parse_eltex_sw_show_system_unit(ssh.send_command(f"show system unit {number}"))
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
    
ip = input("Введите IP-адрес или имя устройства: ")
if ip[0].isdigit():
    ip_verify = check_ip(ip)
if not ip_verify:
    print("Введен некорректный IP-адрес")
    sys.exit(0)
user = input("Введите имя пользователя: ")
password = getpass.getpass(prompt="Введите пароль: ")
try:
    print(f"Подключение к {ip}...\n")
    with netmiko.ConnectHandler(device_type="eltex", timeout=5, host=ip, username=user, password=password) as ssh:
        output = ssh.send_command("show system")
        match = re.search(r"% (.+)", output)
        if "inet" in ssh.find_prompt() and match:
            output = ssh.send_command("show version")
            result = parse_cisco_rt_show_ver(output)
        elif "inet" in ssh.find_prompt():
            result = parse_eltex_rt_show_sys(output)
        elif match:
            output = ssh.send_command("show version")
            result = parse_cisco_sw_show_ver(output)
        else:
            eltex_sw_ver = parse_eltex_sw_show_ver(ssh.send_command("show version"))
            eltex_sw_serial = parse_eltex_sw_show_system_id(ssh.send_command("show system id"))
            eltex_sw_system = output
            eltex_stack_sw = parse_eltex_sw_show_stack(ssh.send_command("show stack"))    
            result = main_parse_eltex_sw(eltex_sw_ver, eltex_sw_serial, eltex_sw_system, eltex_stack_sw)    
except netmiko.exceptions.NetmikoAuthenticationException:
    print("Ошибка аутентификации")
except netmiko.exceptions.NetmikoTimeoutException:
    print(f"IP-адрес {ip} недоступен")
print(tabulate(result, headers="keys", tablefmt="orgtbl"))    
