from datetime import date


def validate_date(str_date: str) -> None:
    try:
        date.fromisoformat(str_date)
    except ValueError as e:
        print(f"error while validating date {e}")
        exit(1)
