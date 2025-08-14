# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv

ignore = ["duplex", "alias", "configuration"]

src_file, dst_file = argv[1], argv[2]

with open(src_file) as src, open(dst_file, 'w') as dst:
    for line in src:
        words = line.split()
        words_intersect = set(words) & set(ignore)
        if not line.startswith("!") and not words_intersect:
            dst.write(line)


# ==================================================

### Мое решение ###

# в части вывода результата в файл мое решение не отличается 

from sys import argv

file1 = argv[1]
file2 = argv[2]

ignore = ["duplex", "alias", "configuration"]

with open(file1) as f1, open(file2, "w") as f2:
    for line in f1:
        flag = True
        for each_ignore in ignore:
            if each_ignore in line:
                flag = False
                break
        if flag and not line.startswith("!"):
            f2.write(line)

# запуск скрипта 
# test.py config_sw1.txt config_sw1_new.txt
