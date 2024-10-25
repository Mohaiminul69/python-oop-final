from bank import rich_bank


def user_menu(user):
    print(f"\n ### Welcome to Rich Bank {user.name} ###\n")
    while True:
        print(
            "--- Please select an options ---\n1) Make a deposit\n2) Make a withdrawal\n3) Check Balance\n4) Check Transaction History\n5) Transfer to another account\n6) Take a Loan\n7) Logout"
        )
        option = int(input("Please Choose an Option: "))

        if option == 1:
            deposit_amount = int(input("\nEnter the amount you want to deposit: "))
            while deposit_amount < 1:
                print("\n *** You cannot deposit less than $1 ***\n")
                deposit_amount = int(input("Enter the amount you want to deposit: "))
            user.make_deposit(deposit_amount)

        elif option == 2:
            withdraw_amount = int(input("\nEnter the amount you want to withdraw: "))
            while withdraw_amount > user.balance:
                print(
                    f"\n *** Withdrawal amount exceeded, You cannot withdraw more than {user.balance} ***\n"
                )
                withdraw_amount = int(input("Enter the amount you want to withdraw: "))
            if rich_bank.is_bankrupt or withdraw_amount > rich_bank.balance:
                print("\n *** We are extremly sorry, the bank is bankrupt. ***\n")
            else:
                user.make_withdraw(withdraw_amount)

        elif option == 3:
            print(
                f"\n --- Current Balance ---\n\n Your available balance is: ${user.balance}\n"
            )

        elif option == 4:
            user.get_transaction_history()

        elif option == 5:
            print("\n --- Please enter Beneficiary's Account Number ---\n")
            while True:
                account_number = input("Enter beneficiary's account number: ")
                if account_number == "0":
                    break
                account = rich_bank.find_account(account_number)
                if account == None:
                    print(
                        "\n --- Account does not exist ---\n --- Please enter a valid account number or enter 0 to go back ---\n"
                    )
                    continue
                if account.account_number == user.account_number:
                    print(
                        "\n --- This is your account number ---\n --- Please enter beneficiary's account number ---\n"
                    )
                    continue
                else:
                    transfer_amount = int(input("Enter transfer amount: "))
                    while transfer_amount > user.balance:
                        print(
                            f"\n *** You cannot transfer more than {user.balance} ***\n"
                        )
                        transfer_amount = int(
                            input("Enter the amount you want to transfer: ")
                        )
                    if rich_bank.is_bankrupt:
                        print(
                            "\n *** The bank has gone bankrupt ***\n *** You cannot make any transaction at the moment ***\n"
                        )
                        break
                    else:
                        rich_bank.make_transfer(user, account, transfer_amount)
                        break

        elif option == 6:
            if rich_bank.is_bankrupt:
                print(
                    "\n *** The bank has gone bankrupt ***\n *** You cannot make any transaction at the moment ***\n"
                )
            else:
                if rich_bank.is_loanable:
                    if user.available_loan:
                        print(
                            f"\n *** You can take up to $10000 as loan at once ***\n *** You can take loan upto {user.available_loan} more time ***\n"
                        )
                        loan_amount = int(
                            input("Enter the amount you want to take as loan: ")
                        )
                        while loan_amount > 10000:
                            print(
                                f"\n *** You cannot take more than $10000 as loan ***\n"
                            )
                            loan_amount = int(
                                input("Enter the amount you want to take as loan: ")
                            )
                        if loan_amount > rich_bank.balance:
                            print(
                                "\n *** We are extremly sorry, the bank is bankrupt. ***\n"
                            )
                        else:
                            user.take_loan(loan_amount)
                    else:
                        print(
                            "\n *** Your available loan quota has been used ***\n *** You can not take any more loans ***\n"
                        )
                else:
                    print(
                        "\n *** The bank is not giving loan at the moment ***\n *** Please try again later ***\n"
                    )

        elif option == 7:
            print("\n --- Thank you for banking with us. ---")
            return

        else:
            print("\n --- Invalid option, please choose between 1 and 3. ---")
