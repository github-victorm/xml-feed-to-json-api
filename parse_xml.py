from lxml import etree
import json
import os
import tempfile
import logging


def parse_xml_to_json(xml_file_path):
    # Create a temporary file for JSON output
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as json_file:
        json_file_path = json_file.name
        # for this section this will be unique to your xml file. Please change the tag and column data to match the output of your xml to properly parse through it. recommend using chatgpt or another ai platform if you're uncomfortable extracting tags and mapping the columns.
        context = etree.iterparse(xml_file_path, events=(
            'end',), tag='job')  # Focus on the 'job' tag
        processed = 0
        for event, elem in context:
            job_data = {
                'location': elem.findtext('location'),
                'title': elem.findtext('title'),
                # continue with xml column mapping
            }
            # Handle missing elements or cleanup
            job_data = {k: (v.strip() if v else '')
                        for k, v in job_data.items()}
            json_data = json.dumps(job_data)
            json_file.write(json_data + '\n')
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            processed += 1
        logging.info(f"Conversion complete, processed {processed} elements.")

    return json_file_path


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    from download_and_decompress import download_and_decompress
    xml_file_url = os.environ.get('XML_FILE_URL')
    if xml_file_url:
        xml_file_path = download_and_decompress(xml_file_url)
        json_file_path = parse_xml_to_json(xml_file_path)
        logging.info(f"JSON output saved to: {json_file_path}")
    else:
        logging.error("XML_FILE_URL environment variable not set.")
