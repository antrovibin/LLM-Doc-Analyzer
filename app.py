from flask import Flask, render_template, request, jsonify
import os
import requests
from docx import Document
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL_API_URL = 'http://192.168.27.106:1234/v1/completions'  # Ensure this URL points to your LM Studio model API

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Function to extract text from a .docx file
def get_text_from_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# Function to analyze the document (i.e., summarize it)
def analyze_document(doc_text):
    prompt = (
        f"Here is the content of a document:\n\n{doc_text}\n\n"
        "Please summarize the document's main points in a concise manner, without any additional questions or commentary."
    )
    
    payload = {
        "model": "gemma-2-2b-it",  # Replace with the correct model identifier
        "prompt": prompt,
        "max_tokens": 500  # Adjust token length as needed
    }

    try:
        logging.debug(f"Sending the following prompt to the LLM model for summarization: {prompt[:100]}...")  # Log the first 100 characters of the prompt
        res = requests.post(MODEL_API_URL, json=payload)

        logging.debug(f"Response Status Code: {res.status_code}")  # Log response status
        logging.debug(f"Response Text: {res.text}")  # Log full response text to see what is returned
        
        if res.status_code == 200:
            response_data = res.json()
            logging.debug(f"API Response: {response_data}")  # Log the full API response
            # Check if 'choices' key exists and contains the text
            if 'choices' in response_data and len(response_data['choices']) > 0:
                summary_text = response_data['choices'][0]['text'].strip()
                if summary_text:
                    # Clean up the summary and format it more properly
                    formatted_summary = (
                        "Summary:\n\n" + summary_text.replace('*', '').replace('\n', '\n\n')
                    )
                    return formatted_summary
                else:
                    logging.error("Error: No summary text returned.")
                    return "Summary could not be generated from the document."
            else:
                logging.error("Error: No 'choices' found in the API response.")
                return "Error occurred while generating the summary."
        else:
            logging.error(f"Error: {res.status_code} - {res.text}")
            return "Error occurred while analyzing the document."
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return "Error occurred while analyzing the document."

# Function to handle the query request
def get_model_query(doc_text, query):
    prompt = (
        f"Here is the content of a document:\n\n{doc_text}\n\n"
        f"User's query: {query}\n\n"
        "Please answer the user's query based on the document's content."
    )
    
    payload = {
        "model": "gemma-2-2b-it",  # Replace with the correct model identifier
        "prompt": prompt,
        "max_tokens": 500  # Adjust token length as needed
    }

    try:
        logging.debug(f"Sending the following query to the LLM model: {prompt[:100]}...")  # Log the first 100 characters of the prompt
        res = requests.post(MODEL_API_URL, json=payload)

        logging.debug(f"Response Status Code: {res.status_code}")  # Log response status
        logging.debug(f"Response Text: {res.text}")  # Log full response text to see what is returned
        
        if res.status_code == 200:
            response_data = res.json()
            logging.debug(f"API Response: {response_data}")  # Log the full API response
            # Check if 'choices' key exists and contains the text
            if 'choices' in response_data and len(response_data['choices']) > 0:
                answer_text = response_data['choices'][0]['text'].strip()
                if answer_text:
                    return answer_text
                else:
                    logging.error("Error: No answer text returned.")
                    return "No relevant information found in the document for your query."
            else:
                logging.error("Error: No 'choices' found in the API response.")
                return "Error occurred while processing your query."
        else:
            logging.error(f"Error: {res.status_code} - {res.text}")
            return "Error occurred while processing your query."
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return "Error occurred while processing your query."

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/document_analyzer')
def document_analyzer():
    return render_template('document_analyzer.html')

@app.route('/query')
def query():
    return render_template('query.html')

# Route to analyze documents (multiple files)
@app.route('/analyze_documents', methods=['POST'])
def analyze_documents():
    files = request.files.getlist('files')
    results = []

    if not files:
        return jsonify({'message': 'No files uploaded.'}), 400

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Get document text
        doc_text = get_text_from_docx(filepath)
        logging.debug(f"Extracted text from document: {doc_text[:200]}...")  # Log the extracted document text (trimmed for readability)
        
        # Get the summary from the LLM
        summary = analyze_document(doc_text)

        results.append({
            "filename": filename,
            "summary": summary
        })

    return jsonify(results)

# Route to handle queries (single document)
@app.route('/query_document', methods=['POST'])
def query_document():
    file = request.files.get('file')
    user_query = request.form.get('query')

    if not file:
        return jsonify({'message': 'No file uploaded.'}), 400

    if not user_query:
        return jsonify({'message': 'No query provided.'}), 400

    # Save the file
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Get document text
    doc_text = get_text_from_docx(filepath)

    # Send the query and document text to the LLM model
    answer = get_model_query(doc_text, user_query)

    if not answer:
        return jsonify({'message': 'No relevant information found in the document for your query.'})

    return jsonify({
        'filename': filename,
        'query': user_query,
        'answer': answer
    })

if __name__ == '__main__':
    app.run(debug=True)
