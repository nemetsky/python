# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""
import re
import csv
import glob


def parse_sh_version(sh_ver_output):
    regex = (
        "Cisco IOS .*? Version (?P<ios>\S+), .*"
        "uptime is (?P<uptime>[\w, ]+)\n.*"
        'image file is "(?P<image>\S+)".*'
    )
    match = re.search(regex, sh_ver_output, re.DOTALL,)
    if match:
        return match.group("ios", "image", "uptime")


def write_inventory_to_csv(data_filenames, csv_filename):
    headers = ["hostname", "ios", "image", "uptime"]
    with open(csv_filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for filename in data_filenames:
            hostname = re.search("sh_version_(\S+).txt", filename).group(1)
            with open(filename) as f:
                parsed_data = parse_sh_version(f.read())
                if parsed_data:
                    writer.writerow([hostname] + list(parsed_data))         # Автор использует списки в данном случае для записи, у меня кортежи записываются


if __name__ == "__main__":
    sh_version_files = glob.glob("sh_vers*")
    write_inventory_to_csv(sh_version_files, "routers_inventory.csv")


#======================================================================================

### Мое решение ###  (в принципе такое же)

import re
import csv
from glob import glob

def parse_sh_version(output):
    regex = re.compile(r"Cisco IOS .+? Version (?P<ios>\S+), "              
                       r".*uptime is (?P<uptime>[\S ]+)"
                       r".*file is \"(?P<image>\S+)\"", re.DOTALL)        # обязательно DOTALL, т.к. ищем не построчно, а во всем выводе
    match = regex.finditer(output)                                        # у автора через re.search, впринципе логично, т.к. совпадение только одно
    for m in match:
        result = m.group("ios", "image", "uptime")                        # кортеж с содержимым, можно через индексы (1, 3, 2)             
    return result

def write_inventory_to_csv(data_filenames, csv_filename):                 
    headers = ["hostname", "ios", "image", "uptime"]                      
    with open(csv_filename, "w", newline="") as f_csv:                    # открываем csv-файл для записи
        wr = csv.writer(f_csv)
        wr.writerow(headers)                                              # записываем заголовки
        for file in data_filenames:                                       # перебираем файлы
            hostname = re.search(r"sh_version_(\S+).txt", file).group(1)  # из имени файла находлим имя хоста
            with open(file) as f_data:
                output = f_data.read()                                    # считываем содержимое файла
                result_tuple = (hostname,) + parse_sh_version(output)     # делаем кортеж с одним элементом (hostname,) и суммирует его с кортежем c найденными группамми с помощью нашей функции parse_sh_version. Автор списки использует 
                wr.writerow(result_tuple)                                 # записываем в наш csv-файл найденный кортеж

if __name__ == "__main__":
    files = glob("sh_vers*")
    write_inventory_to_csv(files, "resutls_17_2.csv")


"""
Результат содержимого файла.csv:

hostname,ios,image,uptime
r1,12.4(15)T1,flash:c1841-advipservicesk9-mz.124-15.T1.bin,"15 days, 8 hours, 32 minutes"
r2,12.4(4)T,disk0:c7200-js-mz.124-4.T,"45 days, 8 hours, 22 minutes"
r3,12.4(4)T,disk0:c7200-js-mz.124-4.T,"5 days, 18 hours, 2 minutes"
"""
