import login
import interface

def main():
    if login.Authorization.login_menu():
        while True:
            interface.UserInterface.menu()

if __name__ == '__main__':
    main()