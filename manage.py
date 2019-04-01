import logging

from manager import Manager

from vsong_bot.main import run_api, run_consumer


LOGGER_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.DEBUG,
)


manager = Manager()


@manager.command
def api():
    run_api()


@manager.command
def consumer():
    run_consumer()


if __name__ == "__main__":
    manager.main()
