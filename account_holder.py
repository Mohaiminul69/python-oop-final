from users import User
from bank import rich_bank
from datetime import datetime
from current_time import current_time


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
