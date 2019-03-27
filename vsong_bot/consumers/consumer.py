import asyncio

import aio_pika


class Consumer:
    def __init__(self, url):
        self.url = url
        self.connection = None

    async def connect(self, loop: asyncio.AbstractEventLoop = None):
        self.connection = await aio_pika.connect_robust(
            url=self.url,
            loop=loop if loop else asyncio.get_event_loop()
        )
