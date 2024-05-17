from pydantic import BaseModel


class Document(BaseModel):
    document: str = None
