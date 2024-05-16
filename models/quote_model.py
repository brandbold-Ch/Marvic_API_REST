from persistence.mapper.relational_mapper import RelationalMapper


class Quote(RelationalMapper):
    
    def __init__(self) -> None:
        super().__init__(self)
        self.id = None
        self.creation_date = None
        self.expiration_date = None
        self.pet_id = None
        self.user_id = None
        self.issue = None
        self.solved = None

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "dates": {
                "creation_date": self.creation_date,
                "expiration_date": self.expiration_date
            },
            "identifiers": {
                "pet_id": self.pet_id,
                "user_id": self.user_id
            },
            "status": {
                "issue": self.issue,
                "solved": self.solved
            }
        }
