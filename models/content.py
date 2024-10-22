from pydantic import BaseModel, Field


class Content(BaseModel):
    question: str = Field(default=None, alias='question')
    customer_uuid: str = Field(default=None, alias='customer_uuid')
    user_uuid: str = Field(default=None, alias='user_uuid')
    message_uuid: str = Field(default=None, alias='message_uuid')
    is_solved: bool = Field(default=None, alias='is_solved')
