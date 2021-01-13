import json
import logging
import os
from json.decoder import JSONDecodeError

from aiohttp import web
from telethon.sync import TelegramClient


def str2bool(boolean_string):
    return boolean_string.lower() in ("yes", "true", "t", "1")


api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
debug = str2bool(os.getenv('DEBUG'))
client = TelegramClient('alex', api_id, api_hash)


async def handle_post(request):
    body = await request.text()
    if not body:
        return web.Response(status=422, body='emtpy body')
    try:
        data = json.loads(body)
        result = await handle(data['username'])
    except JSONDecodeError:
        return web.Response(status=422, body='invalid json')
    except KeyError:
        return web.Response(status=422, body='mission required param username')

    if result:
        return web.Response(status=200, body='ok')
    else:
        return web.Response(status=400, body='bot offline')


async def handle_get(request):
    try:
        username = request.query['username']
    except KeyError:
        return web.Response(status=422, body='mission required param username')
    if not username:
        return web.Response(status=422, body='username param can not be empty')
    result = await handle(username)
    if result:
        return web.Response(status=200, body='ok')
    else:
        return web.Response(status=400, body='bot offline')


async def handle(username):
    logging.info(username)
    chat = await client.get_input_entity(username)
    async with client.conversation(chat) as conv:
        await conv.send_message("/ping")
        answer = await conv.get_response()
        return bool(answer.raw_text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('start application')

    client.connect()
    client.start(phone=telephone)
    app = web.Application()
    app.add_routes([web.post('/', handle_post),
                    web.get('/', handle_get)])
    web.run_app(app, port=8080)
    client.disconnect()
