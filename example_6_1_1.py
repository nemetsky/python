﻿username = input("Введите имя пользователя: ")
password = input("Введите пароль: ")

#if len(password) < 8:
#    print("Пароль слишком короткий")
#elif username.lower() in password.lower():                           # не учитываем регистр при сравнении пользователя и пароля, поэтому переводим и имя пользователя и пароль в нижний регистр
#    print("Пароль содержит имя пользователя")
#elif len(set("0123456789") & set(password)) < 3:                     # переводи пароль в множество, сравниваем с множеством чисел, проверяем количество общих чисел (уникальных)
#    print("В пароле должны быть как минимум 3 уникальных числа")
#else:
#    print(f"Пароль для {username} прошел все проверки")
#print("Привет!")                                                     # строка сработает в любом случае, т.к. блок if закончен (определяется по отступам) 


# С циклом while
# 
# while (
#     len(password) < 8 or username.lower() in password.lower()
#     or len(set("0123456789") & set(password)) < 3
# ):                    
#     print(f"Пароль для {username} не прошел все проверки")
#     password = input("Введите пароль еще раз: ")
# 
# print(f"Пароль для {username} прошел все проверки")


# С циклом while еще один вариант более красивый

password_correct = False        # заводим спец. переменную

while not password_correct:
    if len(password) < 8:
        print("Пароль слишком короткий")
        password = input("Введите пароль еще раз: ")
    elif username.lower() in password.lower():      
        print("Пароль содержит имя пользователя")
        password = input("Введите пароль еще раз: ")
    elif len(set("0123456789") & set(password)) < 3:               
        print("В пароле должны быть как минимум 3 уникальных числа")
        password = input("Введите пароль еще раз: ")
    else:
        print(f"Пароль для {username} прошел все проверки")
        password_correct = True                                 # присваем переменной true чтобы выйти из цикла , так как все проверки пройдены