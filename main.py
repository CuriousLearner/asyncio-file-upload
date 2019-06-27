import asyncio
import aiohttp
import os
from datetime import datetime
from aiohttp import web

async def handle_file_upload(request):
    reader = await request.multipart()
    data = await reader.next()
    filename = data.filename
    content_type = data.headers['Content-Type']
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

    app.router.add_route('POST', '/', handle_file_upload)

    web.run_app(app)
