import ast
import re

from artificial_intelligence import ChatGPT
from database import DataBase
import os


class Kernel:
    __chat_gpt: ChatGPT
    __database_chat: DataBase
    __database_octapipe: DataBase
    __prompts: list[tuple]

    def __init__(self):
        self.__chat_gpt = ChatGPT(
            organization_key=os.getenv('API_OPENAI_ORGANIZATION'),
            project_key=os.getenv('API_OPENAI_PROJECT'),
            api_key=os.getenv('API_OPENAI_API_KEY')
        )
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
        self.__prompts = self.__database_chat.consult(query='SELECT id, prompt FROM prompts')

    def respond(self, customer_question, customer_uuid: str, owner_user_uuid: str) -> str:
        entity_and_context = self.__define_entity_and_context(customer_question=customer_question)
        questions = self.__get_questions(entity=entity_and_context[0], context=entity_and_context[1])
        question = self.__define_question(customer_question, questions)
        customer_id, owner_user_id = self.__get_customer_id_and_user_id(customer_uuid, owner_user_uuid)
        query = self.__make_query(customer_id, owner_user_id, query=question[4], customer_question=customer_question)
        response = self.__generate_response(customer_question=customer_question, query=query)
        return response
               
    def __define_entity_and_context(self, customer_question: str) -> tuple:
        query = 'SELECT DISTINCT entity, context FROM questions'
        result = self.__database_chat.consult(query=query)
        params = {'customer_question': customer_question, 'result': result}
        prompt = next(prompt for prompt in self.__prompts if prompt[0] == 1)[1].format(**params)
        response = self.__chat_gpt.respond(prompt=prompt)
        return ast.literal_eval(response)

    def __get_questions(self, entity: str, context: str) -> list[tuple]:
        query = f'SELECT * FROM questions WHERE entity = "{entity}" AND context = "{context}"'
        result = self.__database_chat.consult(query=query)
        return result

    def __define_question(self, customer_question: str, questions: list[tuple]) -> tuple:
        formatted_questions = "\n".join([f"{question[0]} - {question[3]}" for question in questions])
        params = {'customer_question': customer_question, 'formatted_questions': formatted_questions}
        prompt = next(prompt for prompt in self.__prompts if prompt[0] == 2)[1].format(**params)
        response = self.__chat_gpt.respond(prompt=prompt)
        question = next(question for question in questions if question[0] == int(response))
        return question

    def __get_customer_id_and_user_id(self, customer_uuid: str, owner_user_uuid: str) -> (str, str):
        query_users = f'SELECT id, customer_id FROM users WHERE uuid = "{owner_user_uuid}"'
        query_customers = f'SELECT id FROM customers WHERE uuid = "{customer_uuid}"'
        user_result = self.__database_octapipe.consult(query=query_users)[0]
        customer_result = self.__database_octapipe.consult(query=query_customers)[0]
        owner_user_id = user_result[0]
        customer_id = customer_result[0]
        if user_result[1] != customer_id:
            raise ValueError(f'customer_id {customer_id} does not match owner_user_id {owner_user_id}')
        return customer_id, owner_user_id

    def __make_query(self, customer_id: int, owner_user_id: int, query: str, customer_question: str) -> str:
        placeholders = {'customer_id': customer_id, 'owner_user_id': owner_user_id}
        query_placeholders = re.findall(r'\{(.*?)}', query)
        placeholders.update({placeholder: '' for placeholder in query_placeholders if placeholder not in placeholders})
        params = {'customer_question': customer_question, 'placeholders': placeholders}
        prompt = next(prompt for prompt in self.__prompts if prompt[0] == 4)[1].format(**params)
        filled_placeholders = self.__chat_gpt.respond(prompt=prompt)
        query_formatted = query.format(**ast.literal_eval(filled_placeholders))
        return query_formatted

    def __generate_response(self, customer_question: str, query: str) -> str:
        response = self.__database_octapipe.consult(query=query)[0][0]
        params = {'customer_question': customer_question, 'response': response}
        prompt = next(prompt for prompt in self.__prompts if prompt[0] == 3)[1].format(**params)
        question_response = self.__chat_gpt.respond(prompt=prompt)
        return question_response
