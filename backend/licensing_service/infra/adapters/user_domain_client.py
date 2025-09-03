from uuid import UUID


class Client:

    def __init__(self):
        print("make connection to domain Users")

    def get(self, id: UUID) -> dict:
        user_data = {
            "user_id": id,
            "email": "yaricp@gmail.com",
            "tg_id": "123123123",
            "superadmin": True
        }
        return user_data
