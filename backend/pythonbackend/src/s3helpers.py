import logging
import boto3
from botocore.exceptions import ClientError


def upload_image(file_name, bucket_name, upload_name, mimetype):
    s3_client = boto3.client("s3")
    try:
        with open(file_name, "rb") as f:
            response = s3_client.put_object(
                ACL="public-read",
                Body=f,
                Bucket=bucket_name,
                ContentType=mimetype,
                Key=upload_name,
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_url(object_name, bucket_name, bucket_region):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    return f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{object_name}"
