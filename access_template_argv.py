import sys
# или так 
# from sys import argv

print(sys.argv)                             # напечатать аргументы которые передаем, [0] - это вывод имени скрипта

access_template = [
    ' switchport mode access',
    ' switchport access vlan {}',
    ' switchport nonegotiate',
    ' spanning-tree portfast',
    ' spanning-tree bpduguard enable'
]

vlan = sys.argv[1]                          #  vlan присваеваем наш аргумент
# или так 
# vlan = argv[1]

intf = sys.argv[2]

print(f'interface {intf}')

access_str = '\n'.join(access_template)
print(access_str.format(vlan))


# python access_template_argv.py 5 Gi0/0          - запуск скрипта с аргументами
