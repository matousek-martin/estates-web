import os
import json
import base64
from typing import Dict

import boto3
from botocore.client import ClientError


class Config(object):
    AWS_REGION = 'eu-central-1'
    AWS_SECRET_NAME = 'estates-rds'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'security_here_is_a_joke'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        secret = self.__get_secret(secret_name=self.AWS_SECRET_NAME, region_name=self.AWS_REGION)
        return "postgresql+psycopg2://{username}:{password}@{host}:{port}".format(**secret)

    @staticmethod
    def __get_secret(secret_name: str, region_name: str) -> Dict:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
        )

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            elif e.response['Error']['Code'] == 'DecryptionFailure':
                print("The requested secret can't be decrypted using the provided KMS key:", e)
            elif e.response['Error']['Code'] == 'InternalServiceError':
                print("An error occurred on service side:", e)
        else:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary,
            # only one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            return json.loads(secret)
