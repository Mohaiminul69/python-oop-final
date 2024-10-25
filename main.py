from create_account import create_account
from login import login

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
