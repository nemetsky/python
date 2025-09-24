import telnetlib
import time            
import socket                                     # для исключения, если оно вызвано другим модулем socket
from pprint import pprint

def to_bytes(line):                               # фукция конвертирует строку в байты и добавляет перевод строки
    return f"{line}\n".encode("utf-8")

def send_show_command(ip, user, password, enable, command, timeout=5):   # timeout сделали параметром функции необязательным 
    print(f"Подключаюсь к {ip}")
    try:                                                    # делаем исключение, если мы не сможем подключиться по таймауту
        with telnetlib.Telnet(ip, timeout=timeout) as t:    # задали таймаут на подключение
            r1.read_until(b"Username")                      # можно все выводы записывать в переменную log = b"" (и суммировать log += read_until(b"Username")) и потом в любой момент сделать print для диагностики
            r1.write(to_bytes(user))                        # применяем функцию к нашим данным которые передаем
            r1.read_until(b"Password")
            r1.write(to_bytes(password))      
            r1.read_until(b">")       
            t.write(b"enable\n")      
            t.read_until(b"Password") 
            r1.write(to_bytes(enable))         
            r1.read_until(b"#")
            r1.write(b"terminal length 0\n")
            r1.read_until(b"#")
            
            r1.write(to_bytes(command))
            output = r1.read_until(b"#").decode("utf-8")    # получаем вывод и переводим в обычную строку
            return output.replace("\r\n", "\n")
    except socket.timeout:
        print(f"Timeout при подключении к {ip}")
        
if __name__ == "__main__": 
    ip_list = ["10.10.10.1", "172.16.0.1"]  
    for ip in ip_list:    
        out = send_show_command(ip, "cisco", "cisco", "cisco", "sh clock")     
        pprint(out)