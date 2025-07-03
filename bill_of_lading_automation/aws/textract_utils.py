import boto3
import time

class TextractClient:
    def __init__(self, aws_region):
        self.client = boto3.client('textract', region_name=aws_region)

    def start_document_text_detection(self, s3_bucket, s3_key):
        response = self.client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_key
                }
            }
        )
        return response['JobId']

    def get_document_text_detection(self, job_id):
        while True:
            response = self.client.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(2)
        if status == 'SUCCEEDED':
            return response['Blocks']
        else:
            raise Exception(f"Textract job failed: {response}") 