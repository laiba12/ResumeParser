import redis

class RedisDataHandler():

    def __init__(self):
         try:
            # Production
            # self.conn = redis.StrictRedis(host="api.cardinalintinc.com", port="6379", username="default", password="testing123", encoding='utf-8', decode_responses=True)
            
            # Localhost
            self.conn = redis.StrictRedis(host="localhost", port="6379", username="default", password="testing123", encoding='utf-8', decode_responses=True)
         except Exception as e:
            print(e)
            
    def SaveData(self, obj, prefix='test:'):
        try:
            count = int(self.conn.ft('test_index').info()['num_docs']) + 501
            obj = { "Id": obj['Id'], "Content": obj['Content'], "FileName": obj['FileName'], "Embedding": obj['Vector'], "ParentKey": obj['Id'] + "_" + obj['FileName']}
            self.conn.hset(name=prefix+obj['Id'], mapping=obj)
        except Exception as e:
            print(e)
            print("Some error occured while posting. " + str(e))