from ezsnmp import Session
from pprint import pprint

def get_list(iterable_object):    # функция получает вывод OID в виде объектов Python, возвращает список кортежей [(index, значение),...]
    list1 = []
    for item in iterable_object:
        list1.append((item.index, item.value))
    return list1

#ip = '10.11.10.210'    # Cisco
ip = '10.11.10.211'    # MES 2348ЗP
#ip = '10.20.11.32'     # ia-mdc-lan-accs-csw-a09-1
#ip = '172.16.50.173'   # ia-mdc-aux-uc-csw-1
#ip = '10.20.11.43'     # MES 2308P 
#ip = '10.11.10.15'     # ia-rdc-lan-aggr-csw-137-1
#ip = '10.20.11.4'      # MES 5448

session = Session(hostname=ip, community='CDUro', version=2)

output_pid_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
output_sn_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
index_sw_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.5')
index_sw_unit_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.6')
index_power_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.4')
output_sfp_pid_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.10')
output_sfp_sn_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.6')
output_ports_unit_object = session.walk('1.3.6.1.4.1.89.53.3.1.5')
output_ports_unit_stack_object = session.walk('1.3.6.1.4.1.89.53.23.1.4')  # требуется для стеков, информация по стековым портам (к какому юниту они принадлежат)

output_pid = get_list(output_pid_object)
output_sn = get_list(output_sn_object)
list_index_sw = get_list(index_sw_object)
list_index_sw_unit = get_list(index_sw_unit_object)
list_index_power = get_list(index_power_object)
output_sfp_pid = get_list(output_sfp_pid_object)
output_sfp_sn = get_list(output_sfp_sn_object)
output_ports_unit = get_list(output_ports_unit_object)
output_ports_unit_stack = get_list(output_ports_unit_stack_object)

out_dict = {}           # основной словарь {Номер юнита: Список списоков опций PID, SN}
parent_index_dict = {}  # вспомогательный словарь {Индекс коммутатора: номер юнита}. Для определения к какому юниту принадлежит БП

for index, unit, pid, sn in zip(list_index_sw, list_index_sw_unit, output_pid, output_sn):
    if index[1] == '3' and pid[1] != '':
        out_dict[unit[1]] = [[pid[1], sn[1]]]     # добавялем в итоговый словарь шасси
        parent_index_dict[index[0]] = unit[1]     # сразу формируем вспомогательный словарь

for index, pid, sn, parent in zip(list_index_sw, output_pid, output_sn, list_index_power):
    if index[1] == '6':
        parent_index = parent[1]
        unit = parent_index_dict[parent_index]
        out_dict[unit].append([pid[1], sn[1]])    # добавляем в итоговый словарь БП

ports_unit_dict = {}   # вспомогательный словарь {Индекс порта:  юнит}. Для определения какому к каому юниту принаджлежит индекс порта

total_ports_unit = output_ports_unit + output_ports_unit_stack

for i in total_ports_unit:        # формируем вспомогательный словарь
    if not i[1].isdigit():        # если это не стек, выдаст 'что нет такого OID' в ветке стековых портов, и в вспомогательный словарь не добавляем
        continue
    index = i[0].split('.')[-1]
    ports_unit_dict[index] = i[1]

result_sfp = list(zip(output_sfp_pid, output_sfp_sn))

if result_sfp[0][0][1] != None:
    for sfp_pid, sfp_sn in result_sfp:
        list1 = [sfp_pid[1], sfp_sn[1]]
        index = sfp_pid[0]
        number_stack = ports_unit_dict[index]
        out_dict[number_stack].append(list1)     # добавляем порты в итоговый словарь

pprint(out_dict)
