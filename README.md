# Document Analyzer with LLM Integration
A Flask-based web application that allows users to upload .docx files for analysis. The app interacts with a large language model (LLM) to summarize documents and answer queries based on the content of the uploaded files. The app supports the following:

* **Document Summarization:** Summarizes the key points of the uploaded document.

* **Query-Based Analysis:** Answers user-provided queries based on the content of the uploaded document.
* **Local Model Server:** The model is hosted using LM Studio running as a local server, which handles the summarization and query tasks.

## Features

* Upload and analyze .docx files.

* Summarize documents using an LLM model.

* Answer specific queries related to the document's content.

* Clean and formatted summaries and answers based on the document text.

## Project Structure

```bash
document-analyzer/
├── app.py                 # Flask server that handles document uploads, analysis, and queries
├── templates/             # HTML templates for the web interface
│   ├── welcome.html       # Welcome page
│   ├── document_analyzer.html  # Document upload page for analysis
│   └── query.html         # Query page for document-specific questions
├── uploads/               # Folder to store uploaded files
```

## Setup Instructions
**1. Set Up LM Studio Model Server**
Ensure that your LM Studio model is running as a server. You'll need to replace the MODEL_API_URL in app.py with the correct URL for your local LM Studio server.

If you’re using LM Studio to host the model locally, it will likely be running on a specific port on your machine (e.g., http://123.0.0.1:5000 or another port of your choice).
For example:
```bash
MODEL_API_URL = 'http://123.0.0.1:134/v1/completions'  # Local LM Studio model server
```
**2. Start the LM Studio Server**
Run your LM Studio server locally, ensuring that it's accessible from the Flask app. If you're using LM Studio's built-in server or an external deployment, make sure the API endpoint (/v1/completions) is available and configured correctly.
**3. Run the Flask App**
Start the Flask server to allow users to interact with the document analysis tool:
```bash
python app.py
```

## Usage
#### Home Page
Once the app is running, visit http://localhost:5000/. You will be greeted with the welcome page.

#### Document Analysis
* Navigate to the Document Analyzer page.

* Upload one or more .docx files.

* Click "Analyze" to generate summaries for each document.

* The summaries will be displayed for each file uploaded.

#### Query-Based Analysis
* Navigate to the Query page.

* Upload a .docx file.

* Enter a query that you would like to ask based on the document's content.

* The app will respond with the answer generated from the document using the LM Studio model server.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

