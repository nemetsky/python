import sys
import netmiko
import ipaddress
import getpass
import re
import yaml
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
import logging
import csv

logging.getLogger("netmiko").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s: %(message)s", level=logging.DEBUG)

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
        result_sort.append({'Hostname': obj['hostname'], 'OS': obj['os'], 'Version': obj['version'], 'Model': obj['model'], 'Serial': obj['serial'], 'Uptime': obj['uptime']})
    return result_sort


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
    return result_sort


def parse_cisco_sw_show_ver(output):
    regex_count_sw = r"(\*)* +(\d) \d+ +"
    regex_master = (
        r"(?P<os>\D+) Software.*?Version (?P<version>\S+),"
        r".*\n(?P<hostname>\S+)"
        r" uptime is (?P<uptime>.+?)\n"
        r".+ (?P<model>\S+) \(\S+\) processor.*Processor board ID (?P<serial>\S+)"
        )
    regex_member = (
        r"Switch \d(?P<stack>\d)\n.+?"
        r"ptime +: (?P<uptime>.+?) \n.+?"
        r"Model [Nn]umber +: (?P<model>\S+?)\n.*?"
        r"System [Ss]erial [Nn]umber +: (?P<serial>\S+)"
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
                dict_all["stack"] = number + " (master)"
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
    return result_sort
 
 
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
            dict_serial = dict(eltex_sw_serial) # из кортежа делаем словарь
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
    
def send_show_command(device, password, command, flag):
    ip = device["host"]                                             
    logging.info(f"===> Connection: {ip}")
    try:
        with netmiko.ConnectHandler(password=password, **device) as ssh:
            if flag == "rt_cisco":
                output = ssh.send_command(command)
                result = parse_cisco_rt_show_ver(output)
            elif flag == "rt_eltex":
                output = ssh.send_command(command, read_timeout=60)
                result = parse_eltex_rt_show_sys(output)    
            elif flag == "sw_cisco":
                output = ssh.send_command(command)
                result = parse_cisco_sw_show_ver(output)  
            elif flag == "sw_eltex":
                eltex_sw_ver = parse_eltex_sw_show_ver(ssh.send_command(command[0], read_timeout=60))
                eltex_sw_serial = parse_eltex_sw_show_system_id(ssh.send_command(command[1], read_timeout=60))
                eltex_sw_system =  parse_eltex_sw_show_system(ssh.send_command(command[2], read_timeout=60))
                eltex_stack_sw = parse_eltex_sw_show_stack(ssh.send_command(command[3], read_timeout=60))   
                result = main_parse_eltex_sw(eltex_sw_ver, eltex_sw_serial, eltex_sw_system, eltex_stack_sw)                
            logging.info(f"<=== Received:   {ip}")
            return result
    except netmiko.exceptions.NetmikoAuthenticationException: 
        logging.warning(f"Ошибка аутентификации к {ip}")
    except netmiko.exceptions.NetmikoTimeoutException:
        logging.warning(f"Устройство {ip} недоступно")

def collect_data(devices, max_threads=2):      
    result_list = []
    password = getpass.getpass(prompt="Введите пароль: ")
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_list = []
        for dev in devices:
            if dev["device_type"] == "cisco_ios" and "172.16" in dev["host"]:
                command = "show version"
                flag = "rt_cisco"
            elif dev["device_type"] == "eltex_esr":
                command = "show system"
                flag = "rt_eltex"
            elif dev["device_type"] == "cisco_ios":
                command = "show version"
                flag = "sw_cisco"
            elif dev["device_type"] == "eltex":
                command = ["show system", "show system id", "show system", "show stack"]
                flag = "sw_eltex"
            f = executor.submit(send_show_command, dev, password, command, flag)      
            future_list.append(f)                                          

        for f in future_list:
            result_list.append(f.result()[0])
    return result_list 

if __name__ == "__main__":
    with open("devices_home.yaml") as f:
        devices = yaml.safe_load(f)
    data = collect_data(devices)
    fieldnames=list(data[0].keys()) 
    with open("results.csv", "w", newline="") as f_csv:
        wr = csv.DictWriter(f_csv, fieldnames)
        wr.writeheader() 
        for line in data:             
            wr.writerow(line)
  