from .secrets import access_key, secret_access_key
import boto3
import os

s3_handler = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key,
    )

