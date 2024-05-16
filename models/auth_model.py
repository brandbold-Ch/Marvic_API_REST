from persistence.mapper.relational_mapper import RelationalMapper


class Auth(RelationalMapper):

    def __init__(self) -> None:
        super().__init__(self)
        self.id = None
        self.user_id = None
        self.email = None
        self.password = None
        self.role = None

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
