import openai
import os


openai.api_key = os.getenv('OPENAI_API_KEY')

def call_openai_api(prompt_text):
    
    try:
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the newer model
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

