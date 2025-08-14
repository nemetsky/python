
# Разбивка конфишурации на секции и вывести на печать только интерфейсы с IP-адресами

from pprint import pprint

with open("config_r1.txt", "r") as f:
    output = f.read()

cfg_sections = output.split("!\n")               # делаем список строк, где каждая строка это секция (секция определяется между знаками !)

for section in cfg_sections:                     # перебираем секций
    if section.startswith("interface"):          # отбираем только секции с настройками интерфейсов
    # if section.startswith("interface") and "description" in section:   # с таким условием мы отберем только секции с интерфейсами, где есть description
        print("="*50)
        #pprint(section)
        section_lines = section.split("\n")      # делаем список строк каждой секции
        for line in section_lines:               # перебираем отдельно каждую строку секции
            if line.startswith("interface"):     # отбираем строки которые начинаются на interface
                intf = line.split()[-1]          # берем из строки только интерфейс
                print(intf)
            elif line.startswith(" ip address"): # отбираем строки у которых есть IP-адрес
                ip = line.split()[-2]            # берем из строки только адрес
                print(ip)

print("#"*50)
               
#=====================================================================

# Тоже самое только без секции, перебираем просто построчно файл

with open("config_r1.txt", "r") as f:
    for line in f:                   
        if line.startswith("interface"):   
            intf = line.split()[-1]        
            print(intf)
        elif line.startswith(" ip address"):
            ip = line.split()[-2]          
            print(ip)

print("#"*50)
              
#=====================================================================

# Тоже самое без секций только запишем в словарь и выведем словарь

result = {}

with open("config_r1.txt", "r") as f:
    for line in f:                   
        if line.startswith("interface"):   
            intf = line.split()[-1]
            result[intf] = None                     # Это если добавить в словарь интерфейсы без IP-адресов, иначе такие адреса не попадут
        elif line.startswith(" ip address"):        # Если адрес есть на интерфейсы то перезапишется None
            ip = line.split()[-2]          
            result[intf] = ip

pprint(result)            