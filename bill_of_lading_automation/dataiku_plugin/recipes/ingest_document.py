# Ingest Bill of Lading Document Recipe
# Reads files from S3 or local storage and outputs document metadata
import os
import yaml
from ..aws.s3_utils import S3Client

def run_ingest(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    ocr_conf = config['ocr']
    if ocr_conf['engine'] == 'aws_textract':
        s3 = S3Client(ocr_conf['aws_region'])
        files = s3.list_files(ocr_conf['s3_bucket'], ocr_conf['s3_input_prefix'])
        # Output: list of S3 keys
        return [{'s3_key': key} for key in files]
    else:
        # Local directory ingestion (placeholder)
        local_dir = ocr_conf.get('local_input_dir', './input')
        files = [os.path.join(local_dir, f) for f in os.listdir(local_dir)]
        return [{'local_path': f} for f in files]

# Example usage:
# docs = run_ingest('config/sample_config.yaml')
# print(docs) 