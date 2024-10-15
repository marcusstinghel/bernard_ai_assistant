from pydantic import BaseModel


class Content(BaseModel):
    question: str
    customer_uuid: str
    owner_user_uuid: str
