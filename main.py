from abc import ABC
from datetime import datetime


def current_time():
    date_str = f"{datetime.now()}"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    formatted_date = date_obj.strftime("%d %b %Y, %I:%M %p")
    return formatted_date


class User(ABC):
    def __init__(self, name, email, address, password):
        self.name = name
        self.email = email
        self.address = address
        self.password = password


class AccountHolder(User):
    def __init__(self, name, email, address, account_type, password):
        super().__init__(name, email, address, password)
        self.account_type = account_type
        self.balance = 0
        self.history = []
        self.available_loan = 2
        self.loan_amount = 0
        self.account_number = f"{datetime.now().year}" + (
            f"{rich_bank.total_accounts_till_now + 1:04}"
        )
        rich_bank.add_account(self)

    def make_deposit(self, deposit_amount):
        self.balance += deposit_amount
        rich_bank.increase_balance(deposit_amount)
        statement = f"${deposit_amount} has been deposited on {current_time()}"
        self.history.append(statement)
        print(
            f"\n --- ${deposit_amount} has been deposited to your account ---\n --- Current balance is ${self.balance} ---\n"
        )

    def make_withdraw(self, withdraw_amount):
        self.balance -= withdraw_amount
        if not self.loan_amount:
            rich_bank.decrease_balance(withdraw_amount)
        statement = f"${withdraw_amount} has been withdrawn on {current_time()}"
        self.history.append(statement)
        print(
            f"\n --- ${withdraw_amount} has been withdrawn from your account ---\n --- Current balance is ${self.balance} ---\n"
        )

    def take_loan(self, amount):
        rich_bank.give_loan(amount)
        statement = f"${amount} has been taken as loan on {current_time()}"
        self.history.append(statement)
        self.balance += amount
        self.available_loan -= 1
        self.loan_amount += amount
        print(
            f"\n --- ${amount} has been transfered to your account as loan ---\n --- You can take loan up to {self.available_loan} more time ---\n"
        )

    def get_transaction_history(self):
        print("\n --- Your Transaction History ---\n")
        for statement in self.history:
            print(f" - {statement}")
        print("")

    def check_balance(self):
        print(self.balance)

    def __repr__(self):
        return f"\n- An account has been created with the name of {self.name}\n- Account number: {self.account_number}\n- Account type: {self.account_type} account\n* Make sure to remember the ACCOUNT NUMBER and PASSWORD to login\n"


class Admin(User):
    def __init__(self, name, email, address, password):
        super().__init__(name, email, address, password)
        self.admin_id = f"{rich_bank.total_admins + 1:04}"
        rich_bank.add_admin(self)

    def get_users_list(self):
        rich_bank.see_account_holders_list()

    def get_total_balance_of_bank(self):
        return rich_bank.balance

    def get_total_loan_amount(self):
        rich_bank.see_total_loan_amount()

    def change_loan_state(self, state):
        rich_bank.is_loanable = state

    def change_bank_state(self, state):
        rich_bank.is_bankrupt = state

    def __repr__(self):
        return f"\n- An admin has been created with the name of {self.name}\n- Admin Id: {self.admin_id}\n* Make sure to remember the ADMIN ID and PASSWORD to login"


class Bank:
    def __init__(self):
        self.accounts = []
        self.admins = []
        self.__balance = 70000
        self.__total_accounts_till_now = 0
        self.__is_loanable = True
        self.__total_loan_taken = 0
        self.__is_bankrupt = False

    def add_account(self, account):
        self.__total_accounts_till_now += 1
        self.accounts.append(account)

    def delete_account(self, account):
        if account.loan_amount:
            if account.loan_amount > account.balance:
                self.__balance += account.balance
                self.__total_loan_taken -= account.balance
                remaining_loan = account.loan_amount - account.balance
                print(
                    f"\n *** Account of {account.name} with account number {account.account_number} has been deleted successfully ***\n *** And ${account.balance} has been returned to the bank ***\n *** And $0 has been returned to the account holder ***\n *** Remaining loan amount of ${remaining_loan} is still owed to the bank ***\n"
                )
            else:
                self.__balance += account.loan_amount
                self.__total_loan_taken -= account.loan_amount
                account.balance -= account.loan_amount
                print(
                    f"\n *** Account of {account.name} with account number {account.account_number} has been deleted successfully ***\n *** And ${account.loan_amount} has been returned to the bank ***\n *** And ${account.balance} has been returned to the account holder ***\n"
                )
                self.__balance -= account.balance
        else:
            self.__balance -= account.balance
            print(
                f"\n *** Account of {account.name} with account number {account.account_number} has been deleted successfully ***\n *** And ${account.balance} has been returned to the account holder ***\n"
            )

        updated_accounts = list(
            filter(lambda x: x.account_number != account.account_number, self.accounts)
        )
        self.accounts = updated_accounts

    def make_transfer(self, user_account, beneficiary_account, amount):
        user_account.balance -= amount
        beneficiary_account.balance += amount
        print(
            f"\n --- ${amount} has been transfered to {beneficiary_account.name}, account number: {beneficiary_account.account_number} ---\n --- Your current balance is {user_account.balance} ---\n"
        )

    def give_loan(self, amount):
        self.__total_loan_taken += amount
        self.__balance -= amount

    def add_admin(self, account):
        self.admins.append(account)

    def find_account(self, account_number):
        for acc_num in self.accounts:
            if account_number == acc_num.account_number:
                return acc_num
        return None

    def find_admin(self, admin_id):
        for admin in self.admins:
            if admin_id == admin.admin_id:
                return admin
        return None

    def see_account_holders_list(self):
        print("\n --- List of Account Holders ---\n")
        print(f" #\tName\tAccount Number\tBalance\tLoan Taken")
        for idx, account in enumerate(self.accounts):
            print(
                f" {idx+1}\t{account.name}\t{account.account_number}\t{account.balance}\t{account.loan_amount}"
            )
        print("")

    def see_total_loan_amount(self):
        print(f"\n --- Total Loan Taken from Bank: ${self.__total_loan_taken} ---\n")

    @property
    def balance(self):
        return self.__balance

    def increase_balance(self, amount):
        self.__balance += amount

    def decrease_balance(self, amount):
        self.__balance -= amount

    @property
    def is_loanable(self):
        return self.__is_loanable

    @is_loanable.setter
    def is_loanable(self, state):
        self.__is_loanable = state
        if state:
            print(
                "\n *** The bank is going to give loan to account holders from now on ***\n"
            )
        else:
            print(
                "\n *** The bank is not going to give loan to account holders from now on ***\n"
            )

    @property
    def is_bankrupt(self):
        return self.__is_bankrupt

    @is_bankrupt.setter
    def is_bankrupt(self, state):
        self.__is_bankrupt = state
        if state:
            print("\n *** The bank is bankrupt ***\n")
        else:
            print("\n *** The bank is not bankrupt anymore ***\n")

    @property
    def total_accounts_till_now(self):
        return self.__total_accounts_till_now

    @property
    def total_admins(self):
        return len(self.admins)


