import CameraDummy
from Command import Command


class Driver:

    def __init__(self, device):
        self.device = device
        self.last_operation_successful = None

    # TODO переписать
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

    @operation_state
    def set_led_state(self, state):
        self.device.LED.state = state

    @operation_state
    def get_led_state(self):
        result = self.device.LED.state
        if result is not None:
            return result
        else:
            raise Exception

    @operation_state
    def set_led_color(self, color):
        self.device.LED.color = color

    @operation_state
    def get_led_color(self):
        result = self.device.LED.color
        if result is not None:
            return result
        else:
            raise Exception

    @operation_state
    def set_led_rate(self, rate):
        _rate = int(rate)
        self.device.LED.rate = _rate

    @operation_state
    def get_led_rate(self):
        result = self.device.LED.rate
        if result is not None:
            return result
        else:
            raise Exception


if __name__ == "__main__":
    camera = CameraDummy.Camera()
    drv = Driver(camera)
    set_led_state = Command(
        name="set-led-state",
        command=drv.set_led_state,
        caption="",
        valid_args=[["on", "off"], ["asd", "ASD"]],
        args_check_func=print
    )
    camera.LED.rate = 1
    rate = drv.set_led_rate()
    print(rate)
    print(drv.last_operation_state)
