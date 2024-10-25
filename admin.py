from users import User
from bank import rich_bank


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
