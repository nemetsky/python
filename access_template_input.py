access_template = [
    ' switchport mode access',
    ' switchport access vlan {}',
    ' switchport nonegotiate',
    ' spanning-tree portfast',
    ' spanning-tree bpduguard enable'
]

vlan = input("Введи номер Vlan: ")
intf = input("Введи номер интерфейса: ")

print(f'interface {intf}')

access_str = '\n'.join(access_template)
print(access_str.format(vlan))

input("Нажмите Enter для продолжения")
