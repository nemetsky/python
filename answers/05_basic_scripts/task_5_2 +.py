# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

network = input("Введите адрес сети: ")

ip, mask = network.split("/")
ip_list = ip.split(".")
mask = int(mask)

oct1, oct2, oct3, oct4 = [
    int(ip_list[0]),
    int(ip_list[1]),
    int(ip_list[2]),
    int(ip_list[3]),
]

bin_mask = "1" * mask + "0" * (32 - mask)
m1, m2, m3, m4 = [
    int(bin_mask[0:8], 2),
    int(bin_mask[8:16], 2),
    int(bin_mask[16:24], 2),
    int(bin_mask[24:32], 2),
]

ip_output = """
Network:
{0:<8}  {1:<8}  {2:<8}  {3:<8}
{0:08b}  {1:08b}  {2:08b}  {3:08b}"""

mask_output = """
Mask:
/{0}
{1:<8}  {2:<8}  {3:<8}  {4:<8}
{1:08b}  {2:08b}  {3:08b}  {4:08b}
"""

print(ip_output.format(oct1, oct2, oct3, oct4))
print(mask_output.format(mask, m1, m2, m3, m4))



=============================================================================

=== Мое решение ===
(в моем решение используется поиск "/" и срез (чуть сложнее получается), в остальном принцип такой же, только вывод маски по другому сделан)

network = input("Введите IP-сеть в формате X.X.X.X/X: ")
index = network.find("/")
address = network[:index]
mask = network[index+1:]
list_oct = address.split(".")
mask_bin = "1" * int(mask) + "0" * (32-int(mask))
list_mask = [mask_bin[0:8], mask_bin[8:16], mask_bin[16:24], mask_bin[24:32]]

template_output_net = """
Network:
{0:<10}{1:<10}{2:<10}{3:<10}
{0:08b}  {1:08b}  {2:08b}  {3:08b}

Mask:
/{4:}
{5:<10}{6:<10}{7:<10}{8:<10}
{9:<10}{10:<10}{11:<10}{12:<10}
"""

print(template_output_net.format(int(list_oct[0]), int(list_oct[1]), int(list_oct[2]), int(list_oct[3]), 
    int(mask), list_mask[0], list_mask[1], list_mask[2], list_mask[3], int(list_mask[0], 2), int(list_mask[1], 2), int(list_mask[2], 2), int(list_mask[3], 2)))










