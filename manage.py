from manager import Manager

from app import run_web

manager = Manager()


@manager.command
def web():
    run_web()


if __name__ == '__main__':
    manager.main()