rich_bank = Bank()


def create_account(user_type, is_admin=False):
    name = input(
        "\nEnter account holder's name: " if is_admin else "\nEnter your name: "
    )
    email = input(
        "Enter account holder's email: " if is_admin else "Enter your email: "
    )
    address = input(
        "Enter account holder's address: " if is_admin else "Enter your address: "
    )
    password = input("Enter a password: ")
    while len(password) == 0:
        print("\n --- Password cannot be of length 0 ---\n")
        password = input("Enter a password: ")

    confirmPassword = input("Confirm password: ")

    while password != confirmPassword:
        print("\n --- Password did not match ---\n --- Please re enter password ---\n")
        password = input("Enter a password: ")
        confirmPassword = input("Confirm password: ")

    if user_type == "admin":
        account = Admin(name, email, address, password)
        print(account)
    else:
        print(
            "\n --- Please select an account type ---\n\n 1) Savings Account\n 2) Current Account\n"
        )

        account_type = ""
        while True:
            account_option = int(input("Choose account type: "))
            if account_option == 1:
                account_type = "savings"
                break
            elif account_option == 2:
                account_type = "current"
                break
            else:
                print("\n --- Invalid option, please choose between 1 and 2. ---\n")

        account = AccountHolder(name, email, address, account_type, password)
        print(account)


def login(user_type):
    if user_type == "admin":
        print("\n --- Please enter your Admin Id and password to login ---\n")
        admin_id = input("Enter your admin id: ")
        admin = rich_bank.find_admin(admin_id)
        if admin == None:
            print(
                "\n --- Admin does not exist ---\n --- Please enter a valid admin id ---"
            )
        else:
            password = input("Enter your password: ")
            while admin.password != password:
                print("\n --- Sorry password did not match ---\n")
                password = input("Enter re enter password: ")
            return admin_menu(admin)
    else:
        print("\n --- Please enter your Account Number and password to login ---\n")
        account = None
        while account == None:
            account_number = input("Enter your account number: ")
            if account_number == "0":
                break
            account = rich_bank.find_account(account_number)
            if account == None:
                print(
                    "\n *** Account does not exist ***\n *** Please enter a valid account number, or enter 0 to go back ***\n"
                )
                continue
            else:
                password = input("Enter your password: ")
                while account.password != password:
                    print("\n --- Sorry password did not match ---\n")
                    password = input("Enter re enter password: ")
                return user_menu(account)


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


print("")
while True:
    print(" --- Select from Options ---\n\n1) Create an account\n2) Login\n3) Exit\n")

    option = int(input("Please Choose an Option: "))

    if option == 1:
        while True:
            print(
                "\n --- Select from Options ---\n\n1) Create User Account\n2) Create Admin Account\n3) Go to Previous Menu\n"
            )
            option = int(input("Please choose an option: "))
            if option == 1:
                create_account("account_holder")
                break
            elif option == 2:
                create_account("admin")
                break
            elif option == 3:
                break
            else:
                print("\n --- Invalid option, please choose between 1 and 3. ---\n")

    elif option == 2:
        while True:
            print(
                "\n --- Select from Options ---\n\n1) Login as user\n2) Login as admin\n3) Go to Previous Menu\n"
            )
            option = int(input("Please choose an option: "))
            if option == 1:
                login("account_holder")
            elif option == 2:
                login("admin")
            elif option == 3:
                break
            else:
                print("\n --- Invalid option, please choose between 1 and 3. ---\n")

    elif option == 3:
        print("\n --- Thank you for banking with us. ---")
        break

    else:
        print("\n --- Invalid option, please choose between 1 and 3. ---")
