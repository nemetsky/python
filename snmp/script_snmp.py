from ezsnmp import Session
from ezsnmp.exceptions import TimeoutError
from pprint import pprint
import logging
import sys
import subprocess

type_options = {
    '1': 'other',
    '2': 'unknown',
    '3': '_Шасси_',
    '4': 'backplane',
    '5': 'container',
    '6': 'Блок питания',
    '7': 'Блок вентиляторов',
    '8': 'sensor',
    '9': 'Сетевой модуль',
    '10': 'Трансивер',
    '11': 'stack',
    '12': 'cpu',
    '13': 'energyObject',
    '14': 'battery',
    '15': 'storageDrive'
}

logger = logging.getLogger("module_snmp")    # настраиваем дочерний логгер для главного модуля
logger.setLevel(logging.INFO)

# функция получает вывод OID в виде объектов Python, возвращает список кортежей [(index, значение),...]
def get_list(iterable_object):
    list1 = []
    for item in iterable_object:
        list1.append((item.index, item.value))
    return list1

# функция, в которую передаем сессию snmp коммутатора или маршрутизатора Cisco, возвращает итоговый словарь опций
def main_cisco(session):
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

    result_dict = {}         # основной словарь {Номер юнита : список списков опций}
    sw_index_unit_dict = {}  # вспомогательный словарь 1 {Индекс коммутатора: номер юнита}
    parent_dict = {}         # вспомогательный словарь 2 {Индекс опции/модуля: Родительский индекс}

    for type, unit, pid, sn in zip(list_type_module, list_number_unit, list_pid_module, list_sn_module):
        if type[1] == '3' and pid[1] != '':
            number_unit = unit[1]                                                                   # определяем номер юнита
            result_dict[number_unit] = [[type_options[type[1]], pid[1].strip(), sn[1].strip()]]     # добавялем в основной словарь шасси
            sw_index_unit_dict[type[0]] = number_unit                                               # сразу формируем вспомогательный словарь 1

    for index, parent in list_index_parent:
        parent_dict[index] = parent                                                                 # формируем вспомогательный словарь 2

    for type, pid, sn, fru in zip(list_type_module, list_pid_module, list_sn_module, list_fru_tag):
        if (type[1] != '11' and type[1] != '3') and pid[1] != '' and fru[1] == '1':                 # если компонент не является стеком или шасси, и модуль заменяемый
            current_index = type[0]                                                                 # определяем индекс опции
            while True:                                                                             # делаем цикл в котором ищем самый родительский индекс опции/модуля, чтобы привязать его к шасси
                parent_index = parent_dict[current_index]
                current_index = parent_index
                if parent_index in sw_index_unit_dict:                                              # если родительский индекс есть в нашем вспомогательном словаре 1, мы нашли родительское шасси и выходим из цикла
                    unit = sw_index_unit_dict[current_index]                                        # определяем номер юнита шасси
                    break
            result_dict[unit].append([type_options[type[1]], pid[1].strip(), sn[1].strip()])        # добавляем в основной словарь к нашему шасси опцию (БП, модуль, трансивер и т.п.)
    return result_dict


def main_sw_eltex(session):
    result_dict = {}  # основной словарь {Номер юнита: Список списоков опций PID, SN}
    index_parent_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.4')
    type_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.5')
    number_unit_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.6')
    sn_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
    pid_module_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
    fru_tag_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.16')
    sfp_pid_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.10')
    sfp_sn_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.6')
    ports_unit_object = session.walk('1.3.6.1.4.1.89.53.3.1.5')
    ports_unit_stack_object = session.walk('1.3.6.1.4.1.89.53.23.1.4')  # требуется для стеков, информация по стековым портам (к какому юниту они принадлежат)
    list_index_parent = get_list(index_parent_object)
    list_type_module = get_list(type_module_object)
    list_number_unit = get_list(number_unit_object)
    list_sn_module = get_list(sn_module_object)
    list_pid_module = get_list(pid_module_object)
    list_fru_tag = get_list(fru_tag_object)
    list_sfp_pid = get_list(sfp_pid_object)
    list_sfp_sn = get_list(sfp_sn_object)
    list_ports_unit = get_list(ports_unit_object)
    list_ports_unit_stack = get_list(ports_unit_stack_object)

    parent_dict = {}  # вспомогательный словарь {Индекс коммутатора: номер юнита}. Для определения к какому юниту принадлежит БП

    for type, unit, pid, sn in zip(list_type_module, list_number_unit, list_pid_module, list_sn_module):
        if type[1] == '3' and pid[1] != '':
            result_dict[unit[1]] = [[type_options[type[1]], pid[1].strip(), sn[1].strip()]]     # добавялем в итоговый словарь шасси
            parent_dict[type[0]] = unit[1]                                      # сразу формируем вспомогательный словарь

    for type, pid, sn, parent, fru in zip(list_type_module, list_pid_module, list_sn_module, list_index_parent, list_fru_tag):
        if type[1] == '6' and pid[1] != '' and fru[1] == '1':
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
            list1 = [type_options['10'], sfp_pid[1].strip(), sfp_sn[1].strip()]
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
            result_dict[unit[1]] = [[type_options[type[1]], pid[1].strip(), sn[1].strip()]]     # добавялем в итоговый словарь шасси
            parent_dict[type[0]] = unit[1]                                                    # сразу формируем вспомогательный словарь

    for type, pid, sn, parent in zip(list_type_module, list_pid_module, list_sn_module, list_index_parent):
        if type[1] != '3' and pid[1] != '':
            parent_index = parent[1]
            unit = parent_dict[parent_index]
            result_dict[unit].append([type_options[type[1]], pid[1].strip(), sn[1].strip()])  # добавляем в итоговый словарь модуль

    for pid, sn in zip(list_sfp_pid, list_sfp_sn):
        if 'OID' not in pid[1]:
            result_dict['1'].append([type_options['10'], pid[1].strip(), sn[1].strip()])     # !!! НОДО ДОПИЛИТЬ СКРИПТ, чтобы номер юнита похорошему вычислялся, вдруг это кластер маршрутизаторов будет
                                                                                             # т.е. как с коммутаторами надо найти ветку где номер порта сопоставляется с номером юнита
    return result_dict

