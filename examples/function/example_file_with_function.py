# Задача выбрать из списка конфигов интерфейсы с их IP-адресами 

# Решение задачи без функции

from pprint import pprint
'''
config_list = ["config_r1.txt", "config_r1.txt", "config_sw1.txt"]

for cfg in config_list:
    intf_ip_dict = {}
    with open(cfg) as f:
        for line in f:
            if line.startswith("interface"):
                intf = line.split()[-1]
            elif line.startswith(" ip address"):
                ip = line.split()[-2]
                intf_ip_dict[intf] = ip
    pprint(intf_ip_dict)
'''
###############################################

# Решение задачи с функцией в которую передается имя файла

def get_intf_ip_dict_from_cfg(filename):
    intf_ip_dict = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("interface"):
                intf = line.split()[-1]
            elif line.startswith(" ip address"):
                ip = line.split()[-2]
                intf_ip_dict[intf] = ip
    return intf_ip_dict

# r1 = get_intf_ip_dict_from_cfg("config_r1.txt")
# pprint(r1)

config_list = ["config_r1.txt", "config_r1.txt", "config_sw1.txt"]

for cfg in config_list:                                             # Перебор списка с именами файлов и применение функции к каждому
    result = get_intf_ip_dict_from_cfg(cfg)
    pprint(result)