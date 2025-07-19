# вывод настроек порта

access_template = [
    'switchport mode access',
    'switchport access vlan {}',
    'switchport nonegotiate',
    'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

vlan = 5

##  первый вариант вывода в виде красивого списка

# from pprint import pprint
# access_template[1] = access_template[1].format(vlan)
# pprint(access_template)

## второй вариант вывода в виде готового списка команд для пользователя
## собрали список в одну строку с разделителем \n, который в выводе print не отображается, а потом при печати подставили vlan

access_str = '\n'.join(access_template)
print(access_str.format(vlan))

# такой вывод тоже будет иногда полезен для себя, он покажет как выглядет на самом деле строка 
# pprint(access_str)



