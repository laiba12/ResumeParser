import uuid
import json

class DocumentManager:
    def __init__(self):
        self.docs={}
        
    def add_doc(self, doc, filename):
        doc_id = str(uuid.uuid4())
        self.docs[doc_id] = {"Content": doc, "FileName": filename}
        json_data = {"Id": doc_id, "Content": doc, "FileName": filename}
        return json.dumps(json_data)
    
    def count_documents(self):
        return len(self.docs)
    
        
      
