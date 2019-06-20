import asyncio
import aiohttp
import os
from datetime import datetime
from aiohttp import web

async def handle_file_upload(request):
    # reader = aiohttp.MultipartReader.from_req()
    reader = await request.multipart()
    data = await reader.next()
    # import ipdb; ipdb.set_trace()
    filename = data.filename
    content_type = data.headers['Content-Type']
    # form = await data.form(encoding='ISO-8859-1')
    # chunk = await data.read_chunk()
    # import ipdb; ipdb.set_trace()
    file_path = os.path.join('media/', str(datetime.now()) + filename)
    raw_file_data = bytearray()
    while True:
        chunk = await data.read_chunk()
        # print(chunk)
        if chunk == b'':
            break
        raw_file_data += chunk

    with open(file_path, 'wb') as f:
        f.write(raw_file_data)

    return web.Response(text="File uploaded")


if __name__ == '__main__':
    app = web.Application()
    # app.add_routes([web.get('/', handle_file_upload),])

    app.router.add_route('POST', '/', handle_file_upload)
    web.run_app(app)


# async def handle_file_upload(reader, writer):
#     import ipdb; ipdb.set_trace()
#     data = bytearray()
#     # data = await reader.read(40000000000)
#     i = 1
#     while True:
#         print("CHUNK", i)
#         # print(reader.at_eof())
#         # if reader.at_eof():
#         #     break
#         # import ipdb; ipdb.set_trace()
#         chunk = await reader.read(65536)
#         print(len(chunk))
#         if not chunk:
#             # empty chunk signals the end of file
#             break
#         data += chunk
#         i += 1
#     print("data")
#     print(data)
#     # import ipdb; ipdb.set_trace()
#     message = data.decode(encoding='ISO-8859-1')
#     addr = writer.get_extra_info('peername')
#     # print("Received %r from %r" % (message, addr))
#     with open('somefile.jpeg', 'w') as f:
#         f.write(message)
#     # import ipdb; ipdb.set_trace()


#     writer.close()

# loop = asyncio.get_event_loop()
# coro = asyncio.start_server(handle_file_upload, '127.0.0.1', 8888, loop=loop)
# server = loop.run_until_complete(coro)

# # Serve requests until Ctrl+C is pressed
# print('Serving on {}'.format(server.sockets[0].getsockname()))
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     print('Shutting down the server')

# # Close the server
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()
