from CameraDummy import Camera
from Command import Command
from Driver import Driver


def str_arg_in_array_of_valid(valid_args, args):
    for index, arg in enumerate(args):
        if arg not in valid_args[index]:
            raise ValueError(f"Wrong argument number {index + 1} \"{arg}\" - not in {valid_args[index]}")
    return True


def int_arg_in_valid_range(valid_range, args):
    for index, arg in enumerate(args):
        if int(arg) not in valid_range[index]:
            raise ValueError(f"Wrong argument number {index + 1} \"{arg}\" - not in {valid_range[index]}")
    return True


def no_args(valid_args, args):
    # из функции run класса command передаются valid_args и args,
    # поэтому проверка на отсутствие аргументов принимает их оба.
    # получается лишняя проверка на пустой список допустимых аргументов
    if valid_args:
        return False
    if args:
        return False
    return True


ok_answer = "OK"
fail_answer = "FAIL"
encoding = "utf-8"


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def get_command_by_name(commands, str_command):
    for command in commands:
        if str_command == command.name:
            return command


class ServerCommands(object):

    def __init__(self, drv, device_commands):
        self.drv = drv
        self.device_commands = device_commands
        self.help_command = Command(
            name='get-available-commands',
            command=self.get_available_commands,
            caption="",
            valid_args=[],
            args_check_func=no_args,
        )
        self.get_args_command = Command(
            name="get-args",
            command=self.get_args_by_command,
            caption="",
            valid_args=None,
            args_check_func=str_arg_in_array_of_valid,
        )
        self.service_commands = [
            self.help_command,
            self.get_args_command,
        ]
        self.get_args_command.valid_args = [command.name for command in (self.device_commands + self.service_commands)]

    def get_available_commands(self):
        ans = ""
        ans += "Service commands: "
        for command in self.service_commands:
            ans += command.name + ", "
        ans += "Device commands: "
        for command in self.device_commands:
            ans += command.name + ", "
        return ans[:-2]  # убираем ", "

    def get_args_by_command(self, command):
        result = f"Avalible args of {command}: "
        commands = self.device_commands + self.service_commands
        command = get_command_by_name(commands, command)
        if command:
            if not command.valid_args:
                return result + "None \n"
            for arg in command.valid_args:
                if arg:
                    result += str(arg)
            return result + "\n"
        else:
            return None

    def run_request_get_response(self, request):
        text_command, args = self.parse_command_args(request)
        command = self.get_command_by_request(text_command)
        if command is None:
            result = f"Unknown command, use {self.help_command.name} for list of commands"  # TODO unknown argument
            response = fail_answer
        else:
            try:
                result = command.run(*args)
                response = self.get_answer()
            except Exception as e:
                result = e
                response = fail_answer
        if result is not None:
            response += " " + str(result)
        return response + "\n"

    def get_answer(self):
        global ok_answer
        global fail_answer
        if self.drv.last_operation_successful:  # TODO if wrong argument
            return ok_answer
        else:
            return fail_answer

    def parse_command_args(self, request):
        global encoding
        # print(request)
        request = request.decode(encoding)
        if request.endswith("\n"):  # проверка на корректный конец строки
            request = request[:-1]  # убираем \n
            args = []
            command = request.split(" ")[0]
            for arg in request.split(" ")[1:]:
                args.append(arg)
            return command, args
        else:
            return "", []

    def get_command_by_request(self, request):
        command = None
        commands = (self.service_commands + self.device_commands)
        for server_command in commands:
            if request == server_command.name:  # TODO request может приехать в другой кодировке
                command = get_command_by_name(commands, request)
                break
        return command


if __name__ == "__main__":
    cam = Camera()
    drv = Driver(cam)

