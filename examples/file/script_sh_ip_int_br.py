'''
result = [
    ['FastEthernet0/0', '15.0.15.1'],
    ['FastEthernet0/1', '10.0.12.1'],
    ['FastEthernet0/2', '10.0.13.1']
]
'''
# Задача из вывода команды show ip int br получить только интерфейсы и их IP-адреса как показано выше в виде списка списков

from pprint import pprint

result_list = []                                 # пустой список

with open("sh_ip_int_br.txt", "r") as f:
    for line in f:                               # перебираем строки из файлы  
        line_list = line.split()                 # разбиваем каждую строку на список слов, split по умолчанию удаляет все пробелы и скрытые символы (переводы строк и т.д)
        if line_list:                            # if len(line_list !=0) если не пустой список
            str_index_0 = line_list[0]           # присваиваем переменной первый элемент(слово) строки
            if str_index_0[-1].isdigit():        # проверяем чтобы последний символ первого слова оканчивался на цифру
                # print(line_list[:2])           # печатаем 1-ый и второй элемент строки(списка) с помощью среза
                intf_ip_list = line_list[:2]     # присваиваем новой переменной список состоящий из интерфейса и адреса
                result_list.append(intf_ip_list) # добавляем этот список в другой список (вложенный ранее созданный пустой)   

pprint(result_list)                              # печатаем спомощью pprint чтобы покрасивее было        

# Оптимизация           
'''
from pprint import pprint

result_list = []

with open("sh_ip_int_br.txt", "r") as f:                
    for line in f:                                              
        line_list = line.split()                                                                     
        if line_list and line_list[0][-1].isdigit():   # объединили два условия сразу и исключили промежуточные переменные                                  
            result_list.append(line_list[:2])          # (сначало обязательно идет условие что список не пустой, иначе будет ошибка если попадется пустая строка)                             

pprint(result_list)
'''         

# ========================================================================================

'''
result = {
    'FastEthernet0/0': '15.0.15.1',
    'FastEthernet0/1': '10.0.12.1',
    'FastEthernet0/2': '10.0.13.1'
}
'''
# Задача та же только получить результат в виде словаря как показано выше

result_dict = {}                              

with open("sh_ip_int_br.txt", "r") as f:
    for line in f:                              
        line_list = line.split()                
        if line_list and line_list[0][-1].isdigit():
            intf, ip = line_list[:2]                    # intf, ip = line_list[0], line_list[1]  -  тоже самое (такая вот распаковка переменных)  
            if ip == "unassigned":                      # НЕОБЯЗАТЕЛЬНО, можно проверить что-то и присвоить другое значение (к примеру адрес если не назначен вывести "IP отсутствует")
                ip = None                               # или можно присвоить None, если мы хотим в последующем проверять словарь 
            result_dict[intf] = ip                      # записать в словарь ключ (интерфейс) со значением (ip-адрес)

pprint(result_dict)                             


'''
# Пример, потом вывести только интерфейсы на которых IP назначен (если до этого присвоили None интерфейсам с неназначенными адресами)

for intf,ip in result_dict.items():
    if ip:                              # или    if not ip
        print(intf)
'''
