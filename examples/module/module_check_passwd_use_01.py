from pprint import pprint
from module_check_passwd_01 import check_passwd, data           # импортируем функцию и переменную из собственный модуль, но при спользовании check_passwd весь модуль module_check_passwd_01 выполниться
                                                                # поэтому в модуле module_check_passwd_01 используем переменную __name__ (см. там), чтобы использовать только функции из того модуля

# import module_check_passwd_01   # или так импортировать тогда обращаться к фуккции надо так:  module_check_passwd_01.check_passwd, а к переменной module_check_passwd_01.data                             
                                                                
def check_user_list(user_passwd_data, **kwargs):      
    correct_users = []                     
    wrong_users = []
    for username, password in user_passwd_data:     
        check = check_passwd(username, password, **kwargs)  
        if check:                                  
            correct_users.append(username)     
        else:
            wrong_users.append(username)
    return correct_users, wrong_users         

ok, no_ok = check_user_list(data, min_len=4, check_numbers=True) 
pprint(ok)                   
pprint(no_ok)