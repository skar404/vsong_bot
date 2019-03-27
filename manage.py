from vsong_bot.main import run_api, run_consumer
from manager import Manager

manager = Manager()


@manager.command
def api():
    run_api()


@manager.command
def consumer():
    run_consumer()


if __name__ == "__main__":
    manager.main()
