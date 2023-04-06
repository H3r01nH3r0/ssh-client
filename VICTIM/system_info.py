import platform


class UserSystem:
    def __init__(self):
        victim = platform.uname()
        self.system = f'{victim.system} {victim.release}'
        self.processor = victim.machine
        self.system_version = victim.version
        self.name = victim.node

    def __str__(self):
        output = f'PC:\t\t{self.name}\n' \
                 f'SYS:\t{self.system}\tv.{self.system_version}\n' \
                 f'ARC:\t{self.processor}'
        return output
