import pymysql.cursors
import os
uid=0
uN=""
ulog=""
os.system('cls')
autorization = False
while True:
    os.system('cls')
    while True:
        connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                database='bb_beliaev',
                                cursorclass=pymysql.cursors.DictCursor)
        a = int(input("\n Добро пожаловать в приложение банка ВаБанк. \n Для дальнейших манипуляций вам необходимо войти в аккаунт. \n \n Нажмите: \n 1 - Чтобы создать аккаунт в системе. \n 2 - Чтобы войти в систему. \n 3 - Чтобы выйти из приложения \n\n > "))
        if a == 1:
            os.system('cls')
            Fname = input("Введите ваше имя > ")
            LName = input("Введите вашу фамилию > ")
            Login = input("Введите желаемый логин > ")
            Pass = input("Введите желаемый пароль > ")
            Age = int(input("Укажите ваш возраст > "))
            Phone = input("Укажите ваш номер телефона > ")
            if Age >= 18:
                with connection:
                    with connection.cursor() as cursor:
                        att = f"SELECT * FROM `users` WHERE Login = '{Login}'"
                        cursor.execute(att)
                        results = cursor.fetchall()
                        while (len(results) == 1):
                            print("Данный логин уже занят. Попробуйте снова. \n")
                            Login = input("Введите желаемый логин > ")
                            att = f"SELECT * FROM `users` WHERE Login = '{Login}'"
                            cursor.execute(att)
                            results = cursor.fetchall()    
                        agg = f"SELECT * FROM `users` WHERE Phone = '{Phone}'"
                        cursor.execute(agg)
                        phones = cursor.fetchall()
                        while (len(phones)==1):
                            print("Данный номер телефона уже используется. Попробуйте снова.")
                            Phone = input("Введите номер телефона > ")
                            agg = f"SELECT * FROM 'users' WHERE Phone = '{Phone}'"
                            cursor.execute(agg)
                            phones = cursor.fetchall()
                        sql = "INSERT INTO `users`(`UserID`, `FName`, `LName`, `Login` , `Pass` , `Age`, `Phone`) VALUES ('',%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (Fname,LName,Login,Pass,Age,Phone))
                        connection.commit()
                        os.system('cls')
                        print("\n                Регистрация прошла успешно.\n                       Спасибо.")
            else:
                print("Вам должно быть не менее 18 лет, чтобы зарегистрироваться.")



        elif a == 2:
            os.system('cls')
            Login = input("Введите логин для входа в систему > ")
            Pass = input("Введите пароль > ")
            with connection:
                with connection.cursor() as cursor:
                    sql = f"SELECT * FROM `users` WHERE Login='{Login}' AND Pass ='{Pass}'"
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    if (len(results) == 0):
                        print("Неверный логин или пароль.")
                    else:
                        os.system('cls')
                        for result in results:
                            print("                     Вы успешно вошли в систему.")
                            uid = result['UserID']
                            uN = result['FName']
                            ulog = result['Login']
                            autorization = True
                        break
        elif a == 3:
            exit()
        else: 
            os.system('cls')
            print("Такой команды не существует!")
        
    while autorization:
            connection = pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            database='bb_beliaev',
                            cursorclass=pymysql.cursors.DictCursor)
            print("                     Добро пожаловать, " , uN)
            b = int(input("Выберите желаемую операцию: \n 1 - Открыть счёт \n 2 - Просмотреть баланс \n 3 - Пополнить счёт \n 4 - Перевести деньги другому человеку \n 5 - Перевести кэшбек на свой баланс \n 9 - Выйти из аккаунта \n 10 - Выйти из приложения \n > "))
            if b == 1:
                os.system('cls')
                Conf = input("Желаете открыть счёт? \n > ")
                if Conf == "Да" or  Conf == "да" or Conf == "ДА" or Conf == "дА":
                    with connection:
                        with connection.cursor() as cursor:
                            sql = f"SELECT `BalanceID` FROM `balances` WHERE UserID='{uid}'"
                            cursor.execute(sql)
                            results = cursor.fetchall()
                            sql = "INSERT INTO `balances` (`BalanceID`,`userID`, `Rub`, `Eur`, `USD`, `Cashback`) VALUES ('',%s,%s,%s,%s,%s)"
                            cursor.execute(sql, (uid, 0, 0, 0, 0))
                            os.system('cls')
                            print("Счёт успешно открыт!")
                            connection.commit()
                else:
                    pass
            
            elif b == 2:
                os.system('cls')
                with connection:
                    with connection.cursor() as cursor:
                        sql = f"SELECT `BalanceID` FROM `balances` WHERE UserID='{uid}'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        if (len(results) != 0):
                            print("Список ваших счетов: ")
                            for result in results:
                                print("Номер счёта: " + str(result['BalanceID']))
                            bal = int(input("\n Выберите счёт, баланс которого желаете просмотреть > "))
                            check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                            cursor.execute(check)
                            ck = cursor.fetchall()
                            while (len(ck) == 0):
                                print("У вас нет счёта с таким айди! Попробуйте снова.")
                                bal = int(input("Введите корректный айди счёта из выданного вам списка > "))
                                check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                                cursor.execute(check)
                                ck = cursor.fetchall()
                            sql = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}'"
                            cursor.execute(sql)
                            cash = cursor.fetchall()
                            os.system('cls')
                            for cash in cash:
                                print(f" Rub: " , float(cash['Rub']))
                                print(f" Eur:  " , float(cash['Eur']))
                                print(f" USD:  ", float(cash['USD']))
                                print(f" Накопленный кэшбек: ", float(cash['Cashback']), "\n")
                        else:
                            print("У вас нет открытых счетов!")
                    connection.commit()

            elif b == 3:
                os.system('cls')
                with connection:
                    with connection.cursor() as cursor:
                        sql = f"SELECT `BalanceID` FROM `balances` WHERE UserID='{uid}'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        if (len(results) != 0):
                            print("Список ваших счетов: ")
                            for result in results:
                                print("Номер счёта: " + str(result['BalanceID']))
                            bal = int(input("\nВыберите счёт, баланс которого желаете пополнить > "))
                            check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                            cursor.execute(check)
                            ck = cursor.fetchall()
                            while (len(ck) == 0):
                                print("У вас нет счёта с таким айди! Попробуйте снова.")
                                bal = int(input("Введите корректный айди счёта из выданного вам списка > "))
                                check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                                cursor.execute(check)
                                ck = cursor.fetchall()
                            curr = float(input("Какую сумму вы желаете внести? \n > "))
                            while (curr < 0):
                                print("Нельзя пополнить счёт на отрицательную сумму!")
                                curr = float(input("Введите желаемую сумму > \n > "))
                            upd = f"UPDATE `balances` SET `Rub` = 'Rub' + '{curr}', `Eur` = `Eur` +'{curr}'/80, `USD` = `USD` + '{curr}'/75 WHERE `BalanceID` = '{bal}'"
                            cursor.execute(upd)
                            connection.commit()
                            os.system('cls')
                            print("                 Операция прошла успешно!")
                        else:
                            print("У вас нет открытых счетов в банке!")
            elif b == 4:
                os.system('cls')
                with connection:
                    with connection.cursor() as cursor:
                        sql = f"SELECT `BalanceID` FROM `balances` WHERE UserID='{uid}'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        if (len(results) != 0):
                            print("Список ваших счетов: ")
                            for result in results:
                                print("Номер счёта: " + str(result['BalanceID']))
                            bal = int(input("\nВыберите счёт, с которого желаете перевести средства > "))
                            Lsend = input("Введите логин человека, которому желаете отправить средства > ")
                            while (Lsend==ulog):
                                print("Нельзя отправить средства самому себе. Попробуйте снова")
                                Lsend = input("Введите желаемый логин > ")
                            att = f"SELECT * FROM `users` WHERE Login = '{Lsend}'"
                            cursor.execute(att)
                            results = cursor.fetchall()
                            while (len(results) == 0):
                                print("Данный пользователь не существует. Попробуйте снова. \n")
                                Lsend = input("Введите желаемый логин > ")
                                att = f"SELECT * FROM `users` WHERE Login = '{Lsend}'"
                                cursor.execute(att)
                                results = cursor.fetchall()       
                            sql2 = f"SELECT `UserID` FROM `users` WHERE Login='{Lsend}'"
                            cursor.execute(sql2)
                            rr = cursor.fetchall()
                            for rr in rr:
                                rec = int(rr['UserID'])
                            scam = f"SELECT * FROM `balances` WHERE UserID = '{rec}'"
                            cursor.execute(scam)
                            sc = cursor.fetchall()
                            if (len(sc) == 0):
                                print("У пользователя нет открытых счетов.")
                            else:
                                os.system('cls')
                                print("\nСписок счетов пользователя " + Lsend + ".")
                                for sc in sc:
                                    print("Номер счёта: " , int(sc['BalanceID']))
                                bad = int(input("\nВыберите счёт пользователя " + Lsend + " на который желаете перевести средства > "))
                                check = f"SELECT * FROM `balances` WHERE BalanceID = '{bad}' AND UserID = '{rec}'"
                                cursor.execute(check)
                                ck = cursor.fetchall()
                                while (len(ck) == 0):
                                    print("У пользователя нет счёта с таким айди! Попробуйте снова.")
                                    bad = int(input("Введите корректный айди счёта из выданного вам списка > "))
                                    check = f"SELECT * FROM `balances` WHERE BalanceID = '{bad}' AND UserID = '{rec}'"
                                    cursor.execute(check)
                                    ck = cursor.fetchall()

                                value = float(input("Введите желаемую для перевода сумму > "))
                                sql3 = f"SELECT Rub FROM balances WHERE BalanceID = '{bal}'"
                                cursor.execute(sql3)
                                result = cursor.fetchall()
                                for result in result:
                                    com = float(result['Rub'])
                                while (com < value):
                                    print("На вашем счету недостаточно средств! Введите другую сумму.")
                                    value = float(input("Введите сумму для перевода > "))
                                while (value < 0):
                                    print("Нельзя перевести отрицательную сумму!")
                                    value = float(input("Введите сумму для перевода > \n > "))
                                scam2 = f"UPDATE `balances` SET `Rub` = `Rub` + '{value}' , `Eur` = `Eur` + '{value}'/80, `USD` = `USD` + '{value}'/75 WHERE `BalanceID` = '{bad}'"
                                cursor.execute(scam2)
                                scam3 = f"UPDATE `balances` SET `Rub` = `Rub` - '{value}' , `Eur` = `Eur` - '{value}'/80, `USD` = `USD` - '{value}'/75 , `Cashback` = `Cashback` + '{value}'/100 WHERE `BalanceID` = '{uid}'"
                                cursor.execute(scam3)
                                os.system('cls')
                                print("Операция прошла успешно! Вам было начислено " , value/100 , " рублей кешбека.")
                                connection.commit()
                        else:
                            print("У вас нет открытых счетов в банке!")
            elif b == 5: 
                with connection:
                    with connection.cursor() as cursor:
                        sql = f"SELECT `BalanceID` FROM `balances` WHERE UserID='{uid}'"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        if (len(results) != 0):
                            os.system('cls')
                            print("Список ваших счетов: ")
                            for result in results:
                                print("Номер счёта: " + str(result['BalanceID']))
                            bal = int(input("\nВыберите счёт с которого желаете списать кешбек > "))
                            check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                            cursor.execute(check)
                            ck = cursor.fetchall()
                            while (len(ck) == 0):
                                print("У вас нет счёта с таким айди! Попробуйте снова.")
                                bal = int(input("Введите корректный айди счёта из выданного вам списка > "))
                                check = f"SELECT * FROM `balances` WHERE BalanceID = '{bal}' AND UserID = '{uid}'"
                                cursor.execute(check)
                                ck = cursor.fetchall()
                            os.system('cls')
                            for ck in ck:
                                print(f"Накопленный кешбек на вашем счёт: " + str(ck['Cashback']))
                            Conf = input("Желаете перевести накопленный кешбек на свой счёт? \n > ")
                            if Conf == "Да" or  Conf == "да" or Conf == "ДА" or Conf == "дА":
                                cback = float(ck['Cashback'])
                                sql = f"UPDATE `balances` SET `Rub` = `Rub` + '{cback}', `Eur` = `Eur` + '{cback}'/80 , `USD` = `USD` + '{cback}'/75, `Cashback` = '0' WHERE BalanceID = '{bal}'"
                                os.system('cls')
                                print("Операция прошла успешно!")
                                cursor.execute(sql)
                                connection.commit()
                            else:
                                break
                        else:
                            os.system('cls')
                            print("У вас нет открытых счетов в банке!")
            elif b == 9:
                autorization = False
            elif b == 10:
                exit()



                        
                        



                    

                        




    

    
            