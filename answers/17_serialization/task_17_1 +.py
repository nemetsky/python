# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import csv
import re
import glob


def write_dhcp_snooping_to_csv(filenames, output):
    regex = r"(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)"
    with open(output, "w") as dest:
        writer = csv.writer(dest)
        writer.writerow(["switch", "mac", "ip", "vlan", "interface"])
        for filename in filenames:
            switch = re.search("([^/]+)_dhcp_snooping.txt", filename).group(1)      # странная регулярка у автора, но она как-то работает
            with open(filename) as f:
                for line in f:
                    match = re.search(regex, line)
                    if match:
                        writer.writerow((switch,) + match.groups())                 # автор делает из switch кортеж с одним элементом (switch,) и суммирует его с кортежем найденных групп


if __name__ == "__main__":
    sh_dhcp_snoop_files = glob.glob("*_dhcp_snooping.txt")
    print(sh_dhcp_snoop_files)
    write_dhcp_snooping_to_csv(sh_dhcp_snoop_files, "example_csv.csv")


# =================================================================================

### Мое решение ###    (В оличии от автора я сначала формирую искомый списос списков, а потом его записываю в csv-файл, автор сразу добавляет записи в файл когда находит их)
                       # (Ну а так все правильно я сделал сам)
import re
import csv
from glob import glob
from pprint import pprint

def gwrite_dhcp_snooping_to_csv(filenames, output):
    regex = re.compile(r"^([A-F0-9:]+) +([\d.]+).+ (\d+) +(\S+)", re.MULTILINE) # отлавливаем группы - '00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1'
    regex_device = re.compile(r"^(\S+?)_", re.MULTILINE)                        # регулярка для нахождения имени иструства из имени файла
    result = ["switch mac ip vlan interface".split()]                           # записываем в наш список искомый список заголовков сразу
    for file in filenames:                                                      # пербираем файлы
        device = regex_device.search(file)                                      # находим имя устройства
        with open(file) as f:                                                   
            match = regex.finditer(f.read())                                    # находим все совпадения в файле
            for m in match:                                                     # перебираем совпадения
                list1 = []                                                      # делаем пустой список каждый раз в цикле чтобы внего добавлять список значений 
                list1.append(device.group(1))                                   # добавляем имя устройства в список
                list1.extend(list(m.groups()))                                  # добавляем в список значения '00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1'
                result.append(list1)                                            # теперь весь найденный в наш результирующий список, где уже есть заголовки
    with open(output, "w", newline="") as f:                                    
        wr = csv.writer(f)                                                      # создаем файл csv и в него добавляем наш список списков
        for line in result:
            wr.writerow(line)
    return result

# file_list = ["sw1_dhcp_snooping.txt", "sw2_dhcp_snooping.txt", "sw3_dhcp_snooping.txt"]
file_list = glob("*_dhcp_snooping.txt")                                                     # с помощью glob в текущем каталоге находим все файлы по нашей маске
pprint(gwrite_dhcp_snooping_to_csv(file_list, "resutls_17_1.csv"))

"""
Результат:

[['switch', 'mac', 'ip', 'vlan', 'interface'],
 ['sw1', '00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1'],
 ['sw1', '00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10'],
 ['sw1', '00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9'],
 ['sw1', '00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3'],
 ['sw1', '00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7'],
 ['sw2', '00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7'],
 ['sw2', '00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5'],
 ['sw2', '00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9'],
 ['sw2', '00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2'],
 ['sw3', '00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20'],
 ['sw3', '00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21']]
 
В файле:
 
switch,mac,ip,vlan,interface
sw1,00:09:BB:3D:D6:58,10.1.10.2,10,FastEthernet0/1
sw1,00:04:A3:3E:5B:69,10.1.5.2,5,FastEthernet0/10
sw1,00:05:B3:7E:9B:60,10.1.5.4,5,FastEthernet0/9
sw1,00:07:BC:3F:A6:50,10.1.10.6,10,FastEthernet0/3
sw1,00:09:BC:3F:A6:50,192.168.100.100,1,FastEthernet0/7
sw2,00:A9:BB:3D:D6:58,10.1.10.20,10,FastEthernet0/7
sw2,00:B4:A3:3E:5B:69,10.1.5.20,5,FastEthernet0/5
sw2,00:C5:B3:7E:9B:60,10.1.5.40,5,FastEthernet0/9
sw2,00:A9:BC:3F:A6:50,10.1.10.60,20,FastEthernet0/2
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21
"""