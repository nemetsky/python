# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
from sys import argv

ignore = ["duplex", "alias", "configuration"]

filename = argv[1]

with open(filename) as f:
    for line in f:
        words = line.split()
        words_intersect = set(words) & set(ignore)
        if not line.startswith("!") and not words_intersect:
            print(line.rstrip())

# ===========================================================

### Мое решение ###

# у меня другое совсем решение, но преобразование строки в множество и сравнение с множеством слов-исключений - очень интересное решение

file1 = argv[1]

ignore = ["duplex", "alias", "configuration"]

#with open("config_sw1.txt", "r") as f:
with open(file1) as f:
    for line in f:
        flag = True                                 # ввел переменную флаг, перед проверкой строки присваеваем ему True
        for each_ignore in ignore:                  # цикл в котором перебираем слова-исключения
            if each_ignore in line:                 # если попадается слово-исключение в строке
                flag = False                        # флагу присваеваем другое значение False
                break                               # необязательно
        if flag and not line.startswith("!"):       # если флаг не менялся, значит слов-исключений в строке не было, также проверяем чтобы строка не начиналась на "!"
            print(line.rstrip())