from orme import cli

from .db.migrations import run_migrations


def main():
    # run_migrations()
    cli.main()


if __name__ == '__main__':
    print('i am in main')
    run_migrations()
    main()
