import pyodbc,csv,configparser, datetime, os
#configuration file that can be changed in path file object
config = configparser.ConfigParser()
config.read('userinfo.conf')
#connection to database, bases off your data user info 
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' + f"SERVER={config['USERINFO']['SERVER']};DATABASE={config['USERINFO']['DATABASE']};UID={config['USERINFO']['UID']};PWD={config['USERINFO']['PWD']}")

cursor = connection.cursor()
#method for inserting into ucet
def insert_into_ucet(id_uc,cis_uc,banka_naz,kod_ban):
    cursor.execute(f'set identity_insert [ucet] on')
    cursor.execute(f'''
                    INSERT INTO [ucet] (id,cis_uc,banka_naz,kod_ban)
                    VALUES
                    (?,?,?,?)
                    ''', id_uc,cis_uc,banka_naz,kod_ban)
    connection.commit()
    print("Inserted succesfully")

#method for inserting into zakaznik
def insert_into_zakaznik(id_zak,jmeno,prijmeni,id_uc):
    cursor.execute(f'set identity_insert [zakaznik] on')
    cursor.execute(f'''
                    INSERT INTO [zakaznik] (id,jmeno,prijmeni,id_uc)
                    VALUES
                    (?,?,?,?)
                    ''', id_zak,jmeno,prijmeni,id_uc)
    connection.commit()
    print("Inserted succesfully")    
#method for inserting into vyrobce
def insert_into_vyrobce(id,nazev_vyrobc,sidliste):
    cursor.execute(f'set identity_insert [vyrobce_aut] on')
    cursor.execute(f'''
                    INSERT INTO [vyrobce_aut] (id,nazev_vyrobc,sidliste)
                    VALUES
                    (?,?,?)
                    ''',id,nazev_vyrobc,sidliste)
    connection.commit()
    print("Inserted succesfully")

#method for inserting into auta
def insert_into_auta(id,nazev_znacka,barva,id_vyrob):
    cursor.execute(f'set identity_insert [auta] on')
    cursor.execute(f'''
                    INSERT INTO [auta] (id,nazev_znack,barva,id_vyrob)
                    VALUES
                    (?,?,?,?)
                    ''',id,nazev_znacka,barva,id_vyrob)
    connection.commit()
    print("Inserted succesfully")

#method for inserting into pujcka
def insert_into_pujcka(id,id_zak,id_aut,typ_pujc):
    try:
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(f'set identity_insert [pujcka] on')
        cursor.execute(f'''
                        INSERT INTO [pujcka] (id,datum_pujc,id_zaka,id_aut,typ_pujc)
                        VALUES
                        (?,?,?,?,?)
                        ''',id,now_date,id_zak,id_aut,typ_pujc)
        connection.commit()
        print("Inserted succesfully")
    except:
        print("Constraint error")

#selects data from table with select query request
def select_from_table(table):
    cursor.execute(f'SELECT * FROM {table}')
    for i in cursor:
        print(i)

#method for deletin one row in any table if possible
def delete_item_id(table,id):
    cursor.execute(f'delete from {table} where id = {id}')
    connection.commit()
    select_from_table(table)

#Procedura na vypisovani recent pujcek
def execute_recent_pujcka():
    cursor.execute('exec recent_pujcka')
    for i in cursor:
        print(i)

#export dat z jednotlive tabulky do CSV file
def export_csv(table):
    sql=f"SELECT * from {table}"
    cursor.execute(sql)
    res = cursor.fetchall()
    with open("../bin/export.csv", "w", newline='') as file:
        for row in res:
            if len(row) != 0:
                csv.writer(file).writerow(row)
    print("export succesfull")


#imports csv file into a list 
def import_csv(path):
    try:
        list = []
        with open(path,"r") as file:
            reader = csv.reader(file)
            for row in reader:
                value = str(row)[1:len(str(row))-1]
                print(value)
                list.append(value)
        return list
    except:
        print('Invalid csv expression file')

