import uuid

from models.user_model import Users
from models.auth_model import Auth


class UserServices:

    def __init__(self): ...

    def create_user(self, user_data: dict, auth_data: dict):
        users = Users(**user_data)
        auth = Auth()

        auth_data["user_id"] = users.id

        users.set(**user_data)
        auth.set(**auth_data)

        users.get(id=users.id)
        print(users.format_json())


user = UserServices()
user.create_user({
    "id": str(uuid.uuid4()),
    "name": "Katerina Loba",
    "lastname": "Koslova Monroe Soap",
    "phone_number": "9617105170"
    },
    {
        "id": str(uuid.uuid4()),
        "email": "kastez36q5@gmail.com",
        "password": "locote",
        "role": "USER"
    }
)