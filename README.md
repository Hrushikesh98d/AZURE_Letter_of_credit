# Document Extraction 

## Author
**Hrushikesh Dandge**

## About

This web application enables users to upload PDF documents and extract 45A Field information using  Azure Document Intelligence services.

 Azure services have been trained to recognize and extract specified data fields from these document types. The extracted information is displayed on the web application interface for easy access and review.

 ## Installation & Setup

1. Clone the repository to your local machine:
2. Install the required dependencies:
   
   `pip install -r requirements.txt`
3. Downlaod the service-account-key.json to your local machine and set up the path in the app.py at line:62
4. Run the application
   `python app.py`
5. Open your browser and navigate to http://localhost:5000.
