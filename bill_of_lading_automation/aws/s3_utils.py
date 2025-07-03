import boto3

class S3Client:
    def __init__(self, aws_region):
        self.s3 = boto3.client('s3', region_name=aws_region)

    def upload_file(self, file_path, bucket, key):
        self.s3.upload_file(file_path, bucket, key)

    def download_file(self, bucket, key, file_path):
        self.s3.download_file(bucket, key, file_path)

    def list_files(self, bucket, prefix):
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj['Key'] for obj in response.get('Contents', [])] 