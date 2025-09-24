# === Пример с paging-ом, т.е. когда вывод show большой на несколько страниц и paging мы не отключаем === 

# Прием довольно таки распространненый, например если вывод гигансткий, из-за раз не считывается
# Или прием с циклом while нужен тогда, когда нам надо читать вывод до какого-то определенного момента (или, например, ждем когда пинг не закончится)
 
import pexpect
import re
import time                     # использовали sleep
from pprint import pprint


def send_show_command(ip, user, password, enable, command):

    print(f"Подключаюсь к {ip}")
    try                                                                                
        with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:   
            ssh.expect("Password")                                                  
            ssh.sendline(password)
            ssh.expect(">")
            ssh.sendline("enable")
            ssh.expect("[Pp]assword:")
            ssh.sendline(enable)
            ssh.expect("\S+#")                         
            prompt = ssh.after      # содержит имя устойства, например 'R1#'                        
            ssh.sendline(command)                                                     # отправили команду show...
            output = ""                                                               
            while True:                                                               # делаем бесконечный цикл пока весь вывод не считаем
                index = ssh.expect([prompt, "--More--", pexpect.TIMEOUT], timeout=1)  # expect возвращаем индекс, если вернулось 'R1#' значит вывод весь считался, значит индекс 0 вернет
                                                                                      # также добавляем timeout, хотя бы несколько секунду между считыванием страниц          
                time.sleep(1)                                                         # можно еще опционально сделать паузу (для контроля)                                                                                                
                page = ssh.before                                                     # считываем нащу страницу
                page = re.sub(r" +\x08+ +\x08+", "\n", page)                          # в выводе будут скрытые символы backspace 'x08' (\b), визуально их не будет видно (но в выводе pprint увидим), и если потом этот вывод записать в файл, то будет видно кракозябры ^H
                                                                                      # поэтому эти символы сразу заменим на перевод строки просто, (!!! также в конфиги может остаться пустые строки с пробелом в начале, их можно тоже регуляками поудаля)
                output += page                                                        # к итоговому выводу прибавляем считанную страницу
                if index == 0:                                                        # если все считалост вывходим из цикла
                    break                                                             
                elif index == 1:                                                      # если вывод считался не полностью, появилось '--More--', то отправить пробел с помощью метода send 
                    ssh.send(" ")                                                     
                else:                                                                 
                    print("Timeout")                                                  # если ошибка (исключение pexpect.TIMEOUT), то выйти из цикла 
                    break
        return output.replace("\r\n", "\n") 
    except pexpect.TIMEOUT as error:                    
        print(f"Ощибка при подключении к {ip}")         
                                                        
if __name__ == "__main__":                              
    out = send_show_command("10.10.10.1", "cisco", "cisco", "cisco", "sh run")     
    pprint(out)

    # with open("r1_cfg.txt", "w") as f:            # для теста записать вывод в фал и посмотреть скрытые символы x08, когда их не заменяем 
    #     f.write(out)
    