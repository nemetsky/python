
# Задача из вывода show interfaces получить словарь вида как показано ниже
# Нужные данные в данном случае находятся в разных строках конфига
'''{
    "Ethernet0/0": 1500,
    "Ethernet0/1": 1500
}
'''
from pprint import pprint

result = {}

with open("sh_ip_interface.txt", "r") as f:
    for line in f:
        line = line.rstrip()                        # чтобы в выводе не было лишних строк, удаляем правых \n
        if "line protocol" in line:                 # если в строке есть подстрока  "line protocol"
            intf = line.split()[0]                  # берем интерфей из строки (разбили строку на список и взяли первый элемент)
        elif "MTU" in line:
            mtu = line.split()[2]                   # берем mtu из строки (разбили строку на список и взяли третий элемент)
           #  print(intf, mtu)                        # переменные в цикле каждый раз перезаписываются, поэтому MTU всегда будет относится к своему интерфейсу
            result[intf] = mtu                      # записываем в словарь интерфейс и mtu, ВАЖНО записываем не когда встретили интерфейc, а когда встретили mtu
           
pprint(result)            

print("#" * 50)
# =======================================================
 
# Усложняем задачу, выводим вложенные словари в словаре в следующем виде
        
'''{
    "Ethernet0/0": {"mtu": 1500, "ip": "192.168.100.1/24"},
    "Ethernet0/1": {"mtu": 1500, "ip": "192.168.200.1/24"}
}
Словарь удобен тем, что мы можем обращаться в понятном виде к данным словаря в отличии от списка
Например:
result["Ethernet0/0"]
result["Ethernet0/0"]["ip"]     --->     "192.168.100.1/24"

В списке списков было бы непонятно
result[2][3]
''' 

from pprint import pprint        
        
result = {}        
        
with open("sh_ip_interface.txt", "r") as f:        
    for line in f:        
        line = line.rstrip()                        
        if "line protocol" in line:                 
            intf = line.split()[0]
            result[intf] = {}                # ВАЖНО, создаем вложенный пустой словарь в цикле, чтобы в него вносить данные по интерфейсам, ключом будет интерфейс
        elif "Internet address" in line:     # добавляем условие, чтобы определить строку в которой указан IP
            ip_add = line.split()[-1]        # вычисляем IP-адрес
            result[intf]["ip"] = ip_add      # добавляем в подсловарь ключ "ip" с значением IP-адресса
        elif "MTU" in line:        
            mtu = line.split()[2]                   
            result[intf]["mtu"] = mtu        # аналогично добавляем в подсловарь ключ "mtu" с значением MTU                 
                    
pprint(result)                    

print("#" * 50)

# =======================================================

# Усложняем задачу, если в выоде show interface нет данных по IP и MTU у интерфейса. Пустой подсловарь по интерфейсу (лишние строки) выводить не надо

'''
# Можно просто сделать выборку из словаря по интерфейсам на которых есть параметры

for intf, params in result.items():
    if params:
        print(intf)
        pprint(params)

# Можно пустой словарь создавать попозже в другом условии, например если есть параметр Ip-адрес  

with open("sh_ip_interface.txt", "r") as f:
    for line in f:        
        line = line.rstrip()               
        if "line protocol" in line:        
            intf = line.split()[0]
        elif "Internet address" in line:   
            ip_add = line.split()[-1] 
            result[intf] = {}                   # !!!!! Сюда перенесли
            result[intf]["ip"] = ip_add        
        elif "MTU" in line:                
            mtu = line.split()[2]                  
            result[intf]["mtu"] = mtu              