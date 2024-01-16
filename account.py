import sqlite3
import random

class Account:
    db_connection = sqlite3.connect('banking_system.db')
    db_cursor = db_connection.cursor()

    def __init__(self, account_number, name, mobile_number, address, password, balance=0):
        self.account_number = account_number
        self.name = name
        self.mobile_number = mobile_number
        self.address = address
        self.password = password
        self.balance = balance

        # Create a table if it doesn't exist
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER,
                transaction_type TEXT,
                amount REAL,
                transaction_date TEXT,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        ''')
        self.db_connection.commit()

        # Create a table if it doesn't exist
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY,
                name TEXT,
                mobile_number TEXT,
                address TEXT,
                password TEXT,
                balance REAL
            )
        ''')
        self.db_connection.commit()

        # Insert account into the database
        self.db_cursor.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)',
                               (account_number, name, mobile_number, address, password, balance))
        self.db_connection.commit()

    @classmethod
    def generate_account_number(cls):
        # Generate a unique 6-digit account number
        return random.randint(100000, 999999)

    @classmethod
    def verify_password(cls, account_number, password):
        cls.db_cursor.execute('''
            SELECT password
            FROM accounts
            WHERE account_number = ?
        ''', (account_number,))
        result = cls.db_cursor.fetchone()
        if result and result[0] == password:
            return True
        else:
            return False

    @classmethod
    def log_transaction(cls, account_number, transaction_type, amount):
        cls.db_cursor.execute('''
            INSERT INTO transactions (account_number, transaction_type, amount, transaction_date)
            VALUES (?, ?, ?, datetime('now'))
        ''', (account_number, transaction_type, amount))
        cls.db_connection.commit()

    @classmethod
    def create_account(cls):
        name = input("Enter your name: ")
        mobile_number = input("Enter your mobile number: ")
        address = input("Enter your address: ")
        password = input("Set your password: ")

        account_number = cls.generate_account_number()
        new_account = cls(account_number, name, mobile_number, address, password)
        print(f"Account created successfully! Account Number: {new_account.account_number}")

    @classmethod
    def deposit(cls):
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")

        if cls.verify_password(account_number, password):
            amount = float(input("Enter the amount to deposit: "))
            cls.db_cursor.execute('''
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_number = ?
            ''', (amount, account_number))
            cls.db_connection.commit()
            cls.log_transaction(account_number, 'Deposit', amount)
            print("Deposit successful!")
        else:
            print("Incorrect password or account not found!")

    @classmethod
    def withdraw(cls):
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")

        if cls.verify_password(account_number, password):
            amount = float(input("Enter the amount to withdraw: "))
            cls.db_cursor.execute('''
                SELECT balance
                FROM accounts
                WHERE account_number = ?
            ''', (account_number,))
            result = cls.db_cursor.fetchone()
            if result:
                balance = result[0]
                if balance >= amount:
                    cls.db_cursor.execute('''
                        UPDATE accounts
                        SET balance = balance - ?
                        WHERE account_number = ?
                    ''', (amount, account_number))
                    cls.db_connection.commit()
                    cls.log_transaction(account_number, 'Withdrawal', amount)
                    print("Withdrawal successful!")
                else:
                    print("Insufficient funds.")
            else:
                print("Account not found!")
        else:
            print("Incorrect password or account not found!")

    @classmethod
    def check_balance(cls):
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")

        if cls.verify_password(account_number, password):
            cls.db_cursor.execute('''
                SELECT balance
                FROM accounts
                WHERE account_number = ?
            ''', (account_number,))
            result = cls.db_cursor.fetchone()
            if result:
                balance = result[0]
                print(f"Account Balance: {balance}")
            else:
                print("Account not found!")
        else:
            print("Incorrect password or account not found!")

    @classmethod
    def get_statement(cls):
        account_number = int(input("Enter your account number: "))
        password = input("Enter your password: ")

        if cls.verify_password(account_number, password):
            cls.db_cursor.execute('''
                SELECT account_number, name, mobile_number, address, balance
                FROM accounts
                WHERE account_number = ?
            ''', (account_number,))
            account_details = cls.db_cursor.fetchone()

            if account_details:
                cls.db_cursor.execute('''
                    SELECT transaction_id, transaction_type, amount, transaction_date
                    FROM transactions
                    WHERE account_number = ?
                ''', (account_number,))
                transactions = cls.db_cursor.fetchall()

                print("\nAccount Details:")
                print("Account Number\tName\t\tMobile Number\tAddress\t\tBalance")
                print("--------------\t----\t\t--------------\t-------\t\t-------")
                print(f"{account_details[0]}\t\t{account_details[1]}\t\t{account_details[2]}\t\t{account_details[3]}\t\t{account_details[4]}")

                if transactions:
                    print("\nTransaction Statement:")
                    print("Transaction ID\tType\t\tAmount\t\tDate")
                    print("--------------\t-----------\t-----------\t-------------------")
                    for transaction in transactions:
                        print(f"{transaction[0]}\t\t{transaction[1]}\t\t{transaction[2]}\t\t{transaction[3]}")
                else:
                    print("No transactions found.")
            else:
                print("Account not found.")
        else:
            print("Incorrect password or account not found!")

    @classmethod
    def transfer_money(cls):
        from_account_number = int(input("Enter your account number: "))
        from_password = input("Enter your password: ")

        if cls.verify_password(from_account_number, from_password):
            to_account_number = int(input("Enter the recipient's account number: "))
            amount = float(input("Enter the amount to transfer: "))

            cls.db_cursor.execute('''
                SELECT balance
                FROM accounts
                WHERE account_number = ?
            ''', (from_account_number,))
            from_balance = cls.db_cursor.fetchone()

            if from_balance and from_balance[0] >= amount:
                cls.db_cursor.execute('''
                    UPDATE accounts
                    SET balance = balance - ?
                    WHERE account_number = ?
                ''', (amount, from_account_number))

                cls.db_cursor.execute('''
                    UPDATE accounts
                    SET balance = balance + ?
                    WHERE account_number = ?
                ''', (amount, to_account_number))

                cls.db_connection.commit()
                cls.log_transaction(from_account_number, 'Transfer to ' + str(to_account_number), amount)
                cls.log_transaction(to_account_number, 'Transfer from ' + str(from_account_number), amount)

                print("Transfer successful!")
            else:
                print("Insufficient funds or invalid account.")
        else:
            print("Incorrect password or account not found!")