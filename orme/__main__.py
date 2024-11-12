from orme import cli

from .db.migrations import app_need_migrations


def main():
    # run_migrations()
    cli.main()


if __name__ == '__main__':
    app_need_migrations()
    # main()
