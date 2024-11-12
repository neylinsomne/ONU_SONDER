import streamlit as st
import random
import time
import boto3
import json
from botocore.exceptions import ClientError
from config.AWS_Client import create_client

# Establecer las credenciales de AWS de manera programática
client = create_client("bedrock-runtime")



# Configurar la página
st.set_page_config(page_title="Hello", page_icon="👋")
st.write("# Welcome from AIrepa! 🤖")
st.sidebar.success("Select a demo above.")

# Inicializar el estado de la sesión si no está inicializado
if "messages" not in st.session_state:
    st.session_state.messages = [] 


def call_titan(prompt):
    model_id = "amazon.titan-text-express-v1" 
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    try:

        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return "Sorry, I couldn't get a response from the model."


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar la entrada del usuario
if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = call_titan(prompt)
        st.markdown(response)

 
    st.session_state.messages.append({"role": "assistant", "content": response})
