# 1.3.6.1.2.1.31.1.1.1.1 - посмотреть индексы портов

from snmp_cmds import snmpwalk
from snmp_cmds import Session
from snmp_cmds.exceptions import SNMPTimeout
from pprint import pprint
import time

#print(snmpwalk.__code__.co_varnames)    # вывести доступные аргументы в функции

#ip = '10.11.10.211'
ip = '10.20.11.32'

# 2-ой способ с session, тоже рабочий но также глючит 
#session = Session(ipaddress=ip, read_community='CDUro')
#output_pid = session.walk(oid='1.3.6.1.2.1.47.1.1.1.1.13')
#session = Session(ipaddress=ip, read_community='CDUro')
#output_sn = session.walk(oid='1.3.6.1.2.1.47.1.1.1.1.11')

# определяем количество юнитов в стеке
output_number_sw = snmpwalk(
    oid='1.3.6.1.4.1.89.53.8',
    community='CDUro', 
    ipaddress=ip, 
)
number_sw = int(output_number_sw[0][1])

# делаем заготовку итогового словаря, в котором ключ - это номер юнита, значение - список списков с всеми опциями (PID, SN)
out_dict = {}
for i in range(1,number_sw+1):               # {1: [], 2: [], ...}
    out_dict[i] = []

# считываем информацию по модулям коммутатора (PID коммутатора и блоков питания)
try:
    output_pid = snmpwalk(
        oid='1.3.6.1.2.1.47.1.1.1.1.13',
        community='CDUro', 
        ipaddress=ip,
        timeout=10
    )
except SNMPTimeout:
    print("Ошибка 1")

# считываем информацию по модулям коммутатора (SN коммутатора и блоков питания)
try:
    output_sn = snmpwalk(
        oid='1.3.6.1.2.1.47.1.1.1.1.11',
        community='CDUro', 
        ipaddress=ip,
        timeout=10
    )
except SNMPTimeout:
    print("Ошибка 2")

# с помощью функции zip складываем/сопоставляем полученные списки кортежей и берем только необходимые значения PID и SN, удаляя OID, но смотрим индексы модулей 
try:
    result_module = list(zip(output_pid, output_sn)) 
    for pid, sn in result_module:
        if pid[1] != '""':
            list1 = [pid[1].strip('"'), sn[1].strip('"')]
            index = int(pid[0].split('.')[-1])
            if index in range(67108864,134217728):           # надо что-то думать по другому делать с блоками питания, автоматически индексы надо высчитывать
                out_dict[1].append(list1)
            elif index in range(134217728,201326592):
                out_dict[2].append(list1)
            #elif index in range(313,469):                     
            #    out_dict[3].append(list1)
            #elif index in range(469,625):
            #    out_dict[4].append(list1)            
            #print(f"{index} = {pid[1]} = {sn[1]}")
except NameError:
    print("")

time.sleep(3)

# считываем информацию по трансиверам(PID и SN)
output_sfp_pid = snmpwalk(
    oid='1.3.6.1.4.1.35265.1.23.53.1.1.1.10',
    community='CDUro', 
    ipaddress=ip, 
)
output_sfp_sn = snmpwalk(
    oid='1.3.6.1.4.1.35265.1.23.53.1.1.1.6',
    community='CDUro', 
    ipaddress=ip, 
)
result_sfp = list(zip(output_sfp_pid, output_sfp_sn)) # таже складываем/сопоставляем трансиверы (PID и SN) с помощью функции zip

# делаем вспомогательный словарь, к котором сопосталяем индекс порта с номером юнита  {'49': '1', '50': '1', '51': '1 ...} Как оказалось в словарь не попадают стековые порты
num_dict = {}
output_index_num = snmpwalk(
    oid='1.3.6.1.4.1.89.53.3.1.5',
    community='CDUro', 
    ipaddress=ip, 
)
output_index_stack = snmpwalk(
    oid='1.3.6.1.4.1.89.53.23.1.4',
    community='CDUro', 
    ipaddress=ip, 
)
for i in output_index_stack:
    index = i[0].split('.')[-1]
    num_dict[index] = i[1]

for i in output_index_num:
    index = i[0].split('.')[-1]
    num_dict[index] = i[1]
print(num_dict)


if result_sfp[0][0][1] != None:
    for sfp_pid, sfp_sn in result_sfp:
        list1 = [sfp_pid[1].strip('"'), sfp_sn[1].strip('"')]
        """
        index = int(sfp_pid[0].split('.')[-1])        # первый способ, неудобный так как диапазон индексов вручную задан               
        if index <= 156:                                       
            out_dict[1].append(list1)
        elif index in range(157,313):
            out_dict[2].append(list1)
        elif index in range(313,469):
            out_dict[3].append(list1)
        elif index in range(469,625):
            out_dict[4].append(list1)
        """
        index = sfp_pid[0].split('.')[-1]            # второй правильный способ используя вспомогательный словарь,
        number_stack = int(num_dict[index])          # но как оказалось в словаре нет стековых портов
        pprint(num_dict[index])
        out_dict[number_stack].append(list1)
        
pprint(out_dict)   
        
 






