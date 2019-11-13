# -*- coding: utf-8 -*-
from ServerCore import AsyncServer
from ServerCommands import *
from Command import Command
from Driver import Driver

host = 'localhost'
port = 7777
cam = Camera()
drv = Driver(cam)

example_command = Command(
    name="command-name-by-protocol",
    command="func_that_exec_when_we_run_this_command",
    caption="caption for help string",
    valid_args=[["array", "of", "valid", "args"]],
    args_check_func="func_that_checks_if_args_in_run_method_is_valid",
)

set_led_state = Command(
    name="set-led-state",
    command=drv.set_led_state,
    caption="sets led state on or off",
    valid_args=[["on", "off"]],
    args_check_func=str_arg_in_array_of_valid,
)
get_led_state = Command(
    name="get-led-state",
    command=drv.get_led_state,
    caption="gets current led stat",
    valid_args=[],
    args_check_func=no_args,
)
set_led_color = Command(
    name="set-led-color",
    command=drv.set_led_color,
    caption="sets led color",
    valid_args=[["red", "green", "blue"]],
    args_check_func=str_arg_in_array_of_valid,
)
get_led_color = Command(
    name="get-led-color",
    command=drv.get_led_color,
    caption="gets led color",
    valid_args=[],
    args_check_func=no_args,
)
set_led_rate = Command(
    name="set-led-rate",
    command=drv.set_led_rate,
    caption="sets led blinking rate",
    valid_args=[range(6)],
    args_check_func=int_arg_in_valid_range,
)
get_led_rate = Command(
    name="get-led-rate",
    command=drv.get_led_rate,
    caption="gets current led blinking rate",
    valid_args=[],
    args_check_func=no_args,
)

device_commands = [
    set_led_state,
    get_led_state,
    set_led_color,
    get_led_color,
    set_led_rate,
    get_led_rate,
]

cam_commands = ServerCommands(drv, device_commands)
# TODO на винде падает клиент при падении сервера
serv = AsyncServer(handler=cam_commands.run_request_get_response, host=host, port=port)
