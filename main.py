from fastapi import FastAPI
from dotenv import load_dotenv

from controllers import MessagesController
from models import Content

app = FastAPI()


@app.get("/messages")
async def respond_question(customer_uuid: str, user_uuid: str):
    try:
        messanger = MessagesController()
        return messanger.get_historical_messages(customer_uuid, user_uuid)
    except Exception as e:
        return {"Error": str(e)}


@app.post("/messages")
async def respond_question(content: Content):
    try:
        messanger = MessagesController()
        return messanger.post_message(content.question, content.customer_uuid, content.user_uuid)
    except Exception as e:
        return {"Error": str(e)}


@app.put("/messages")
async def respond_question(content: Content):
    try:
        messanger = MessagesController()
        return messanger.put_message_review(content.message_uuid, content.is_solved)
    except Exception as e:
        return {"Error": str(e)}
