import asyncclick as click
from db import database
from models import RoleType
from managers.user import Usermanager


@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-pa", "--password", type=str, required=True)
async def create_user(first_name, last_name, email, phone, iban, password):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "iban": iban,
        "password": password,
        "role": RoleType.admin
    }

    await database.connect()
    await Usermanager.register(user_data)
    await database.disconnect()


if __name__ == '__main__':
    create_user(_anyio_backend="asyncio")
