from create_account import create_account
from bank import rich_bank


def admin_menu(admin):
    print(f"\n ### Welcome to Rich Bank Admin {admin.name} ###\n")
    while True:
        print(
            "--- Please select an options ---\n1) Create an account\n2) Delete an account\n3) See all user accounts\n4) Check total balance of bank\n5) Check total loan amount\n6) Manage bank loan policy\n7) Change bankruptcy state\n8) Logout"
        )
        option = int(input("Please Choose an Option: "))

        if option == 1:
            create_account("account_holder", True)

        elif option == 2:
            print("\n --- Please enter account number you want to delete ---\n")
            account = None
            while account == None:
                account_number = input("Enter your account number: ")
                account = rich_bank.find_account(account_number)
                if account == None:
                    print(
                        "\n --- Account does not exist ---\n --- Please enter a valid account number ---\n"
                    )
                else:
                    rich_bank.delete_account(account)

        elif option == 3:
            admin.get_users_list()

        elif option == 4:
            balance = admin.get_total_balance_of_bank()
            print(f"\n --- Total Balance of Bank: ${balance} ---\n")

        elif option == 5:
            admin.get_total_loan_amount()

        elif option == 6:
            print(
                f"\n --- Please select an option ---\n\n1) Turn on bank loan policy\n2) Turn off bank loan policy\n"
            )
            option = int(input("Please choose an option: "))
            if option == 1:
                admin.change_loan_state(True)
            elif option == 2:
                admin.change_loan_state(False)

        elif option == 7:
            print(
                f"\n --- Please select an option ---\n\n1) Announce bank as bankrupt\n2) Announce bank as not bankrupt\n"
            )
            option = int(input("Please choose an option: "))
            if option == 1:
                admin.change_bank_state(True)
            elif option == 2:
                admin.change_bank_state(False)

        elif option == 8:
            print("\n --- Thank you for banking with us. ---")
            return

        else:
            print("\n --- Invalid option, please choose between 1 and 3. ---")
