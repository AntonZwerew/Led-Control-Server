class Command:
    def __init__(self, name, command, caption, valid_args, args_check_func):
        self.name = name
        self.command = command
        self.caption = caption
        self.valid_args = valid_args
        self.args_check_func = args_check_func

    def check_args_valid(self, *args):
        if len(args) != len(self.valid_args):
            raise KeyError("Wrong number of arguments")  # TODO лишний пробел в конце распознается как аргумент
            # обрезать пробел когда приезжает пакет нельзя
            # т.к. может передаваться текстовая строка,
            # оканчивающаяся пробелом
        if self.args_check_func(self.valid_args, args):
            return True
        else:
            raise ValueError("Wrong argument")

    def run(self, *args):
        self.check_args_valid(*args)
        return self.command(*args)