def verify_sn_and_select(result_dict, serial):
    result = []
    for unit, options in result_dict.items():
        for type, pn, sn in options:
            if type == type_options['3'] and sn == serial:
                return options
    logger.warning(error := "Серийный номер из СУУС ИТ не совпадает с серийным номером оборудования")
    return error

def check_dns(ip, fqdn):
    try:
        record_a = subprocess.run(['dig', fqdn, '+short'], stdout=subprocess.PIPE, encoding="utf=8", check=True) # check=True -> если dig выполнился с ошибкой, то сработает исключение
        #record_a = subprocess.run(['dig', fqdn, '+short'], capture_output=True, text=True, check=True)           # Можно так, тоже самое
        ip_in_dns = record_a.stdout.rstrip('\n')
        record_rtp = subprocess.run(['dig', '-x', ip, '+short'], stdout=subprocess.PIPE, encoding="utf=8", check=True)
        fqdn_in_dns = record_rtp.stdout.rstrip('.\n')
        #check_a = True if ip = ip_in_dns else False:                                                                # Можно так
        #check_a = (ip == ip_in_dns)
        error1 = error2 = ''
        if ip_in_dns == '':
            logger.error(error1 := 'Отсутствует запись DNS для %s в прямой зоне. ' %fqdn)
            check_a = True
        elif check_a := (ip != ip_in_dns):                                               #  используем маржовый оператор :=, полюбому присвоит переменной check_a значение исходя из проверки условий
            logger.error(error1 := 'Запись DNS для %s не совпадает в прямой зоне (%s != %s). ' %(fqdn, ip, ip_in_dns))
        if fqdn_in_dns == '':
            logger.error(error2 := 'Отсутствует запись DNS для %s в обратной зоне.'  %ip)
            check_rtp = True
        elif check_rtp := (fqdn != fqdn_in_dns):
            logger.error(error2 := 'Запись DNS для %s не совпадает в обратной зоне (%s != %s).' %(ip, fqdn, fqdn_in_dns))
        if not check_a and not check_rtp:
            return True
        else:
            return error1 + error2
    # except FileNotFoundError:
    #    logger.error('Утилита dig не найдена')
    # except subprocess.CalledProcessError as e:
    #    logger.error(f'Ошибка выполнения команды dig: {e}. Детали ошибки: {e.stderr}')
    except Exception as e:
        logger.error(f"Произошла ошибка при проверке DNS-записи: {e}")
        return f"Произошла ошибка пр проверки DNS"

def main(ip):
    vendors = {
        '9': 'Cisco',
        '35265': 'Eltex'
    }
    logger.info(f"---> Подключаюсь к {ip}")
    try:
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
        logger.info("<--- Список опций с %s успешно собран", ip)
        return result_dict
    except TimeoutError:
        logger.error(error := "Устройство %s недоступно по SNMP" %ip)
        return error
    except Exception as Error:
        #traceback.print_exc()
        line_num = sys.exc_info()[2].tb_lineno
        logger.error("Устройство %s не поддерживается. Ошибка скрипта в строке %s: %s: %s", ip, line_num, Error.__class__.__name__, Error)
        return f"Произошла ошибка. Устройство не поддерживается."


if __name__ == '__main__':
    # настраиваем в этом месте логирование (RootLogger) для случая, если запускаем модуль отдельно
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)8s %(name)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    ip = '10.11.10.210'    # Cisco
    ip = '10.11.10.211'    # MES 2348P
    ip = '10.20.11.32'     # ia-mdc-lan-accs-csw-a09-1
    #ip = '172.16.50.173'   # ia-mdc-aux-uc-csw-1
    #ip = '10.20.11.43'     # MES 2308P
    #ip = '10.11.10.15'     # ia-rdc-lan-aggr-csw-137-1
    #ip = '10.20.11.4'      # MES 5448
    #ip = '172.16.50.137'   # Cisco 9300 stack
    #ip = '172.25.0.4'      # Eltex ESR 1500
    #ip = '172.25.0.2'      # Cisco ASR 1001X
    #ip = '10.12.4.254'     # Cisco 6500
    #ip = '172.16.145.2'    # Cisco 6800
    #ip = '10.11.10.107'    # Eltex 2300B-48
    ip = '172.16.50.131'   # Cisco 4451
    ip = '172.25.0.15'     # Cisco 4431
    ip = '172.25.0.1'      # Cisco ASR 1006X
    ip = '172.25.0.31'      # Cisco  3850
    ip = '172.25.0.8'      # Cisco 3850 Stack
    #ip = '172.25.0.6'      # Cisco 7206
    #ip = '10.5.19.4'      # Cisco 2960-XR
    
    serial = 'FXS2526Q22T'

    result = main(ip)
    pprint(result)
    print('#'*50)
    #pprint(verify_sn_and_select(result, serial))

    #ip = '10.20.11.32'
    #ip = '178.74.128.173'
    #name = 'ia-mdc-lan-accs-csw-a09-1.cd.so'
    #name = 'br.so-ups.ru'
    #print(type(check_dns(ip, name)))
