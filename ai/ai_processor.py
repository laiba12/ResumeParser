import openai
import os


openai.api_key = 'sk-vZvotTt5QvnXsdTgM-vEGSusIl56IHj5n8v1RUqE69T3BlbkFJg5J3rBALlF3St2r_lieonHBhNsVehqbaYkagorzr0A'
 

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

