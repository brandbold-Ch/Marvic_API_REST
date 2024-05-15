from persistence.mapper.mapper_class import RelationalMapper


class Image(RelationalMapper):

    def __init__(self):
        super().__init__(self)
        self.id = None
        self.image = None
        self.pet_id = None
        self.medical_history_id = None

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "image": self.image,
            "pet_id": self.pet_id,
            "medical_history_id": self.medical_history_id
        }
