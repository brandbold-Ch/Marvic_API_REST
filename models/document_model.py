from persistence.mapper.mapper_class import RelationalMapper


class Document(RelationalMapper):
    
    def __init__(self) -> None:
        super().__init__(self)
        self.id = None
        self.document = None
        self.medical_history_id = None

    def format_json(self) -> dict:
        return {
            "id": self.id,
            "document": self.document,
            "medical_history_id": self.medical_history_id
        }
