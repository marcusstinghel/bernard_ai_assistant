from fastapi import FastAPI, APIRouter
from kernel import Mind
from models import Content
from dotenv import load_dotenv

app = FastAPI()


@app.post("/respond")
async def respond_question(content: Content):
    try:
        load_dotenv(r'C:\Users\vinio\Projects\octamind-web-api\.env')
        pipeline_card_controller = Mind()
        return pipeline_card_controller.respond(content.question, content.customer_uuid, content.owner_user_uuid)
    except Exception as e:
        return {"Error": str(e)}
