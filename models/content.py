from pydantic import BaseModel


class Content(BaseModel):
    question: str
    customer_uuid: str
    user_uuid: str
