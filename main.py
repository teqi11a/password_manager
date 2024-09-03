import login
import interface

def main():
    while True:
        if login.Authorization.login_menu():
            interface.UserInterface.menu()

if __name__ == '__main__':
    main()