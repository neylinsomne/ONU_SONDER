import boto3
from botocore.exceptions import ClientError

def create_client(service:str):
    client = boto3.client(

    service, 
    region_name="us-west-2",  
    aws_access_key_id="AKIA6GPQ3JXO7LFHWFMI",  
    aws_secret_access_key="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")

    print(f'conexion exitosa {service}')
    return client