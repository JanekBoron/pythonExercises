import pyodbc
from datetime import datetime
import random
import string

SERVER = 'localhost'
DATABASE = 'Banking_App'
USERNAME = 'sa'
PASSWORD = ''
DRIVER = 'ODBC Driver 17 for SQL Server'

CONNECTION_STRING = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"


def create_db_users_table():

    try:
        conn =  pyodbc.connect(CONNECTION_STRING)
        cursor =  conn.cursor()
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users')
            CREATE TABLE users (
                login NVARCHAR(100) PRIMARY KEY,
                password NVARCHAR(100),
                account_number NVARCHAR(100),
                balance FLOAT,
                transactions NVARCHAR(200)
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Błąd przy tworzeniu tabeli users: {e}")
    finally:
        conn.close()



def add_user_to_table(login, password, account_number, starting_balance):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (login, password, account_number, balance, transactions) VALUES (?, ?, ?, ?, ?)",
                       ( login, password, account_number, starting_balance, "[]" ) )
        conn.commit()
    except Exception as e:
        print(f"Błąd przy dodawaniu użytkownika do tabeli users: {e}")
    finally:
        conn.close()



def get_user_info(login):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute( "SELECT * FROM users WHERE login=?", (login,))
        user_row = cursor.fetchone()
    except Exception as e:
        print(f"Błąd pobierania informacji o użytkowniku: {e}")
        user_row = None
    finally:
        conn.close()
    return user_row


def update_user(login, balance, transactions):
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance=?, transactions=? WHERE login=?", (balance, transactions, login))
        conn.commit()
    except Exception as e:
        print(f"Błąd przy aktualizacji salda użytkownika: {e}")
    finally:
        conn.close()


def authenticate(login, password):
    user = get_user_info(login)
    if user and user[1] == password: 
        return login 
    return None


def generate_account_number():
    return ''.join(random.choices(string.digits, k=26))


def create_user():
    login = input("Podaj login: ")
    password = input("Podaj hasło: ")
    starting_balance = float(input("Wpłać pieniądze: "))
    
    if get_user_info(login):
        print("Taki login już istnieje")
        return False, None, None
    
    account_number = generate_account_number()
    add_user_to_table(login, password, account_number, starting_balance)
    print(f"Udało ci się stworzyć konto oto jego numer: {account_number}")
    return True, login, password


def show_users():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT login, account_number, balance FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"Użytkownik: {user[0]}, Numer konta: {user[1]}, Saldo: {user[2]} zł")
    except Exception as e:
        print(f"Błąd wyświetlania użytkowników: {e}")
    finally:
        conn.close()


def check_balance(logged_in_user):
    user = get_user_info(logged_in_user)
    print(f"Twój stan konta to: {user[3]} zł")


def transfer_funds(logged_in_user):
    from_user = get_user_info(logged_in_user)
    to_account = input("Podaj numer konta do przelewu: ")
    amount = float(input("Podaj kwotę którą chcesz przelać: "))
    title = input("Podaj tytuł przelewu: ")

    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE account_number=?", (to_account,))
        to_user_row = cursor.fetchone()
        to_user = to_user_row if to_user_row else None
    except Exception as e:
        print(f"Błąd przy transferze funduszy: {e}")
        return
    finally:
        conn.close()

    if not to_user:
        print("Takie konto nie istnieje.")
        return

    if from_user[2] == to_account:  
        print("Nie można wykonać przelewu na to samo konto!")
        return

    if from_user[3] < amount:  
        print("Niewystarczające środki.")
        return
    
    from_balance = from_user[3] - amount
    to_balance = to_user[3] + amount

    transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    from_transactions = eval(from_user[4]) 
    to_transactions = eval(to_user[4])  


    from_transactions.append({
        'type': 'outgoing',
        'amount': amount,
        'to_account': to_account,
        'title': title,
        'date': transaction_date
    })
    
    to_transactions.append({
        'type': 'incoming',
        'amount':  amount,
        'from_account': from_user[2],
        'title': title,
        'date': transaction_date
    })


    update_user(logged_in_user, from_balance, str(from_transactions))
    update_user(to_user[0], to_balance, str(to_transactions))  
    print("Przelew zlecony!")


def view_transactions(logged_in_user):
    user = get_user_info(logged_in_user)
    if user:
        transactions = eval(user[4]) 
        if not transactions:
            print("Brak transakcji do wyświetlenia.")
            return
        
        start_date = input("Podaj datę początkową w formacie YYYY-MM-DD lub naciśnij Enter, aby pominąć: ")
        end_date = input("Podaj datę końcową w formacie YYYY-MM-DD lub naciśnij Enter, aby pominąć: ")

        dated_transactions =  transactions

        if start_date:
            dated_transactions = [t for t in dated_transactions if t['date'] >= start_date]
        if end_date:
            dated_transactions = [t for t in dated_transactions if t['date'] <= end_date]

        for t in dated_transactions:
            if t['type'] == 'outgoing':
                print(f"Data: {t['date']}, Tytuł: {t['title']}, Wysłane: {t['amount']} do konta: {t['to_account']}")
            elif t['type'] == 'incoming':
                print(f"Data: {t['date']}, Tytuł: {t['title']}, Otrzymane: {t['amount']} od konta: {t['from_account']}")
    else:
        print("Nie ma takiego użytkownika!")

def main_menu(logged_in_user):
    while True:
        print("1. Wyświetl użytkowników")
        print("2. Wykonaj przelew")
        print("3. Wyświetl historię transakcji")
        print("4. Sprawdź stan konta")
        print("5. Wyloguj się")

        choice = input("Wpisz którą opcję wybierasz: ")
        
        if choice == '1':
            show_users()
        elif choice == '2':
            transfer_funds( logged_in_user)
        elif choice == '3':
            view_transactions(logged_in_user)
        elif choice == '4':
            check_balance(logged_in_user)
        elif choice == '5':
            break
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")

def main():
    create_db_users_table()
    print("\nWitaj w konsolowej aplikacji bankowej! ")
    while True:
        logged_in_user = None
        
        while not logged_in_user:
            print("1. Zaloguj się")
            print("2. Zarejestruj się")
            choice = input("Wpisz którą opcję wybierasz: ")
            
            if choice == '1':
                login =  input("Podaj login: ")
                password = input("Podaj hasło: ")
                logged_in_user = authenticate(login, password)
                if not logged_in_user:
                    print("Niepoprawna login lub hasło.")
            elif choice == '2':
                success, login, password = create_user()
                if success:
                    logged_in_user = authenticate(login, password)
            else:
                print("Niepoprawny wybór. Spróbuj ponownie.")
        
        main_menu(logged_in_user)

if __name__ == "__main__":
    main()