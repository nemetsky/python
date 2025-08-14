# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

output = "\n{:25} {}" * 5

with open("ospf.txt", "r") as f:
    for line in f:
        route = line.replace(",", " ").replace("[", "").replace("]", "")
        route = route.split()

        print(output.format(
                "Prefix", route[1],
                "AD/Metric", route[2],
                "Next-Hop", route[4],
                "Last update", route[5],
                "Outbound Interface", route[6],
        ))

# ======================================================================

### Мое решение ###   

# сделал иначе, сначала считал файл, разбил на строки, и каждую строку перебирал в цикле

with open("ospf.txt", "r") as f:
    output = f.read()
    
routes = output.split("\n")
                                                              # сделал другой шаблон
template = """                                               
Prefix                {}
AD/Metric             {}
Next-Hop              {}
Last update           {}
Outbound Interface    {}"""

for line in routes:
    if line:                                                  # проверяю нет ли пустой строки, так как в файле была последняя строка пустая и выдавалась ошибка
        line = line.replace(",", "")                          # убрал запятые в строке
        route = line.split()                                  # сделал список из строки
        route.remove("via")                                   # удалил в списке значение "via"
        route[2] = route[2].strip("[]")                       # удалил скобки в AD
        route.pop(0)                                          # удалил первый элемент "Тип маршрута"
        prefix, ad, ndate, last, intf  = route                # распоковал переменные
        print(template.format(prefix, ad, ndate, last, intf)) # вывел на печать в шаблон

