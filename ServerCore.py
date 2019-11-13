# -*- coding: utf-8 -*-
import asyncio

encoding = "utf-8"


class AsyncServer:
    def __init__(self, handler, host, port):
        self.host = host
        self.port = port
        self.handler = handler
        asyncio.run(self.run_server(self.host, self.port))

    async def run_server(self, host, port):
        server = await asyncio.start_server(self.serve_client, host, port)
        await server.serve_forever()

    async def serve_client(self, reader, writer):
        print('Client connected')
        while reader:
            try:
                request = await self.read_request(reader)
            except ConnectionResetError:
                request = None
                break
            if request is None:
                print('Client unexpectedly disconnected')
                break
            else:
                response = await self.handle_request(request)
                await self.write_response(writer, request, response)

    async def read_request(self, reader):
        request = bytearray()
        chunk = ""
        while chunk is not None:
            chunk = await reader.read(1024)
            request += chunk
            print(f"Client says: {str(request, encoding=encoding)}")
            if not chunk:
                break
            if request:
                return request

    async def handle_request(self, request):
        result = self.handler(request)
        return result

    async def write_response(self, writer, request, response):
        global encoding
        response = bytes(response, encoding=encoding)
        writer.write(response)
        await writer.drain()
        # writer.close()
        print(f'Request {request} has been served')


if __name__ == '__main__':
    serv = AsyncServer(host='localhost', port=7777, handler=print)
