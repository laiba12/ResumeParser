import redis
from datetime import datetime
from flask import json, jsonify
from redis_handler.document_manager import DocumentManager
import tiktoken
from ai.openai_core import OpenAIHandler
import numpy as np
from redis_handler.redisDataHandling import RedisDataHandler
import os

redis_client = redis.StrictRedis(host='localhost', port=6379, username="default", password="testing123", encoding='utf-8', decode_responses=True)
openai_api_key=os.getenv('OPENAI_API_KEY')

openAIHandler= OpenAIHandler(openai_api_key)
redisHandler=RedisDataHandler()


class TextChunker:
    def __init__(self, maxlen):
        self.maxlen = maxlen

    def chunk(self, text):
        """Yields chunks of text with a max length."""
        for i in range(0, len(text), self.maxlen):
            yield text[i:i+self.maxlen]
            
def process_data(parsed_data, filename):
    """Process parsed AI data and save it into Redis in small chunks."""
    chunker = TextChunker(maxlen=500)  # Chunk size can be adjusted as needed
     
    obj=[]
    
    for  chunk in chunker.chunk(parsed_data):
        
        data=DocumentManager.add_doc(chunk, filename)
        obj.append(json.loads(data))
        
    embeddings = process_embedding(obj)
    knowledge_base = process_save(embeddings)
    
    total_docs = DocumentManager.count_documents()
    print(f"Total number of documents: {total_docs}")
        
    return knowledge_base
    
def process_embedding(input_data):
    input_list = []
    
    # Ensure input_data is of the expected format
    if not isinstance(input_data, list):
        print("Input data is not a list.")
        return
                                                     
    for item in input_data:
        # Replace newline characters with spaces
        item_content = item.get('Content', '')  # Ensure 'Content' key exists
        item_content = item_content.replace("\n", " ")
        input_list.append(item_content)

    input_size = token_count(input_list)
    print(f"Total input_size is: {input_size}") 
    
    if input_size<= 8191:
        try:
            response = openAIHandler.GetEmbeddings(input_list)
            # Iterate over input_data and add the embedding vectors
            for item, vector_item in zip(input_data, response):
                item['Vector'] = np.array(vector_item.embedding).astype(np.float32).tobytes()
        except ValueError as e:
            print(f"ValueError: {e}")
            
    return input_data
            
def process_save(input_data):
    for data in input_data:
        try:
             # Save the processed data using redisHandler.SaveData()
            redisHandler.SaveData(data)
        except Exception as e:
            print(f"Some error occurred while processing data: {e}")

    
def token_count(string_list) -> int:
    total = 0
    tik = tiktoken.get_encoding("cl100k_base")
    for i_str in string_list:
        total += len(tik.encode(i_str))
    return total

        

    # Generate a unique Redis key using the filename and timestamp
    # redis_key_prefix = f"{filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Convert the parsed data to a string if needed
    # parsed_data_str = json.dumps(parsed_data)

    # # Iterate over chunks and save each to Redis
    # for idx, chunk in enumerate(chunker.chunk(parsed_data_str)):
    #     redis_key = f"{redis_key_prefix}_chunk_{idx}"
    #     print(f"Saving chunk to Redis with key: {redis_key}")
    #     redis_client.set(redis_key, chunk)

    # print(f"Total chunks saved: {idx + 1}")
    