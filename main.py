from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import os
import logging
import download_and_decompress
import parse_xml
import send_jobs_to_xano

app = Flask(__name__)
auth = HTTPBasicAuth()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the username and password for authentication
USERNAME = os.environ.get('AUTH_USERNAME', 'admin')
PASSWORD = os.environ.get('AUTH_PASSWORD', 'password')

# URLs for external resources
XANO_URL = os.environ.get('XANO_URL', 'https://your-default-xano-url.com')
XML_FILE_URL = os.environ.get('XML_FILE_URL', 'https://default-xml-url.com')


@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD


@app.route('/trigger', methods=['POST'])
@auth.login_required
def trigger():
    logging.info("Trigger function started")
    decompressed_file = download_and_decompress.download_and_decompress(
        XML_FILE_URL)
    logging.info(f"Decompressed file: {decompressed_file}")
    json_file_path = parse_xml.parse_xml_to_json(decompressed_file)
    logging.info(f"JSON file path: {json_file_path}")
    send_jobs_to_xano.send_jobs_in_chunks(json_file_path)
    logging.info("Jobs sent to Xano")

    # Clean up temporary files
    if decompressed_file:
        os.remove(decompressed_file)
    if json_file_path:
        os.remove(json_file_path)

    logging.info("Trigger function completed")
    return "Code execution triggered successfully!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
