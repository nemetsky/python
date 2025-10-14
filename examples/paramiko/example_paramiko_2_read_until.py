"""
В этом примере  реализовываем конструкцию на подобие read_until как в модуле telnetlib
Это необязательно, но чтобы не думать а дочиталось ли все до конца, и не зависеть от max_read (так как мы не знаем насколько большой вывод может быть получен и если задавать в байтах его, то все равно может не хватить байт)

"""

"""
import paramiko
import time
import socket
import getpass
import re
from pprint import pprint

def send_show_command(
    ip, user, password, enable, command,
    short_sleep=0.2, max_read=100000, long_sleep=2           
):                                                           
    try:                                                     
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cl.connect(
            hostname=ip, 
            username=user, 
            password=password, 
            look_for_keys=False, 
            allow_agent=False,
            timeout=5                                        
        )                                                    
    except socket.timeout:                                          
        print(f"Не удалось подключиться к {ip}")             
        return                                               
    except paramiko.SSHException as error:                   
        print(f"Возникла ошибка {error} на {ip}")            
        return                                               
                                                             
    with cl.invoke_shell() as ssh:
        ssh.send("terminal length 0\n")
        time.sleep(short_sleep)
        output = ssh.recv(max_read).decode("utf-8")             # добавляем переменную, в которую считываем что вывелось на устройстве
        prompt = re.search(r"\S+#", output).group()             # регуляркой описываем наше приглашение на устройстве, например R1#, дальше будем искать это приглашение
        
        ssh.send(f"{command}\n")                                # отправляем команду
        output = ""                                             # обнуляем переменную с выводом и будем в нее собирать вывод нашей команды по кусочкам
        ssh.settimeout(3)                                       # !!! делаем таймаут на возвращение вывода, сколько recv должен ждать вывод с оборудования (нужен если от оборудование ничего нет, никаких символов)
        while True:                                             # делаем бесконечный цикл
            time.sleep(short_sleep)
            try:                                                # делаем исключение, если приглашение не дождемся по какой-то причине, то прервем цикл, но вывод все равно какой-нибудь получим, который собрали
                part = ssh.recv(100).decode("utf-8")            # собираем вывод по 100 байт/символов
            except socket.timeout:
                break
            output += part                                      # суммируем вывод 
            if prompt in output:                                # если встретили в выводе "R1#", значит дочитали до конца (до приглашения) и прерываем цикл
                break                                    
        output = output.replace("\r\n", "\n")
        return output

if __name__ == "__main__":                                                             
    ip_list = ["10.11.10.107"]
    password = getpass.getpass()
    for ip in ip_list:
        out = send_show_command(ip, "nemetskiy-sv", password, "cisco", "sh int descr")     
        pprint(out, width=120)
"""

# ==============================================================================================

"""
Можно в отдельную функцию read_until выделить наш сбор по кусочкам и поиск нужного приглашения
Можно потом эту функцию использовать хоть где, где используем paramiko
"""

import paramiko
import time
import socket
import getpass
import re
from pprint import pprint

def send_show_command(
    ip, user, password, enable, command,
    short_sleep=0.2, max_read=100000, long_sleep=2           
):                                                           
    try:                                                     
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cl.connect(
            hostname=ip, 
            username=user, 
            password=password, 
            look_for_keys=False, 
            allow_agent=False,
            timeout=5                                        
        )                                                    
    except socket.timeout:                                          
        print(f"Не удалось подключиться к {ip}")             
        return                                               
    except paramiko.SSHException as error:                   
        print(f"Возникла ошибка {error} на {ip}")            
        return                                               
                                                             
    with cl.invoke_shell() as ssh:
        ssh.send("terminal length 0\n")
        time.sleep(short_sleep)
        output = ssh.recv(max_read).decode("utf-8")             
        prompt = re.search(r"\S+#", output).group()             
                                                                
        ssh.send(f"{command}\n")                                
        output = read_until(ssh, prompt)                    # передаем нашу сессию ssh "cl.invoke_shell()" в функцию и получаем наш вывод. Удобно использовать отдельно функцию
        return output

def read_until(ssh_conn, prompt, short_sleep=0.2):          # вынесли в отдельную функцию наш сбор по кусочкам вывода до приглашения, 
                                                            # в функцию передаем целиком сессию ssh как аргумент ssh_conn и приглашение prompt
    output = ""                                             
    ssh_conn.settimeout(3)                                       
    while True:                                             
        time.sleep(short_sleep)                             
        try:                                                
            part = ssh_conn.recv(100).decode("utf-8")            
        except socket.timeout:                              
            break                                           
        output += part                                      
        if prompt in output:                                
            break                                    
    output = output.replace("\r\n", "\n")
    return output

if __name__ == "__main__":                                                             
    ip_list = ["10.11.10.107"]
    password = getpass.getpass()
    for ip in ip_list:
        out = send_show_command(ip, "nemetskiy-sv", password, "cisco", "sh int descr")     
        pprint(out, width=120)



























