import logging
import boto3
from botocore.exceptions import ClientError
import os
from key import ACCESS_KEY,SECRET_KEY,SESSION_TOKEN

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
                                    aws_secret_access_key=SECRET_KEY,
                                    aws_session_token = SESSION_TOKEN
                                    )
            #,aws_session_token=SESSION_TOKEN
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region,
                                    aws_access_key_id=ACCESS_KEY,
                                    aws_secret_access_key=SECRET_KEY,
                                     aws_session_token=SESSION_TOKEN
                                    )
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_existing_buckets():
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN
                    )#aws_session_token=SESSION_TOKEN
    response = s3.list_buckets()
    # Output the bucket names
    print('Existing buckets:')

    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

def delete_objects_from_s3(file_path,kind):
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                             aws_secret_access_key=SECRET_KEY,
                             aws_session_token=SESSION_TOKEN
                             )
    try:
      result = s3_client.delete_object(Bucket="modelplex-"+kind, Key=file_path)
    except ClientError as e:
      raise Exception( "boto3 client error in delete_objects_from_s3 function: " + e.__str__())
    except Exception as e:
      raise Exception( "Unexpected error in delete_objects_from_s3 function of s3 helper: " + e.__str__())

def upload_file(file_name, bucket, object_name=None, extrainfo = None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)
    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                             aws_session_token=SESSION_TOKEN
                    )
    try:
        if extrainfo is None:
            response = s3_client.upload_file(file_name, bucket, object_name)
        else:
            response = s3_client.upload_file(file_name, bucket, object_name,extrainfo)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_data(path,name,kind):
    s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN
                    )
    s3.download_file("modelplex-"+kind, name, path)

def upload_data(path,name,kind):
    obj_name = name
    upload_file(path,"modelplex-"+kind,obj_name)
    return obj_name

info = dict()
info["name"] = "cifa10"
info["kind"] = "image data set"
info["owner"] = "root"
remote_dir = "sagemaker/DEMO-xgboost-dm/output/xgboost-2022-04-16-07-59-27-393/output/model.tar.gz"
if __name__ == '__main__':
    #create_bucket("modelplex-model")
    list_existing_buckets()
    #upload_file("cifar10.zip","modelplexdata",extrainfo = {"Metadata":info})
    #download_file("model.tar.gz","lhwbucket",remote_dir)