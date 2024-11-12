import streamlit as st
import pandas as pd
import altair as alt
import json
from urllib.error import URLError
from urllib.parse import urlparse
from config.AWS_Client import create_client

st.set_page_config(page_title="GeoJSON DataFrame Demo", page_icon="📊")

st.markdown("# GeoJSON DataFrame Demo")
st.sidebar.header("GeoJSON DataFrame Demo")
st.write(
    """Este demo muestra cómo usar `st.write` para visualizar un DataFrame de Pandas
    con datos provenientes de un archivo GeoJSON almacenado en S3."""
)

# Crear cliente S3
s3_client = create_client('s3')


def read_geojson_from_s3(s3_client, bucket_name, object_key):
    try:

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        

        file_content = response['Body'].read().decode('utf-8')
        

        data = json.loads(file_content)
        

        features = data['features']
        records = []
        
  
        for feature in features:
            properties = feature['properties']
            geometry = feature['geometry']
            record = properties.copy()  
            

            if geometry['type'] == 'Point':
                record['latitud'] = geometry['coordinates'][1]
                record['longitud'] = geometry['coordinates'][0]
            
            records.append(record)
        

        df = pd.DataFrame(records)
        return df
    
    except Exception as e:
        st.error(f"Error al leer el archivo desde S3: {e}")
        return None


bucket_name = 'equiporocket'
object_key = 'pa_brincar/atractivos_turisticos.geojson'


df = read_geojson_from_s3(s3_client, bucket_name, object_key)


if df is not None:
    st.write("### Datos de Atractivos Turísticos en Medellín", df)

 
    st.write("### Primeros registros", df.head())


    if 'imperdible' in df.columns:
        imperdible_count = df['imperdible'].value_counts().reset_index()
        imperdible_count.columns = ['Imperdible', 'Cantidad']
        
        imperdible_chart = (
            alt.Chart(imperdible_count)
            .mark_bar()
            .encode(
                x='Imperdible:N',
                y='Cantidad:Q',
                color='Imperdible:N',
                tooltip=['Imperdible:N', 'Cantidad:Q']
            )
            .properties(
                title="Comparación de Atractivos 'Imperdibles' vs 'No Imperdibles'"
            )
        )
        st.altair_chart(imperdible_chart, use_container_width=True)

else:
    st.error("No se pudo cargar el DataFrame desde el archivo GeoJSON.")
