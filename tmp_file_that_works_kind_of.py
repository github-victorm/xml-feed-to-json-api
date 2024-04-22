import requests
import gzip


async def fastgen(context):
    print(context)

    # Define the download URL and filename
    download_url = "https://exchangefeeds.s3.amazonaws.com/473ed2d8ad4294c48e5145929070061e/feed.xml.gz"
    # download_url = "https://statechange.ai"

    compressed_filename = "/tmp/appcast_cpc_feed.xml.gz"
    decompressed_filename = "/tmp/appcast_cpc_feed.xml"

    # Function to download and decompress the file
    def download_and_decompress():
        # Download the file
        print("Downloading the file...")
        response = requests.get(download_url, stream=True)
        print("download completed")

        # Check for successful download
        if response.status_code == 200:
            print("status code 200")
            with open(compressed_filename, "wb") as f:
                print("inside with")
                # Increase chunk size to 1MB
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    print("writing a chunk")
                    f.write(chunk)
            print(f"Download complete. File saved as: {compressed_filename}")
        else:
            print(f"Download failed. Status code: {response.status_code}")
            return  # Exit if download failed

        # Decompress the downloaded file
        try:
            print("Decompressing the file...")
            with gzip.open(compressed_filename, 'rb') as f_in:
                with open(decompressed_filename, 'wb') as f_out:
                    for chunk in iter(lambda: f_in.read(1024 * 1024), b''):  # Read in 1MB chunks
                        f_out.write(chunk)
            print("Decompression successful!")
        except FileNotFoundError:
            print("Downloaded file not found. Decompression failed!")

    # Call the function to download and decompress
    download_and_decompress()

    return {"message": "Process completed successfully"}
