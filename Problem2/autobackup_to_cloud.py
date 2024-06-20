import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure logging
logging.basicConfig(filename='backup_to_s3.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# AWS S3 bucket name
bucket_name = 'mybucketpanda'

# Source directory to be backed up
source_dir = 'D:\Code\Docker\\test'

# Initialize S3 client
s3 = boto3.client('s3')

def upload_file_to_s3(file_path, bucket_name, s3_path):
    try:
        s3.upload_file(file_path, bucket_name, s3_path)
        logging.info(f'Successfully uploaded {file_path} to {bucket_name}/{s3_path}')
        return True
    except FileNotFoundError:
        logging.error(f'File not found: {file_path}')
        return False
    except NoCredentialsError:
        logging.error('Credentials not available')
        return False
    except PartialCredentialsError:
        logging.error('Incomplete credentials')
        return False
    except Exception as e:
        logging.error(f'Failed to upload {file_path}. Error: {str(e)}')
        return False

def backup_directory_to_s3(source_dir, bucket_name):
    try:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                s3_path = os.path.relpath(file_path, source_dir)
                upload_file_to_s3(file_path, bucket_name, s3_path)
        
        logging.info('Backup completed successfully.')
        return True
    except Exception as e:
        logging.error(f'Backup failed. Error: {str(e)}')
        return False

def main():
    print(f'Starting backup process from {source_dir} to S3 bucket: {bucket_name}...')
    success = backup_directory_to_s3(source_dir, bucket_name)

    if success:
        print('Backup completed successfully.')
    else:
        print('Backup failed. Check log for details.')

if __name__ == '__main__':
    main()