#method for inserting data to a table imported from a csv file, uses import_csv() method list return
def insert_from_csv(table,list):
    if table == 'ucet':
        for value in list:
            cursor.execute(f'set identity_insert [ucet] on')
            cursor.execute(f'''
                            INSERT INTO [ucet] (id,cis_uc,banka_naz,kod_ban)
                            VALUES
                            ({value})
                            ''')
            connection.commit()
    if table == 'auta':
        for value in list:
            cursor.execute(f'set identity_insert [auta] on')
            cursor.execute(f'''
                    INSERT INTO [auta] (id,nazev_znack,barva,id_vyrob)
                    VALUES
                    ({value})
                    ''')
            connection.commit()
    if table == 'vyrobce_aut':
        for value in list:
            cursor.execute(f'set identity_insert [vyrobce_aut] on')
            cursor.execute(f'''
                        INSERT INTO [vyrobce_aut] (id,nazev_vyrobc,sidliste)
                        VALUES
                        ({value}')
                        ''')
    if table == 'zakaznik':
        for value in list:
            cursor.execute(f'set identity_insert [zakaznik] on')
            cursor.execute(f'''
                        INSERT INTO [zakaznik] (id,jmeno,prijmeni,id_uc)
                        VALUES
                        ({value})
                        ''')
            connection.commit()
    print("Inserted succesfully")  
    connection.commit()

#This transaction allows us to change cars for rent in each individual case
def transaction_pujcka(id1,id2):
    try:
        cursor.execute(f'exec Promena_Aut @id1 = {id1}, @id2 = {id2};')
        connection.commit
    except:
       print("Error")
       connection.rollback()


#This is a terminal method which allows us to communicate with the programme
def terminal_interface():
    end = False
    while end == False:
        print("1. INSERT DATA INTO TABLES")
        print("2. SELECT DATA FROM TABLES")
        print("3. DELETE DATA FROM TABLES")
        print("4. EXPORT TO CSV")
        print("5. IMPORT DATA FROM CSV")
        print("6. EXECUTE LAST PUJCKAS ")
        print("7. EXECUTE TRANSACTION")
        print("8. Exit")
        a = input()
        a = int(a)
        if a == 1:
            print("Name of the table: ")
            name = input()
            if name == 'pujcka':
                print("Insert id of pujcka: ")
                thisid = input()
                print("Insert id of zakaznik: ")
                idzaka = input()
                print("Insert id of auto: ")
                id_aut = input()
                print("Insert typ pujcky: ")
                typeofpujc = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                insert_into_pujcka(thisid,idzaka,id_aut,typeofpujc)
            if name == 'vyrobce_aut':
                print("Insert id of vyrobce: ")
                id_vyrobce = input()
                print("Insert name of vyrobce: ")
                vyrobce = input()
                print("Insert sidliste name: ")
                sidliste = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                insert_into_vyrobce(id_vyrobce,vyrobce,sidliste)
            if name == 'auta':
                print("Insert id of auto: ")
                id_auta = input()
                print("Insert name of auto: ")
                nameofauto = input()
                print("Insert barva: ")
                barva = input()
                print("Insert id of vyrobce: ")
                vyrobce = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                insert_into_auta(id_auta,nameofauto,barva,vyrobce)
            if name == 'ucet':
                print("Insert id of ucet: ")
                id_uct = input()
                print("Insert cislo uctu: ")
                cislouctu = input()
                print("Insert nazev banku: ")
                nameofbank = input()
                print("Insert kod banku: ")
                kodbanku = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                insert_into_ucet(id_uct,cislouctu,nameofbank,kodbanku)
            if name == 'zakaznik':
                print("Insert id of zakaznik: ")
                id_zak = input()
                print("Insert name of zakaznik: ")
                nameofzakaz = input()
                print("Insert surname of zakaznik: ")
                surnameofzakaz = input()
                print("Insert id of ucet: ")
                id_uc = input()
                os.system('cls' if os.name == 'nt' else 'clear')
                insert_into_zakaznik(id_zak,nameofzakaz,surnameofzakaz,id_uc)
        if a == 2:
            print("Please select a table for selecting elements(auta,pujcka,ucet,vyrobce_aut,zakaznik): ")
            choise = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            select_from_table(choise)
        if a == 3:
            print("Please select a table(auta,pujcka,ucet,vyrobce_aut,zakaznik): ")
            table = input()
            print("Please select a row id to be deleted: ")
            idnow = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            delete_item_id(table,idnow)
        if a == 4:
            print("Please select a table to be exported(auta,pujcka,ucet,vyrobce_aut,zakaznik): ")
            table = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            export_csv(table)
        if a == 5:
            print("Please select a table to be inserted into: ")
            table = input()
            print("please type in a path: ")
            path = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            insert_from_csv(table,import_csv(path)) 
        if a == 6:
            execute_recent_pujcka()
            untilexit = input()
            os.system('cls' if os.name == 'nt' else 'clear')
        if a == 7:
            print("Enter first id: ")
            id1 = input()
            print("Enter second id: ")
            id2 = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            transaction_pujcka(id1,id2)
        if a == 8:
            end = True
terminal_interface()
connection.close()