from persistence.mapper.relational_mapper import RelationalMapper


class MedicalHistory(RelationalMapper):
    
    def __init__(self) -> None:
        super().__init__(self)
        self.id = None
        self.issue = None
        self.pet_id = None

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "issue": self.issue,
            "pet_id": self.pet_id
        }
