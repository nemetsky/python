import paramiko
import time
import socket
import getpass
from pprint import pprint

def send_show_command(
    ip, user, password, enable, command,
    short_sleep=0.2, max_read=100000, long_sleep=2           # задали паузы и сколько байт считывать глобально, чтобы в теле скрипта не задавать каждый раз
):
    try:                                                     # обрабатываем исключение на подключение 
        cl = paramiko.SSHClient()
        cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cl.connect(
            hostname=ip, 
            username=user, 
            password=password, 
            look_for_keys=False, 
            allow_agent=False,
            timeout=5                                        # можно здесь сразу таймаут задать на подключение (отдельно ssh.settimeout(5) - это таймаут на ожидание вернуть что-нибудь)
        )
    except socket.timeout:                                   # внешение исключение из socket
        print(f"Не удалось подключиться к {ip}")
        return                                               # если не подключились, то функция прерветься. Можно без return в этом месте, тогда надо делать else в конструкции try/except
    # except paramiko.ssh_exception.AuthenticationException  # делаем еще исключение, если не правильно пароль задали при подключении (таких исключений может быть много)
                                                             # но можно задать одно родительское исключение, чтобы все не перечислять исключения paramiko
    except paramiko.SSHException as error:                   # задаем родительское исключения paramiko
        print(f"Возникла ошибка {error} на {ip}")
        return                                               # если не подключились, то функция прерветься. 
                                                             # Но скрипт не прервется, удобно, так как к следующим устройствам дальше будем подключаться
    with cl.invoke_shell() as ssh:
        #ssh.send("enable\n")       
        #ssh.send(f"{enable}\n")
        #time.sleep(short_sleep)
        ssh.send("terminal length 0\n")
        time.sleep(short_sleep)
        ssh.recv(max_read)                                   # считываем все, чтобы потом уже вести команду и лишние при следующем считывании не получить
        
        ssh.send(f"{command}\n")
        time.sleep(long_sleep)
        output = ssh.recv(max_read).decode("utf-8").replace("\r\n", "\n")
        return output

if __name__ == "__main__":                                                             
    ip_list = ["10.11.10.107"]
    password = getpass.getpass()
    for ip in ip_list:
        out = send_show_command(ip, "nemetskiy-sv", password, "cisco", "sh int descr")     
        pprint(out, width=120)
