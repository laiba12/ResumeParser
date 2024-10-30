from flask import Flask, request, jsonify, render_template, json
import os
from pdf_extractor.pdf_handler import extract_text_from_pdf, extract_text_from_docx, extract_text_from_doc
from ai.ai_processor import call_openai_api
from datetime import datetime
from flask_cors import CORS
from ai_prompts import aiprompt_text, aioutputJsonFormat
from concurrent.futures import ThreadPoolExecutor, as_completed


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Create folders for uploads and responses if they don't exist
for folder in ['uploads', 'ai_responses']:
    if not os.path.exists(folder):
        os.makedirs(folder)
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check if 'files' is present in request
        print("Received a request to upload a file.")
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
    
        files = request.files.getlist('files') 
        if len(files) == 0:
            return jsonify({'error': 'No selected files'}), 400

        responses = []  # To store responses for each file

        # Process each uploaded file
        def process_file(file):
            try:
                file_path = os.path.join('uploads', file.filename)
                file.save(file_path)
                
                if file_path.endswith('.pdf'):
                    extracted_text = extract_text_from_pdf(file_path)
                elif file_path.endswith('.docx'):
                    extracted_text = extract_text_from_docx(file_path)
                elif file_path.endswith('.doc'):
                    extracted_text = extract_text_from_doc(file_path)
                else:
                    return {'error': f'Unsupported file format: {file.filename}'}
                
                # AI Processing
                output_format = aioutputJsonFormat()
                prompt = aiprompt_text(extracted_text, output_format)
                ai_response = call_openai_api(prompt)
                ai_response = ai_response.replace("`", "").replace("json", "").replace("\n", "").strip()
                parsed_json = json.loads(ai_response)

                response_filename = f"{os.path.splitext(file.filename)[0]}_{datetime.now().strftime('%d%M%Y')}.json"
                response_path = os.path.join('ai_responses', response_filename)
                
                with open(response_path, 'w') as json_file:
                    json.dump(parsed_json, json_file, indent=4)

                return {
                    'file': file.filename,
                    'parsed_data': parsed_json,
                    'response_file': response_filename
                }
            except Exception as e:
                return {'error': str(e)}

        # Process files concurrently
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_file, file) for file in files]
            for future in as_completed(futures):
                responses.append(future.result())

        return jsonify({'data': responses})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

 # Process files concurrently


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port)
