from pydantic import BaseModel


class Message(BaseModel):
    uuid: str
    message: str
    response: str
    created_at: str
    updated_at: str
