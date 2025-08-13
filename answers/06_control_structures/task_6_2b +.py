# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

while True:
    ip_address = input("Введите адрес: ")
    octets = ip_address.split(".")
    correct_ip = True

    if len(octets) == 4:
        for octet in octets:
            if not (octet.isdigit() and int(octet) in range(256)):
                correct_ip = False
                break
    else:
        correct_ip = False
    if correct_ip:
        break
    print("Неправильный IP-адрес")

first_octet = int(octets[0])

if 1 <= first_octet <= 223:
    print("unicast")
elif 224 <= first_octet <= 239:
    print("multicast")
elif ip_address == "0.0.0.0":
    print("unassigned")
elif ip_address == "255.255.255.255":
    print("local broadcast")
else:
    print("unused")

# еще один вариант
#
# while True:
#     ip = input("Введите IP-адрес в формате x.x.x.x: ")
#     octets = ip.split(".")
#     valid_ip = len(octets) == 4
#
#     for i in octets:
#         valid_ip = i.isdigit() and 0 <= int(i) <= 255 and valid_ip
#
#     if valid_ip:
#         break
#     print("Неправильный IP-адрес")
#
# if 1 <= int(octets[0]) <= 223:
#     print("unicast")
# elif 224 <= int(octets[0]) <= 239:
#     print("multicast")
# elif ip == "255.255.255.255":
#     print("local broadcast")
# elif ip == "0.0.0.0":
#     print("unassigned")
# else:
#     print("unused")


=============================================================

### МОЕ РЕШЕНИЕ (другой вариант совсем) ###

ip = input("Введите IP-адрес в формате X.X.X.X: ")

correct_ip = False                                                  # флаг - False

while not correct_ip:                                               # пока флаг False делаем цикл
    list1 = ip.split(".")
    for octet in list1:                                             # проверяем на правильность октеты (нет букв и диапазон от 0 до 256)
        if not octet.isdigit() or int(octet) not in range(256):
            correct_ip = True                                       # если хоть один неправельный октет то флагу присваеваем True 
            break
    if correct_ip or len(list1) != 4:                               # если флаг True то присваеваем ему False, вводим еще раз IP и в начало цикла возвращаемся
        ip = input("Неправильный IP-адрес, введите еще раз: ")      # или если октетов не 4 (можно это условие отдельно ниже сделать elif, тогда в нем False флагу необязательно прсваивать, он и так False)
        correct_ip = False
        continue
    else:                                                           # иначе адрес правильный, берем и вычисляем к какому типу относится
        if int(list1[0]) in range(1,224):
            print("unicast")
        elif int(list1[0]) in range(224,240):
            print("multicast")
        elif ip == "255.255.255.255":
            print("local broadcast")
        elif ip == "0.0.0.0":
            print("unassigned")
        else:
            print("unused")
    correct_ip = True                                               # присваеваем флагу True, чтобы выйти из цикла, или просто break в конце можно сделать
  