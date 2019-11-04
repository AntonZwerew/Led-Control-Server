# -*- coding: utf-8 -*-
from commands import CameraCommands
from async_server2 import AsyncServer
from CameraDummy import Camera

host = 'localhost'
port = 7777

cam = Camera()
commands = CameraCommands(camera=cam)
serv = AsyncServer(handler=commands.run_request_get_response, host=host, port=port)
