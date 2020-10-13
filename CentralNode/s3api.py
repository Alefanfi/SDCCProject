import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

s3_resource = boto3.resource('s3')


def get_s3(region=None):
    """Get a Boto 3 S3 resource with a specific Region or with your default Region."""
    global s3_resource
    if not region or s3_resource.meta.client.meta.region_name == region:
        return s3_resource
    else:
        return boto3.resource('s3', region_name=region)


def create_bucket(name, region=None):
    """
    Create an Amazon S3 bucket with the specified name and in the specified Region.

    Usage is shown in usage_demo at the end of this module.

    :param name: The name of the bucket to create. This name must be globally unique
                 and must adhere to bucket naming requirements.
    :param region: The Region in which to create the bucket. If this is not specified,
                   the Region configured in your shared credentials is used. If no
                   Region is configured, 'us-east-1' is used.
    :return: The newly created bucket.
    """
    s3 = get_s3(region)

    try:
        if region:
            bucket = s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        else:
            bucket = s3.create_bucket(Bucket=name)

        bucket.wait_until_exists()

        logger.info("Created bucket '%s' in region=%s", bucket.name,
                    s3.meta.client.meta.region_name)
    except ClientError as error:
        logger.exception("Couldn't create bucket named '%s' in region=%s.",
                         name, region)
        if error.response['Error']['Code'] == 'IllegalLocationConstraintException':
            logger.error("When the session Region is anything other than us-east-1, "
                         "you must specify a LocationConstraint that matches the "
                         "session Region. The current session Region is %s and the "
                         "LocationConstraint Region is %s.",
                         s3.meta.client.meta.region_name, region)
        raise error
    else:
        return bucket


def bucket_exists(bucket_name):
    """
    Determine whether a bucket with the specified name exists.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The name of the bucket to check.
    :return: True when the bucket exists; otherwise, False.
    """
    s3 = get_s3()
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
    s3 = get_s3()
    try:
        buckets = list(s3.buckets.all())
        logger.info("Got buckets: %s.", buckets)
    except ClientError:
        logger.exception("Couldn't get buckets.")
        raise
    else:
        return buckets


def delete_bucket(bucket):
    """
    Delete a bucket. The bucket must be empty or an error is raised.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket to delete.
    """
    try:
        bucket.delete()
        bucket.wait_until_not_exists()
        logger.info("Bucket %s successfully deleted.", bucket.name)
    except ClientError:
        logger.exception("Couldn't delete bucket %s.", bucket.name)
        raise

# -----------------------------------------------------------------------------------------------------------------------


def put_object(bucket, object_key, data):
    """
    Upload data to a bucket and identify it with the specified object key.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket to receive the data.
    :param object_key: The key of the object in the bucket.
    :param data: The data to upload. This can either be bytes or a string. When this
                 argument is a string, it is interpreted as a file name, which is
                 opened in read bytes mode.
    """
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


def get_object(bucket, object_key):
    """
    Gets an object from a bucket.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket that contains the object.
    :param object_key: The key of the object to retrieve.
    :return: The object data in bytes.
    """
    try:
        body = bucket.Object(object_key).get()['Body'].read()
        logger.info("Got object '%s' from bucket '%s'.", object_key, bucket.name)
    except ClientError:
        logger.exception(("Couldn't get object '%s' from bucket '%s'.",
                          object_key, bucket.name))
        raise
    else:
        return body


def list_objects(bucket, prefix=None):
    """
    Lists the objects in a bucket, optionally filtered by a prefix.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket to query.
    :param prefix: When specified, only objects that start with this prefix are listed.
    :return: The list of objects.
    """
    try:
        if not prefix:
            objects = list(bucket.objects.all())
        else:
            objects = list(bucket.objects.filter(Prefix=prefix))
        logger.info("Got objects %s from bucket '%s'",
                    [o.key for o in objects], bucket.name)
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


def delete_object(bucket, object_key):
    """
    Removes an object from a bucket.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket that contains the object.
    :param object_key: The key of the object to delete.
    """
    try:
        obj = bucket.Object(object_key)
        obj.delete()
        obj.wait_until_not_exists()
        logger.info("Deleted object '%s' from bucket '%s'.", object_key, bucket.name)
    except ClientError:
        logger.exception("Couldn't delete object '%s' from bucket '%s'.",
                         object_key, bucket.name)
        raise
