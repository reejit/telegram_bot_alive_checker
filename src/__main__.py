import json
import logging
import os

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
    data = json.loads(body)
    logging.info(data['username'])
    chat = await client.get_input_entity(data['username'])
    async with client.conversation(chat) as conv:
        await conv.send_message("/start")
        answer = await conv.get_response()
        if answer.raw_text:
            return web.Response(status=200)
        else:
            return web.Response(status=400)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('start application')

    client.connect()
    client.start(phone=telephone)
    app = web.Application()
    app.add_routes([web.post('/', handle_post)])
    web.run_app(app)
    client.disconnect()
