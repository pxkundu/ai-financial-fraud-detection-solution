# OCR Extraction Recipe
# Uses AWS Textract to extract text from documents
import yaml
from ..aws.textract_utils import TextractClient

def run_ocr(config_path, docs):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    ocr_conf = config['ocr']
    if ocr_conf['engine'] == 'aws_textract':
        textract = TextractClient(ocr_conf['aws_region'])
        results = []
        for doc in docs:
            s3_key = doc['s3_key']
            job_id = textract.start_document_text_detection(ocr_conf['s3_bucket'], s3_key)
            blocks = textract.get_document_text_detection(job_id)
            results.append({'s3_key': s3_key, 'blocks': blocks})
        return results
    else:
        # Placeholder for other OCR engines
        return []

# Example usage:
# ocr_results = run_ocr('config/sample_config.yaml', docs)
# print(ocr_results) 