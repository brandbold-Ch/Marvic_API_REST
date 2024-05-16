from persistence.mapper.relational_mapper import RelationalMapper


class Pet(RelationalMapper):
    
    def __init__(self) -> None:
        super().__init__(self)
        self.id = None
        self.user_id = None
        self.name = None
        self.specie = None
        self.gender = None
        self.size = None
        self.age = None
        self.breed = None
        self.weight = None
        self.live = None

    def __add__(self, other):
        return

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pet_info": {
                "name": self.name,
                "specie": self.specie,
                "breed": self.breed,
                "gender": self.gender
            },
            "phys_char": {
                "size": self.size,
                "weight": self.weight
            },
            "pet_state": {
                "age": self.age,
                "live": self.live
            }
        }
