from dotenv import load_dotenv
from models import Message
import os

from database import DataBase
from kernel import Kernel


class MessagesController:
    def __init__(self):
        self.__database_chat = DataBase(
            db_host=os.getenv('DB_HOST'),
            db_database=os.getenv('DB_DATABASE_CHATGPT'),
            db_user=os.getenv('DB_USER'),
            db_password=os.getenv('DB_PASSWORD')
        )
        self.__database_octapipe = DataBase(
            db_host=os.getenv('DB_HOST'),
            db_database=os.getenv('DB_DATABASE_OCTAPIPE'),
            db_user=os.getenv('DB_USER'),
            db_password=os.getenv('DB_PASSWORD')
        )

    def get_historical_messages(self, customer_uuid: str, user_uuid: str):
        query_users = f'SELECT id, customer_id FROM users WHERE uuid = "{user_uuid}"'
        query_customers = f'SELECT id FROM customers WHERE uuid = "{customer_uuid}"'
        user_result = self.__database_octapipe.consult(query=query_users)[0]
        customer_result = self.__database_octapipe.consult(query=query_customers)[0]
        user_id = user_result[0]
        customer_id = customer_result[0]
        query_messages = f'SELECT * FROM messages WHERE customer_id = "{customer_id}" and user_id = "{user_id}"'
        result = self.__database_chat.consult(query=query_messages)
        formatted_data = [
            Message(
                uuid=row[1],
                message=row[4],
                response=row[6],
                created_at=row[9].isoformat(),
                updated_at=row[10].isoformat()
            )
            for row in result
        ]
        return [msg.dict() for msg in formatted_data]

    def post_message(self, message: str, customer_uuid: str, user_uuid: str):
        kernel = Kernel()
        return kernel.respond(message, customer_uuid, user_uuid)

    def put_message_review(self, message_uuid: str, is_solved: bool):
        query = f'UPDATE messages SET is_solved = "{int(is_solved)}" WHERE uuid = "{message_uuid}"'
        self.__database_chat.insert_or_update(query)
        return 'Updated successfully'
