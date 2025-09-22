import pexpect
from getpass import getpass                             # как input, толко не показывает ввод


def send_show_command(ip, user, password, enable, command):
"""
Функции передаем данные для подключения к оборудованию и команду/список команд
Возвращается словарь вида {команда: вывод команды}
"""
    print(f"Подключаюсь к {ip}")
    cmd_output_dict = {}                                # результат функции будем собирать в словарь                                                                                                  
    try                                                                                # try/except лучше внутри функции писать, весь менеджер контекста загоняем в исключение, чтобы сессия в случае чего коректно завершилась
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:   # используем менеждер контекста, чтобы сессия закрывалась автоматически
            ssh.expect("Password")                                                     # timeout по умолчанию 30, уменьшим
    
            ssh.sendline(password)
            ssh.expect(">")
    
            ssh.sendline("enable")
            ssh.expect("[Pp]assword:")
    
            ssh.sendline(enable)
            ssh.expect("#")    
            
            ssh.sendline("terminal length 0")           # для show команд обязательно отключаем paging      
            ssh.expect("\S+#")                          # ждать не до решетки, а считать вывод до приглашения 'c3845-inet-2#'    
            promt = ssh.after                           # записали в переменную promt, то что после считанного вывода, т.е. 'c3845-inet-2#'
            
            if type(commands) == str:                   # проверка сколько команд надо выполнить в функции. Если "строка", то это одна команда
                commands = [commands]                   # то превращаем строку в список из одной команды
            
            for cmd in commands:
                ssh.sendline(cmd)                       
                ssh.expect(promt)                       # можно указывать переменную теперь вместо '#'  
                output = ssh.before + ssh.after         # '+ ssh.after' - чтобы в конце вывода не обрезался promt (например в конце будет теперь: c3845-inet-2#)
                output = output.replace("\r\n", "\n")   # лучше сделать замену, т.к. если применить pprint, то он покажет в выводе перенос каретки \r, удалить ее лучше сразу
                cmd_output_dict[cmd] = output           # возвращать функция будет словарь вида {команда: вывод команды}
        return cmd_output_dict   
    except pexpect.TIMEOUT as error:                    # если к какому-то устройству не подключимся, то получим сообщение, но дальше к другим устройствам продолжим подключаться
        print(f"Ощибка при подключении к {ip}")                                        
                                                                                       
if __name__ == "__main__":                                                             
    ip_list = ["10.10.10.1", "172.16.0.1"]              # подключение к оборудованию будет последовательное
    commands = ["sh clock", "sh ip int brief"]
    result = {}
    user = input("Username: ")
    password = getpass()                                # запрос пароля (по умолчанию запрос вида 'Password:')
    ena_password = getpass("Enable password: ")         # запрос пароля 
    for ip in ip_list:
        #out = send_show_command(ip, "cisco", "cisco", "cisco", "sh ip int brief")     
        out = send_show_command(ip, user, password, ena_password, commands)
        print(out)
        result[ip] = out                                # можем записать теперь в словарь вида {ip_1: {команда_1: вывод команды, команда_2: вывод команды}, 
                                                        #                                       ip_2: {команда_1: вывод команды, команда_2: вывод команды}}
                                                        # словарь можно теперь перебирать и парсить или в JSON записать например