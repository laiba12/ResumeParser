def aiprompt_text(pdf_text, outputJsonFormat):
    return f"""
        You are a specialist in resume parsing. 
        Your task is to extract relevant information from the provided resume text and 
        organize it into a structured JSON format.
        
        ### Instructions:
        1. **Input Data:** Use the resume text provided in [InputData].
        2. **Output Format:** Adhere to the following JSON schema in [OutputJSON]. 
        Ensure that the data is organized into key-value pairs according to this schema. 
        Omit any sections that do not contain relevant information.
        
        InputData: {pdf_text}
        OutputJSON: {outputJsonFormat}
        
        ### Sections to Extract:
        - **Personal Information:** Extract the first name, middle name, last name, date of birth, email, mobile number, designation, total experience (years and months), and availability.
        - **Key Skills:** Identify key skills and languages known by the candidate.
        - **Education:** List all educational qualifications, including the institute, degree, start date, and end date.
        - **Address Details:** Provide the candidate's address, city, country, and postal code.
        - **Social Links:** Include any relevant URLs (LinkedIn, personal website, etc.).
        - **Experience:** Outline each work experience, including title, company name, location, employment type, start and end dates, whether it is the current role, and a summary of responsibilities.

        ### Additional Notes:
        - Ensure to follow the order of sections as specified in the JSON schema.
        - If any section is absent in the resume, omit it from the response.
        - Focus on accuracy and clarity in extracting the information.

        """
def aioutputJsonFormat():
    return """
        {
            "personal_information": {
                "first_name": "",
                "middle_name": "",
                "last_name": "",
                "date_of_birth": "",
                "email": "",
                "mobile_number": "",
                "designation": "",
                "total_experience": {
                    "years": "",
                    "months": ""
                },
                "availability": ""
            },
            "key_skills": {
                "skills": [],
                "languages": []
            },
            "education": [
                {
                    "institute": "",
                    "degree": "",
                    "start_date": "",
                    "end_date": ""
                }
            ],
            "address_details": {
                "address": "",
                "city": "",
                "country": "",
                "postal_code": ""
            },
            "social_links": {
                "urls": []
            },
            "experience": [
                {
                    "title": "",
                    "company_name": "",
                    "company_location": "",
                    "employment_type": "",
                    "start_date": "",
                    "end_date": "",
                    "current_role": "",
                    "summary": ""
                }
            ]
        }

        """
    
