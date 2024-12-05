from models import Account


async def read_accout_by_phone_number(phone_number: str) -> Account:
    account = await Account.find(Account.phone_number == phone_number).first_or_none()
    return account


async def create_account(phone_number: str, name: str) -> Account:
    account = await Account.create(phone_number=phone_number, name=name)
    return account
