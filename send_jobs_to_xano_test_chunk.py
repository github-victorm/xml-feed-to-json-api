import requests
import json

# API endpoint configuration
api_url = 'https://xacy-l964-x9i6.n7c.xano.io/api:VG3k0Xrv/live_direct_from_appcast_cpc'
headers = {'Content-Type': 'application/json'}


def send_test_chunk(json_file_path, chunk_size=300):
    # Read the JSON file line by line
    try:
        with open(json_file_path, 'r') as file:
            jobs = []
            for line in file:
                job = json.loads(line)
                jobs.append(job)
                # Only send one chunk for the test
                if len(jobs) == chunk_size:
                    send_to_api(jobs)
                    return  # Exit after sending one chunk

    except FileNotFoundError:
        print("JSON file not found.")


def send_to_api(jobs):
    data = {'jobs': jobs}
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        print("Chunk sent successfully!")
    else:
        print(
            f"Failed to send chunk. Status code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    json_file_path = 'xml_feed_as_json_output.json'
    send_test_chunk(json_file_path)
