import logging

import aio_pika

from vsong_bot.consumers.consumer import Consumer


class DownloadSongConsumer(Consumer):
    async def declare_queues(self):
        await self.declare_processing_queue(
            name="song_download",
            exchange="song.new",
            durable=True,
            prefetch_count=100,
            timeout=15,
            with_ack=True
        )

    async def processing(self, message: aio_pika.IncomingMessage, queue: aio_pika.Queue):
        logging.info('start download song...')
        logging.info('end download song')
