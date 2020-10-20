import json
import logging
import shutil

import boto3
import botocore
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

AWS_KEY_ID = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = ""
FOLDER_NAME = ""
AWS_SESSION_TOKEN = ""


# Read the .json file to get the config.
def readJson():
    global AWS_KEY_ID, AWS_SECRET_KEY, BUCKET_NAME, FOLDER_NAME, AWS_SESSION_TOKEN
    with open('config.json') as config_file:
        data = json.load(config_file)
        AWS_KEY_ID = data['aws_key_id']
        AWS_SECRET_KEY = data['aws_secret_key']
        AWS_SESSION_TOKEN = data['aws_session_token']
        BUCKET_NAME = data['bucket_name']
        FOLDER_NAME = data['folder_name']
        config_file.close()


def get_s3(region=None):
    """Get a Boto 3 S3 resource with a specific Region or with your default Region."""
    readJson()
    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN)

    if not region or s3_resource.meta.client.meta.region_name == region:
        return s3_resource
    else:
        return boto3.resource('s3', region_name=region)


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    readJson()

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY_ID,
                                     aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY_ID,
                                     aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN,
                                     region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def bucket_exists(bucket_name):
    """
    Determine whether a bucket with the specified name exists.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The name of the bucket to check.
    :return: True when the bucket exists; otherwise, False.
    """
    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        logger.info("Bucket %s exists.", bucket_name)
        exists = True
    except ClientError:
        logger.warning("Bucket %s doesn't exist or you don't have access to it.",
                       bucket_name)
        exists = False
    return exists


def get_buckets():
    """
    Get the buckets in all Regions for the current account.

    Usage is shown in usage_demo at the end of this module.

    :return: The list of buckets.
    """
    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    try:
        buckets = list(s3.buckets.all())
        for k in buckets:
            print("Got buckets:", k)
    except ClientError:
        logger.exception("Couldn't get buckets.")
        raise
    else:
        return buckets


def delete_bucket(bucket_name):
    """
    Delete a bucket. The bucket must be empty or an error is raised.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The bucket's name that you want to delete
    """

    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)

    bucket = s3.Bucket(bucket_name)

    try:
        bucket.delete()
        bucket.wait_until_not_exists()
        logger.info("Bucket %s successfully deleted.", bucket.name)
    except ClientError:
        logger.exception("Couldn't delete bucket %s.", bucket.name)
        raise


# -----------------------------------------------------------------------------------------------------------------------


def put_object(bucket_name, object_key, data):
    """
    Upload data to a bucket and identify it with the specified object key.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The bucket's name that receive the data.
    :param object_key: The key of the object in the bucket.
    :param data: The data to upload. This can either be bytes or a string. When this
                 argument is a string, it is interpreted as a file name, which is
                 opened in read bytes mode.
    """
    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    bucket = s3.Bucket(bucket_name)

    put_data = data
    if isinstance(data, str):
        try:
            put_data = open(data, 'rb')
        except IOError:
            logger.exception("Expected file name or binary data, got '%s'.", data)
            raise

    try:
        obj = bucket.Object(object_key)
        obj.put(Body=put_data)
        obj.wait_until_exists()
        logger.info("Put object '%s' to bucket '%s'.", object_key, bucket.name)
    except ClientError:
        logger.exception("Couldn't put object '%s' to bucket '%s'.",
                         object_key, bucket.name)
        raise
    finally:
        if getattr(put_data, 'close', None):
            put_data.close()


def get_object(bucket_name, object_key):
    """
    Gets an object from a bucket.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The bucket that contains the object.
    :param object_key: The key of the object to retrieve.
    :return: The object data in bytes.
    """

    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    bucket = s3.Bucket(bucket_name)

    try:
        body = bucket.Object(object_key).get()['Body'].read()
        print("Got object", object_key, "from bucket", bucket.name)
    except ClientError:
        logger.exception(("Couldn't get object '%s' from bucket '%s'.",
                          object_key, bucket.name))
        raise
    else:
        return body


def list_objects(bucket_name, prefix=None):
    """
    Lists the objects in a bucket, optionally filtered by a prefix.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The bucket to query.
    :param prefix: When specified, only objects that start with this prefix are listed.
    :return: The list of objects.
    """
    readJson()
    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    bucket = s3.Bucket(bucket_name)

    try:
        if not prefix:
            objects = list(bucket.objects.all())
        else:
            objects = list(bucket.objects.filter(Prefix=prefix))
        for k in objects:
            print("Got object", k.key, "from bucket", bucket_name)

    except ClientError:
        logger.exception("Couldn't get objects for bucket '%s'.", bucket.name)
        raise
    else:
        return objects


def copy_object(source_bucket, source_object_key, dest_bucket, dest_object_key):
    """
    Copies an object from one bucket to another.

    Usage is shown in usage_demo at the end of this module.

    :param source_bucket: The bucket that contains the source object.
    :param source_object_key: The key of the source object.
    :param dest_bucket: The bucket that receives the copied object.
    :param dest_object_key: The key of the copied object.
    :return: The new copy of the object.
    """

    try:
        obj = dest_bucket.Object(dest_object_key)
        obj.copy_from(CopySource={
            'Bucket': source_bucket.name,
            'Key': source_object_key
        })
        obj.wait_until_exists()
        logger.info("Copied object from %s/%s to %s/%s.",
                    source_bucket.name, source_object_key,
                    dest_bucket.name, dest_object_key)
    except ClientError:
        logger.exception("Couldn't copy object from %s/%s to %s/%s.",
                         source_bucket.name, source_object_key,
                         dest_bucket.name, dest_object_key)
        raise
    else:
        return obj


def delete_object(bucket_name, object_key):
    """
    Removes an object from a bucket.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The bucket that contains the object.
    :param object_key: The key of the object to delete.
    """
    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    bucket = s3.Bucket(bucket_name)

    try:
        obj = bucket.Object(object_key)
        obj.delete()
        obj.wait_until_not_exists()
        print("Deleted object", object_key, "from bucket", bucket.name)
    except ClientError:
        logger.exception("Couldn't delete object '%s' from bucket '%s'.",
                         object_key, bucket.name)
        raise


def download_file(bucket_name, file_key, file_name):

    readJson()

    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.download_file(file_key, file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    else:
        shutil.move(file_name, FOLDER_NAME)
        return


def upload_file(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
    """

    readJson()

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=AWS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_KEY, aws_session_token=AWS_SESSION_TOKEN)

    try:

        s3_client.upload_file(file_name, bucket_name, object_name)

    except ClientError as e:
        logging.error(e)
        return False
    print('Done')
    return True
