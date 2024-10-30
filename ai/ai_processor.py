import openai
import os


<<<<<<< HEAD
openai.api_key = 'sk-dsoXDnCOhC-y3BfOp-JZzlBUoA3AnBZS2gJKKv_JH2T3BlbkFJIWItWZF9SB-TwBx3CqBXqCVKouPBOkLAVilxACfzUA'
=======
openai.api_key = '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'
>>>>>>> 1668d963f62998003c7998ac11628060f1aab3f1
 

def call_openai_api(prompt_text):
    
    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an AI that extracts structured data from resumes in JSON format."},
                {"role": "user", "content": prompt_text},
            ]
        )
        print(f"AI Response: {response}")

        ai_message=  response['choices'][0]['message']['content'].strip()
        return ai_message
    
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

