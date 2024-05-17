from pydantic import BaseModel


class MedicalHistory(BaseModel):
    issue: str = None
