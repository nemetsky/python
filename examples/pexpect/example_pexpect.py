import pexpect

def send_show_command(ip, user, password, enable, command):
    with pexpect.spawn(f"ssh {user}@{ip}", timeout=10, encoding="utf-8") as ssh:   # используем менеждер контекста, чтобы сессия закрывалась автоматически
        ssh.expect("Password")                                                     # timeout по умолчанию 30, уменьшим

        ssh.sendline(password)
        ssh.expect(">")

        ssh.sendline("enable")
        ssh.expect("Password")

        ssh.sendline(enable)
        ssh.expect("#")

        ssh.sendline("terminal length 0")
        ssh.expect("#")

        ssh.sendline(command)
        ssh.expect("#")
        output = ssh.before + ssh.after             # '+ ssh.after' - чтобы в конце вывода не обрезалась решетка после имени устройства (например: c3845-inet-2#)
        return output.replace("\r\n", "\n")         # лучше сделать замену, т.к. если применить pprint, то он покажет в выводе перенос каретки \r, удалить ее лучше сразу

if __name__ == "__main__":
    ip_list = ["10.10.10.1", "172.16.0.1"]          # подключение к оборудованию будет последовательное
    for ip in ip_list:
        out = send_show_command(ip, "cisco", "cisco", "cisco", "sh ip int brief")
        print(out)
