from interfaces import interface, login_interface


def main():
    while True:
        if login_interface.Authorization.login_menu():
            interface.UserInterface.menu()

if __name__ == '__main__':
    main()