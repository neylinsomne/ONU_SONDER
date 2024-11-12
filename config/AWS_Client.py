import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def create_client(service:str):
    client = boto3.client(

    service, 
    region_name=os.getenv("REGION"), 
    aws_access_key_id=os.getenv("KEY_ID"),  
    aws_secret_access_key=os.getenv("KEY_ACCESS")
    )

    print(f'conexion exitosa {service}')
    return client