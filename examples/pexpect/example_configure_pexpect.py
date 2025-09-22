import pexpect
from getpass import getpass                             # как input, толко не показывает ввод


def send_cfg_command(ip, user, password, enable, command):
"""
Функции передаем данные для подключения к оборудованию и команду/список команд
Возвращается словарь вида {команда: вывод команды}
"""
    print(f"Подключаюсь к {ip}")
    cmd_output = ""                                     # результат функции будем собирать в одну строку                                                                                                  
    try                                                                                # try/except лучше внутри функции писать, весь менеджер контекста загоняем в исключение, чтобы сессия в случае чего коректно завершилась
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:   # используем менеждер контекста, чтобы сессия закрывалась автоматически
            ssh.expect("Password")                                                     # timeout по умолчанию 30, уменьшим
            ssh.sendline(password)
            ssh.expect(">")
            ssh.sendline("enable")
            ssh.expect("[Pp]assword:")
            ssh.sendline(enable)
            ssh.expect("\S+#")                          # ждать не до решетки, а считать вывод до приглашения 'c3845-inet-2#'    
            promt = "\(config\S*\)#"                    # promt теперь для режима конфига можно указать регуляркой, попадет под нее: '(config)#', '(config-if)#', '(config-line)#'
            
            if type(commands) == str:                   # проверка сколько команд надо выполнить в функции. Если "строка", то это одна команда
                commands = ["conf t", commands, "end"]  # превращаем строку в список, и добавляем команды для входы и выхода из режиам конфигурирования
            else:
                commands = ["conf t", *commands, "end"] # если список/кортедж команд, то команды распокавать команды (*commands) в наш список как отдельные элементы (удобный прием)
            
            for cmd in commands:
                #print(f"{cmd=}")                        # для диагностики 
                ssh.sendline(cmd)                       
                ssh.expect([promt, "#"])                # указываем что ожидать или promt или "#", т.к. после команды end promt '(config)#' не будет уже   
                output = ssh.before + ssh.after         # '+ ssh.after' - чтобы в конце вывода не обрезался promt (например в конце будет теперь: c3845-inet-2#)
                output = output.replace("\r\n", "\n")   # лучше сделать замену, т.к. если применить pprint, то он покажет в выводе перенос каретки \r, удалить ее лучше сразу
                #print(f"{output=}")                    # для диагностики 
                if "%" in output:                       # если в выводе есть "%" (в cisco так ошибки начинаются)
                    print(                                               # !!! вместо print в этом месте можно использовать конструкцию raise (ПОДРОБНО ВНИЗУ) 
                        f"При выполнение команды {cmd} возникла ошибка "
                        f"{output}"
                    )
                    break                               # вывести ошибку и дальше команды не отправлять, выйти из цикла (c raise этого не надо будет делать)
                cmd_output += output                    # возвращать функция будет большую суммируемую строку  # cmd_output = cmd_output + output
        return cmd_output  
    except pexpect.TIMEOUT as error:                    # если к какому-то устройству не подключимся, то получим сообщение, но дальше к другим устройствам продолжим подключаться
        print(f"Ощибка при подключении к {ip}")
        print(error)                                    # если проблемы с подключением, то можно так посмотреть подробный вывод ошибки
                                                                                       
if __name__ == "__main__":                                                             
    ip_list = ["10.10.10.1", "172.16.0.1"]              # подключение к оборудованию будет последовательное
    commands = ["interface lo77", "ip add 10.1.1.1 255.255.255.255"]
    user = input("Username: ")
    password = getpass()                                # запрос пароля (по умолчанию запрос вида 'Password:')
    ena_password = getpass("Enable password: ")         # запрос пароля 
    for ip in ip_list:
        out = send_cfg_command(ip, user, password, ena_password, commands)
        print(out)


"""
Пример c raise

                ...
                if "%" in output:   
                    raise ValueError(                                              
                        f"При выполнение команды {cmd} возникла ошибка "
                        f"{output}"
                    )
                ...
                
if __name__ == "__main__":                                                             
    ...
    for ip in ip_list:
        try:
            out = send_cfg_command(ip, user, password, ena_password, commands)
        expect ValueError as error:
            print(error)
        break
"""




                                                      