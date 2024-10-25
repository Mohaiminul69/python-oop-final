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
