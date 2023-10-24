from datetime import date


def validate_date(str_date):
    try:
        date.fromisoformat(str_date)
    except ValueError as e:
        print(e)
