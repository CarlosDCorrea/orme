from orme import cli

from .db.migrations import run_migrations, _create_migration


def main():
    # run_migrations()
    cli.main()


if __name__ == '__main__':
    _create_migration()
    # run_migrations()
    # main()
