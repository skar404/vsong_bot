from app.settings import RABBITMQ_QUERY

from app.consume.jobs import consumer_bot_message


async def consumers_init(app):
    queue_name = RABBITMQ_QUERY

    # Creating channel
    channel = await app.aio_pika.channel()

    # Declaring queue
    queue = await channel.declare_queue(
        queue_name,
        durable=True,
    )

    await queue.consume(consumer_bot_message)
