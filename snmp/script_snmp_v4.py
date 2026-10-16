from ezsnmp import Session
from pprint import pprint

# функция получает вывод OID в виде объектов Python, возвращает список кортежей [(index, значение),...]
def get_list(iterable_object):   
    list1 = []
    for item in iterable_object:
        list1.append((item.index, item.value))
    return list1


def main_cisco(session):
    result_dict = {}
    index_parent_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.4')
    type_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.5')
    number_unit_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.6')
    sn_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
    pid_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
    fru_tag_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.16')
    list_index_parent = get_list(index_parent_object)
    list_type_module = get_list(type_module_object)
    list_number_unit = get_list(number_unit_object)
    list_sn_module = get_list(sn_module_object)
    list_pid_module = get_list(pid_module_object)
    list_fru_tag = get_list(fru_tag_object)

    sw_index_unit_dict = {}  # вспомогательный словарь {Индекс коммутатора: номер юнита}

    for type, unit, pid, sn in zip(list_type_module, list_number_unit, list_pid_module, list_sn_module):
        if type[1] == '3' and pid[1] != '':
            number_unit = str(int(unit[1])) 
            result_dict[number_unit] = [[type_options[type[1]], pid[1].strip(), sn[1].strip()]]    # добавялем в итоговый словарь шасси
            sw_index_unit_dict[type[0]] = number_unit                             # сразу формируем вспомогательный словарь

    parent_dict = {}                           # вспомогательный словарь {Индекс компонента: Родительский индекс}
    for index, parent in list_index_parent:
        parent_dict[index] = parent

    for type, pid, sn, fru in zip(list_type_module, list_pid_module, list_sn_module,list_fru_tag):
        if (type[1] != '11' and type[1] != '3') and pid[1] != '' and fru[1] == '1':    # если копмонент не является стеком или шасси, и модуль заменяемый
            current_index = type[0]                                                    # делаем цикл в котором ищем самый родительский индекс модуля, чтобы привязать модуль к шасси 
            while True:
                parent_index = parent_dict[current_index]
                current_index = parent_index
                if parent_index in sw_index_unit_dict:          # если родительский индекс есть в нашем вспомогательном словаре юнитов, мы нашли родителя и выходим из цикла
                     unit = sw_index_unit_dict[current_index]
                     break
            result_dict[unit].append([type_options[type[1]], pid[1].strip(), sn[1].strip()])           # добавляем в итоговый словарь компонент (БП, модуль, трансивер и т.п.)
    return result_dict


def main_sw_eltex(session):
    result_dict = {}  # основной словарь {Номер юнита: Список списоков опций PID, SN}
    index_parent_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.4')
    type_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.5')
    number_unit_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.6')
    sn_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
    pid_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
    sfp_pid_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.10')
    sfp_sn_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.6')
    ports_unit_object = session.walk('1.3.6.1.4.1.89.53.3.1.5')
    ports_unit_stack_object = session.walk('1.3.6.1.4.1.89.53.23.1.4')  # требуется для стеков, информация по стековым портам (к какому юниту они принадлежат)
    list_index_parent = get_list(index_parent_object)
    list_type_module = get_list(type_module_object)
    list_number_unit = get_list(number_unit_object)
    list_sn_module = get_list(sn_module_object)
    list_pid_module = get_list(pid_module_object)
    list_sfp_pid = get_list(sfp_pid_object)
    list_sfp_sn = get_list(sfp_sn_object)
    list_ports_unit = get_list(ports_unit_object)
    list_ports_unit_stack = get_list(ports_unit_stack_object)

    parent_dict = {}  # вспомогательный словарь {Индекс коммутатора: номер юнита}. Для определения к какому юниту принадлежит БП

    for type, unit, pid, sn in zip(list_type_module, list_number_unit, list_pid_module, list_sn_module):
        if type[1] == '3' and pid[1] != '':
            result_dict[unit[1]] = [[type_options[type[1]], pid[1].strip(), sn[1].strip()]]     # добавялем в итоговый словарь шасси
            parent_dict[type[0]] = unit[1]                                      # сразу формируем вспомогательный словарь

    for type, pid, sn, parent in zip(list_type_module, list_pid_module, list_sn_module, list_index_parent):
        if type[1] == '6':
            parent_index = parent[1]
            unit = parent_dict[parent_index]
            result_dict[unit].append([type_options[type[1]], pid[1].strip(), sn[1].strip()])    # добавляем в итоговый словарь БП

    ports_unit_dict = {}   # вспомогательный словарь {Индекс порта:  юнит}. Для определения какому к каrому юниту принаджлежит индекс порта
    total_ports_unit = list_ports_unit + list_ports_unit_stack

    for i in total_ports_unit:        # формируем вспомогательный словарь
        if not i[1].isdigit():        # если это не стек, выдаст 'что нет такого OID' в ветке стековых портов, и в вспомогательный словарь не добавляем
            continue
        index = i[0].split('.')[-1]
        ports_unit_dict[index] = i[1]

    result_sfp = list(zip(list_sfp_pid, list_sfp_sn))

    if result_sfp[0][0][1] != None:
        for sfp_pid, sfp_sn in result_sfp:
            list1 = [type_options['9'], sfp_pid[1].strip(), sfp_sn[1].strip()]
            index = sfp_pid[0]
            number_stack = ports_unit_dict[index]
            result_dict[number_stack].append(list1)     # добавляем порты в итоговый словарь
    return result_dict


