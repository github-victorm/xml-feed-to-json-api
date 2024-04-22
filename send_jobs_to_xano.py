import os
import requests
import json
import logging
import time
from parse_xml import parse_xml_to_json
from download_and_decompress import download_and_decompress

# API endpoint configuration
api_url = os.environ.get('XANO_URL')
api_key = os.environ.get('XANO_KEY')
headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
    }

# I created these exclusions to prefilter some undesirable job titles from the feed we are working with. feel free to apply exclusions to your fields using the same logic.
# Job title exclusions (lowercased for case-insensitive matching)
exclusions = [
    "delivery driver", "cashier", "barista", "waiter", "waitress",
    "line cook", "prep cook", "retail sales associate", "customer service representative",
    "warehouse worker", "cleaner", "housekeeper", "uber driver", "lyft driver",
    "seasonal worker", "entry level", "crew member", "staff member",
    "team member", "helper", "attendant"
]


def job_title_excluded(title):
    title = title.lower()
    return any(exclusion in title for exclusion in exclusions)


def send_jobs_in_chunks(json_file_path, chunk_size=1500, max_chunks=3000):
    try:
        with open(json_file_path, 'r') as file:
            jobs = []
            chunk_count = 0
            for line in file:
                job = json.loads(line)
                # Skip jobs with excluded titles
                if job_title_excluded(job["title"]):
                    continue
                # Check other filters like URL exclusions here, if needed
                jobs.append(job)
                # Send chunks of jobs
                if len(jobs) == chunk_size:
                    send_to_api(jobs)
                    jobs = []  # Reset the list after sending
                    chunk_count += 1
                    # Break the loop after sending the specified number of chunks
                    if chunk_count >= max_chunks:
                        break
                    # Add a sleep delay between API requests
                    time.sleep(1)  # Adjust the delay as needed
            # Send any remaining jobs if there are any and the chunk limit is not reached
            if jobs and chunk_count < max_chunks:
                send_to_api(jobs)
    except FileNotFoundError:
        logging.error("JSON file not found.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def send_to_api(jobs):
    data = {'jobs': jobs}
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        logging.info("Chunk sent successfully!")
    else:
        logging.error(f"Failed to send chunk. Status code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    # Retrieve the XML file URL from the environment variable
    xml_file_url = os.environ.get('XML_FILE_URL')
    if xml_file_url:
        decompressed_file = download_and_decompress(xml_file_url)
        json_file_path = parse_xml_to_json(decompressed_file)
        send_jobs_in_chunks(json_file_path, max_chunks=1)
        os.remove(json_file_path)  # Clean up the temporary JSON file
        os.remove(decompressed_file) # Clean up the temporary decompressed xml file
    else:
        logging.error("XML_FILE_URL environment variable not set.")
