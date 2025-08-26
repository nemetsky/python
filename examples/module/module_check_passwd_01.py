
def check_passwd(username, password, *, min_len=8, check_numbers=False):
    if len(password) < min_len:
        return False
    elif username.lower() in password.lower():                      
        return False
    elif check_numbers and len(set("0123456789") & set(password)) < 3:  
        return False
    else:
        return True

data = [                               
    ["user1", "jsadhkj567asd"],
    ["user2", "20"],
    ["user3", "user3jsadhkjasd"],                      
]

# print(__name__)                                       # можно посмотреть что содержится в переменной __name__ при использовании импорта в другом скрипте

if __name__ == "__main__":                              # значит выполнить код, если модуль не импортируется,  __main__ - специальная переменная
    print("Тестовая проверка")                          # Если запустит этот скрпит напрямую, то эти строки выполняться
    print(check_passwd("user1", "hbdsfdsf32782309"))
    print(check_passwd("user2", "hbds309"))