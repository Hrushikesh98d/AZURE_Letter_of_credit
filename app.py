from flask import Flask, render_template, request, send_from_directory
from google.oauth2 import service_account
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import os
import mimetypes
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO)

# Azure models configuration
azure_models = {
    "45A": {
        "endpoint": "https://45a.cognitiveservices.azure.com/",
        "key": "bb460754073646d2ada133f6b470a5ac",
        "model_id": "45A_1"  # Ensure model_id is correctly specified here
    },

}



def process_document_azure(file_path, model_info):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=model_info["endpoint"],
        credential=AzureKeyCredential(model_info["key"])
    )

    with open(file_path, "rb") as document:
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_info["model_id"],
            document=document
        )
        result = poller.result()

    extracted_data = []
    for idx, document in enumerate(result.documents):
        for name, field in document.fields.items():
            if field.value_type:  # Only include labeled fields
                field_value = field.value if field.value else field.content
                extracted_data.append((name, field_value))
    extracted_data.sort(key=lambda x: x[0])
    return extracted_data



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        document_file = request.files['document_file']
        service_type = request.form['service_type']
        processor_id = request.form['processor_type']

        if document_file:
            file_content = document_file.read()
            mime_type, _ = mimetypes.guess_type(document_file.filename)

            if mime_type is None:
                logging.error("Unsupported file type")
                return "Unsupported file type", 400

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], document_file.filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)


                # service_type == 'azure':
                model_info = azure_models.get(processor_id)
                entities = process_document_azure(file_path, model_info)
                return render_template('results2.html', entities=entities, file_url=f"/uploads/{document_file.filename}")

    return render_template('index.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
