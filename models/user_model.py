from persistence.mapper.mapper_class import RelationalMapper


class Users(RelationalMapper):

    def __init__(self, id=None, name=None, lastname=None, phone_number=None) -> None:
        super().__init__(self)
        self.id = id
        self.name = name
        self.lastname = lastname
        self.phone_number = phone_number

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.lastname,
            "lastname": self.lastname,
            "phone_number": self.phone_number
        }