def main_rt_eltex(session):
    result_dict = {}  # основной словарь {Номер юнита: Список списоков опций PID, SN}
    index_parent_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.4')
    type_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.5')
    number_unit_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.6')
    sn_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
    pid_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
    sfp_pid_object = session.walk('1.3.6.1.4.1.35265.38.90.1.1.3')
    sfp_sn_object = session.walk('1.3.6.1.4.1.35265.38.90.1.1.4')

    list_index_parent = get_list(index_parent_object)
    list_type_module = get_list(type_module_object)
    list_number_unit = get_list(number_unit_object)
    list_sn_module = get_list(sn_module_object)
    list_pid_module = get_list(pid_module_object)
    list_sfp_pid = get_list(sfp_pid_object)
    list_sfp_sn = get_list(sfp_sn_object)

    parent_dict = {}  # вспомогательный словарь {Индекс коммутатора: номер юнита}. Для определения к какому юниту принадлежит модуль

    for type, unit, pid, sn in zip(list_type_module, list_number_unit, list_pid_module, list_sn_module):
        if type[1] == '3' and pid[1] != '':
            result_dict[unit[1]] = [type_options[type[1]], [pid[1].strip(), sn[1].strip()]]     # добавялем в итоговый словарь шасси
            parent_dict[type[0]] = unit[1]               # сразу формируем вспомогательный словарь

    for type, pid, sn, parent in zip(list_type_module, list_pid_module, list_sn_module, list_index_parent):
        if type[1] != '3' and pid[1] != '':
            parent_index = parent[1]
            unit = parent_dict[parent_index]
            result_dict[unit].append(type_options[type[1]], [pid[1].strip(), sn[1].strip()])    # добавляем в итоговый словарь модуль

    for pid, sn in zip(list_sfp_pid, list_sfp_sn):
        if 'OID' not in pid[1]:
            result_dict['1'].append(type_options[type[1]], [pid[1].strip(), sn[1].strip()])     # !!! НОДО ДОПИЛИТЬ СКРИПТ, чтобы номер юнита похорошему вычислялся, вдруг это кластер маршрутизаторов будет
                                                                                               # т.е. как с коммутаторами надо найти ветку где номер порта сопоставляется с номером юнита          
    return result_dict

def verify_selection(result_dict, serial):
    result = []
    for unit, options in result_dict.items():
        for type, pn, sn in options:
            if type == type_options['3'] and sn == serial:              # Проверить       
                return options
    return 'серийный номер не совпадает'     

if __name__ == "__main__":
    vendors = {
        '9': 'Cisco',
        '35265': 'Eltex'
    }
    #ip = '10.11.10.210'    # Cisco
    #ip = '10.11.10.211'    # MES 2348P
    #ip = '10.20.11.32'     # ia-mdc-lan-accs-csw-a09-1
    #ip = '172.16.50.173'   # ia-mdc-aux-uc-csw-1
    #ip = '10.20.11.43'     # MES 2308P
    #ip = '10.11.10.15'     # ia-rdc-lan-aggr-csw-137-1
    #ip = '10.20.11.4'      # MES 5448
    #ip = '172.16.50.137'   # Cisco 9300 stack
    #ip = '172.25.0.4'      # Eltex ESR 1500
    #ip = '172.25.0.2'      # Cisco ASR 1001X
    ip = '10.12.4.254'      # Cisco 6500
    #ip = '172.16.145.2'    # Cisco 6800
    serial = 'SMC1832000K'

    type_options = {
        '1': 'other',
        '2': 'unknown',
        '3': 'Шасси',
        '4': 'бэкплейн',
        '6': 'Блок питания',
        '7': 'Блок вентиляторов',
        '8': 'датчик',
        '9': 'Трансивер',
        '10': 'Сетевой модуль',
        '15': 'HDD'
    }
    
    session = Session(hostname=ip, community='CDUro', version=2)
    vendor_object = session.get('1.3.6.1.2.1.1.2.0')
    vendor_index = vendor_object[0].value.split('.')[-3]         # по индексу определяем вендоре в словаре vendors 

    vendor_name_object = session.get('1.3.6.1.2.1.1.1.0')
    if vendors[vendor_index] == 'Eltex':
        if 'ESR' in vendor_name_object[0].value:                 # пока так определяем, что это маршрутизатор Eltex
            result_dict = main_rt_eltex(session)
        else:
            result_dict = main_sw_eltex(session)
    elif vendors[vendor_index] == 'Cisco':
        result_dict = main_cisco(session)
    
    pprint(result_dict)
    print('#'*50) 
    pprint(verify_selection(result_dict, serial))

