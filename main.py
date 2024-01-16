from account import Account

def main():
    print("Welcome to the Console Banking System!")

    while True:
        print("\nOptions:")
        print("1. Create an account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check balance")
        print("5. Get statement")
        print("6. Transfer to other account")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            Account.create_account()
        elif choice == '2':
            Account.deposit()
        elif choice == '3':
            Account.withdraw()
        elif choice == '4':
            Account.check_balance()
        elif choice == '5':
            Account.get_statement()
        elif choice == '6':
            Account.transfer_money()
        elif choice == '7':
            print("Thank you for using the Console Banking System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
