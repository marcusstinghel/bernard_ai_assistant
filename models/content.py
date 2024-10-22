from pydantic import BaseModel, Field


class Content(BaseModel):
    question: str
    customer_uuid: str
    user_uuid: str
    message: str = Field(default=None, alias='message')
    is_solved: bool = Field(default=None, alias='is_solved')
