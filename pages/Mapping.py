import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from config.AWS_Client import create_client

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """Este demo muestra cómo usar `st.pydeck_chart` para visualizar datos geoespaciales."""
)

# Crear cliente S3
s3_client = create_client('s3')

# Función para leer el archivo GeoJSON desde S3 y convertirlo a un DataFrame
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

# Nombre del bucket y clave del objeto
bucket_name = 'equiporocket'
object_key = 'pa_brincar/atractivos_turisticos.geojson'

# Leer datos desde S3 y convertirlos en un DataFrame
df = read_geojson_from_s3(s3_client, bucket_name, object_key)

# Si el DataFrame se cargó correctamente, mostrar el mapa
if df is not None and 'latitud' in df.columns and 'longitud' in df.columns:
    # Ajuste de la vista inicial del mapa basado en el centroide de los puntos
    initial_view_state = pdk.ViewState(
        latitude=df['latitud'].mean(),
        longitude=df['longitud'].mean(),
        zoom=12,
        pitch=50,
    )

    # Crear una capa de Scatterplot para mostrar los atractivos turísticos
    tourist_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitud", "latitud"],
        get_color=[0, 128, 255, 160],
        get_radius=100,
        pickable=True,
        tooltip=True,
    )

    # Configurar y renderizar el mapa
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=initial_view_state,
            layers=[tourist_layer],
            tooltip={"text": "{nombre_sitio}\n{comuna}\n{tipo_atractivo}"}
        )
    )
else:
    st.error("No se pudieron cargar los datos geoespaciales para el mapa.")
