import asyncio
import json

import aio_pika


class RabbitmqClient:

    def __init__(self, app):
        self.app = app

    async def connect(self):
        self.connection = await asyncio.wait_for(
            aio_pika.connect_robust("amqp://admin:123456@localhost/"), timeout=5
        )
        print(self.connection)
        asyncio.create_task(self.listen_for_user_device(app.socket_clients))
        asyncio.create_task(self.listen_for_device_user(app.socket_clients))

    async def listen_for_device_user(connection, cluster):
        channel = await connection.channel()

        queue = await channel.declare_queue('device_user')

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    messagejson = json.loads(message.body)
                    if "uuid" in messagejson:
                        if str(messagejson['uuid']) in cluster:
                            print(await cluster[messagejson["uuid"]].sendMessage(messagejson["message"]))
                        else:
                            print("Kullanici bulanamadi")
                    print(f"Received message: {message.body}")

    async def listen_for_user_device(connection, cluster):
        channel = await connection.channel()
        queue = await channel.declare_queue('user_device')

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    messagejson = json.loads(message.body)
                    if "uuid" in messagejson:
                        if str(messagejson['uuid']) in cluster:
                            print(await cluster[messagejson["uuid"]].sendMessage(messagejson["message"]))
                        else:
                            print("Kullanici bulanamadi")
                    print(f"Received message: {message.body}")
