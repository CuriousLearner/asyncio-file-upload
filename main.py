import asyncio


async def handle_file_upload(reader, writer):
    import ipdb; ipdb.set_trace()
    data = b''
    # data = await reader.read(40000000000)
    i = 1
    while not reader.at_eof():
        print("CHUNK", i)
        print(reader.at_eof())
        if reader.at_eof():
            break
        data += await reader.read(1000000)
        i += 1
    print("data")
    print(data)
    # import ipdb; ipdb.set_trace()
    message = data.decode(encoding='ISO-8859-1')
    addr = writer.get_extra_info('peername')
    # print("Received %r from %r" % (message, addr))
    with open('somefile.jpeg', 'w') as f:
        f.write(message)
    # import ipdb; ipdb.set_trace()


    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_file_upload, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Shutting down the server')

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
