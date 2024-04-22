import requests
import gzip
import bz2
import lzma
import tempfile
import os
import logging


def download_and_decompress(xml_file_url):
    # Create temporary file paths
    temp_dir = tempfile.gettempdir()
    compressed_filename = os.path.join(temp_dir, "appcast_feed")
    decompressed_filename = os.path.join(temp_dir, "appcast_feed.xml")

    # Download the file
    logging.info("Downloading the file...")
    response = requests.get(xml_file_url, stream=True)

    # Check for successful download
    if response.status_code == 200:
        with open(compressed_filename, "wb") as f:
            # Increase chunk size to 1MB
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
        logging.info(f"Download complete. File saved as: {compressed_filename}")
    else:
        logging.error(f"Download failed. Status code: {response.status_code}")
        return  # Exit if download failed

    # Detect the compression type based on the file extension
    _, file_extension = os.path.splitext(xml_file_url)
    compression_type = file_extension.lower()

    # Decompress the downloaded file based on the compression type
    try:
        logging.info(f"Decompressing the file using {compression_type} compression...")
        if compression_type == ".gz":
            with gzip.open(compressed_filename, 'rb') as f_in:
                with open(decompressed_filename, 'wb') as f_out:
                    f_out.write(f_in.read())
        elif compression_type == ".bz2":
            with bz2.BZ2File(compressed_filename, 'rb') as f_in:
                with open(decompressed_filename, 'wb') as f_out:
                    f_out.write(f_in.read())
        elif compression_type == ".xz":
            with lzma.open(compressed_filename, 'rb') as f_in:
                with open(decompressed_filename, 'wb') as f_out:
                    f_out.write(f_in.read())
        elif compression_type == ".xml" or compression_type == "":
            # If the file is uncompressed, just rename it
            os.rename(compressed_filename, decompressed_filename)
        else:
            raise ValueError(f"Unsupported compression type: {compression_type}")

        logging.info("Decompression successful!")
    except Exception as e:
        logging.error(f"Decompression failed: {str(e)}")
        return  # Exit if decompression failed

    return decompressed_filename


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Retrieve the XML file URL from the environment variable
    xml_file_url = os.environ.get('XML_FILE_URL')

    if xml_file_url:
        decompressed_file = download_and_decompress(xml_file_url)
        logging.info(f"Decompressed file: {decompressed_file}")
    else:
        logging.error("XML_FILE_URL environment variable not set.")
