from datetime import datetime, timezone


def validate_otp(otp: int) -> bool:
    date = datetime.now(timezone.utc).strftime("%y-%m-%d").replace("-", "")
    return str(otp) == date
