from openai import OpenAI


class ChatGPT:

    def __init__(self, organization_key: str, project_key: str, api_key: str):
        self.__client = OpenAI(organization=organization_key, project=project_key, api_key=api_key)

    def respond(self, prompt: str):
        stream = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        return ChatGPT.__make_response(stream=stream)

    @classmethod
    def __make_response(cls, stream):
        response = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response
