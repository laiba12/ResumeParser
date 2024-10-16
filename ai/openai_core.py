from openai import OpenAI
from config.const import EMBEDDING_MODEL


class OpenAIHandler():
    def __init__(self, openai_api_key):
         self.client = OpenAI()
         self.client.api_key = openai_api_key
    

    def GetEmbeddings(self, text, model=EMBEDDING_MODEL, query=False):
        try:
            result = self.client.embeddings.create(input=text, model=model).data
            if query:
                return result[0].embedding
            return result
        except Exception as e:
            print(e.with_traceback)