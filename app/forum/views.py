import os
import aiohttp_jinja2
from aiohttp import web, WSMsgType
from datetime import datetime
from app.forum.models import Message

print(os.path.dirname(__file__))
WS_FILE = (os.path.dirname(__file__), 'index.html')


@aiohttp_jinja2.template("index.html")
async def index(_):
    return {"title": "Сервис приема новостей и информирования пользователей"}


class ListMessageView(web.View):
    async def get(self):
        messages = await Message.query.order_by(Message.id.desc()).gino.all()
        messages_data = []
        for message in messages:
            messages_data.append(
                {
                    "id": message.id,
                    "text": message.text,
                    "created": str(message.created),
                },
            )
        return web.json_response(data={"messages": messages_data})


class CreateMessageView(web.View):
    async def post(self):
        data = await self.request.json()
        message = await self.request.app["db"].message.create(
            text=data["text"],
            created=datetime.now(),
        )
        return web.json_response(
            data={
                "message": {
                    "id": message.id,
                    "text": message.text,
                    "created": str(message.created),
                },
            },
        )


class WsConnectView(web.View):
    async def get(self):
        resp = web.WebSocketResponse()
        available = resp.can_prepare(self.request)
        if not available:
            with open(WS_FILE, "rb") as fp:
                return web.Response(body=fp.read(), content_type="text/html")

        await resp.prepare(self.request)

        try:
            print("Someone joined.")
            self.request.app["sockets"].append(resp)

            async for msg in resp:
                if msg.type == web.WSMsgType.TEXT:
                    for ws in self.request.app["sockets"]:
                        if ws is not resp:
                            await ws.send_str(msg.data)
                else:
                    return resp
            return resp

        finally:
            self.request.app["sockets"].remove(resp)
            print("Someone disconnected.")


async def on_shutdown(app: web.Application):
    for ws in app["sockets"]:
        await ws.close()
