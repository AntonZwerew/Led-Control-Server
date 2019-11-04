# -*- coding: utf-8 -*-

ok_answer = "OK"
fail_answer = "FAIL"
encoding = "utf-8"


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


class CameraCommands(object):

    def __init__(self, camera):
        self.camera = camera
        self.last_operation_successful = None
        self.device_commands = {
            u"set-led-state": self.set_led_state,  # set­led­state  on, off OK, FAILED включить/выключить LED
            u"get-led-state": self.get_led_state,  # get­led­state OK on|off, FAILED запросить состояние LED
            u"set-led-color": self.set_led_color,  # set­led­color red, green, blue OK, FAILED изменить цвет LED
            u"get-led-color": self.get_led_color,  # get­led­color OK red|green|blue, FAILED запросить цвет LED
            u"set-led-rate": self.set_led_rate,  # set­led­rate 0..5 OK, FAILED изменить частоту мерцания LED
            u"get-led-rate": self.get_led_rate,  # get­led­rate OK 0..5, FAILED запросить частоту ме"
        }
        self.service_commands = {
            u"show-commands": self.get_avalible_commands,
        }

    def operation_state(func):
        def _wrapper(*args, **kwargs):
            self = args[0]
            try:
                result = func(*args, **kwargs)
                self.last_operation_successful = True
            except Exception:
                self.last_operation_successful = False
                result = None
            return result
        return _wrapper


    # TODO get_command_params
    def get_avalible_commands(self):
        ans = ""
        ans += "Service commands: "
        for command in self.service_commands:
            ans += command + ", "
        ans += "Device commands: "
        for command in self.device_commands:
            ans += command + ", "
        self.last_operation_successful = True
        return ans[:-2]

    def run_request_get_response(self, request):
        text_command, args = self.parse_command_args(request)
        command = self.get_command_by_request(text_command)
        if command is None:
            help_command_name = str(get_key(self.service_commands, self.get_avalible_commands))
            result = f"Unknown command, use {help_command_name} for list of commands"  # TODO unknown argument
        else:
            result = command(*args)
        response = self.get_answer()
        if result is not None:
            response += " " + str(result)
        return response + "\n"

    def get_answer(self):
        global ok_answer
        global fail_answer
        if self.last_operation_successful:
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
        commands = {**self.service_commands, **self.service_commands}
        for server_command in commands:
            if request == server_command:  # TODO request может приехать в другой кодировке
                command = commands.get(request)
                break
            if command is None:
                self.last_operation_successful = False
        return command

    @operation_state
    def set_led_state(self, state):
        if state not in (["on", "off"]):
            raise Exception
        self.camera.LED.state = state

    @operation_state
    def get_led_state(self):
        result = self.camera.LED.state
        if result is not None:
            return self.camera.LED.state
        else:
            raise Exception

    @operation_state
    def set_led_color(self, color):
        if color not in (["red", "green", "blue"]):
            raise Exception
        self.camera.LED.color = color

    @operation_state
    def get_led_color(self):
        result = self.camera.LED.color
        if result is not None:
            return result
        else:
            raise Exception

    @operation_state
    def set_led_rate(self, rate):
        _rate = int(rate)
        if _rate not in (range(0, 6)):
            raise Exception
        self.camera.LED.rate = _rate

    @operation_state
    def get_led_rate(self):
        result = self.camera.LED.rate
        if result is not None:
            return result
        else:
            raise Exception


if __name__ == "__main__":
    cam_commands = CameraCommands()
    """
    cam_commands.set_led_state("on")
    print(cam_commands.get_led_state())
    print(cam_commands.last_operation_state)
    print(cam_commands.run("set­led­state on"))
    print(cam_commands.run("get-led-state"))
    """
