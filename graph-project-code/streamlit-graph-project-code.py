import pandas as pd
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
from community import community_louvain
import numpy as np
import time


import requests
url = 'https://raw.githubusercontent.com/aleeeec02/wattzfinder/main/data/Electric_Vehicle_Population_Data_3000_FINAL.csv'


def cargar_datos(num_rows=100):
    url = 'https://raw.githubusercontent.com/aleeeec02/wattzfinder/main/data/Electric_Vehicle_Population_Data_3000_FINAL.csv'
    local_path = os.path.join('..', 'data', 'Electric_Vehicle_Population_Data_3000_FINAL.csv')

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        df = pd.read_csv(url, delimiter=';', nrows=num_rows)
        st.success("Datos cargados desde GitHub.")
        return df
    except requests.RequestException:
        st.warning("No se pudo acceder a los datos en línea. Intentando cargar datos locales...")
        try:
            df = pd.read_csv(local_path, delimiter=';', nrows=num_rows)
            st.success("Datos cargados desde archivo local.")
            return df
        except Exception as e:
            st.error(f"No se pudieron cargar los datos locales: {e}")
            return pd.DataFrame()



def construir_grafo(df):
    G = nx.Graph()
    for _, fila in df.iterrows():
        G.add_node(fila['VIN (1-10)'], msrp=fila['Base MSRP'], etiqueta=f"{fila['Make']} {fila['Model']}")
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            peso = abs(df.iloc[i]['Base MSRP'] - df.iloc[j]['Base MSRP'])
            G.add_edge(df.iloc[i]['VIN (1-10)'], df.iloc[j]['VIN (1-10)'], weight=peso)
    return G


def mostrar_vehiculo_seleccionado(df, vin):
    vehiculo = df[df['VIN (1-10)'] == vin].iloc[0]
    st.subheader(f"{vehiculo['Make']} {vehiculo['Model']} {vehiculo['Model Year']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio Base", f"${vehiculo['Base MSRP']:,.2f}")
    col2.metric("Rango Eléctrico", f"{vehiculo['Electric Range']} millas")
    col3.metric("Tipo", vehiculo['Electric Vehicle Type'])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Marca:** {vehiculo['Make']}")
        st.markdown(f"**Modelo:** {vehiculo['Model']}")
        st.markdown(f"**Año:** {vehiculo['Model Year']}")
        st.markdown(f"**Tipo:** {vehiculo['Electric Vehicle Type']}")
    with col2:
        st.markdown(f"**Rango Eléctrico:** {vehiculo['Electric Range']} millas")
        st.markdown(f"**Precio Base:** ${vehiculo['Base MSRP']:,.2f}")
        st.markdown(f"**Ciudad:** {vehiculo['City']}")
        st.markdown(f"**Estado:** {vehiculo['State']}")




def aplicar_filtros(df, rango_min, rango_max, precio_min, precio_max):
    return df[(df['Electric Range'] >= rango_min) & 
              (df['Electric Range'] <= rango_max) & 
              (df['Base MSRP'] >= precio_min) & 
              (df['Base MSRP'] <= precio_max)]


def dijkstra_algo(G, df, vin_inicio, n=5):
    longitudes_camino = nx.single_source_dijkstra_path_length(G, source=vin_inicio, weight='weight')
    carros_ordenados = sorted(longitudes_camino.items(), key=lambda x: x[1])
    recomendaciones = carros_ordenados[1:n+1]

    resultados = []
    for vin, diferencia in recomendaciones:
        vehiculo = df[df['VIN (1-10)'] == vin].iloc[0]
        resultados.append({
            'VIN': vin,
            'Make': vehiculo['Make'],
            'Model': vehiculo['Model'],
            'Year': vehiculo['Model Year'],
            'Electric Range': vehiculo['Electric Range'],
            'Base MSRP': vehiculo['Base MSRP'],
            'City': vehiculo['City'],
            'State': vehiculo['State'],
            'Electric Vehicle Type': vehiculo['Electric Vehicle Type'],
            'Diferencia MSRP': diferencia
        })
    return resultados


def detectar_comunidades(G):
    particion = community_louvain.best_partition(G)
    return particion

def vecinos_mas_cercanos(G, vin_inicio, k=5):
    distancias = nx.single_source_dijkstra_path_length(G, vin_inicio, weight='weight')
    vecinos = sorted(distancias.items(), key=lambda x: x[1])[1:k+1]
    return vecinos

def visualizar_grafo(G, destacados=None, comunidades=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G)
    if comunidades:
        nx.draw(G, pos, node_color=[comunidades[node] for node in G.nodes()], 
                with_labels=True, cmap=plt.cm.rainbow, node_size=300, ax=ax)
    else:
        nx.draw(G, pos, with_labels=True, node_color='deepskyblue', edge_color='magenta', node_size=300, ax=ax)
    if destacados:
        nx.draw_networkx_nodes(G, pos, nodelist=destacados, node_color='red', node_size=500, ax=ax)
    plt.title("Grafo de Vehículos Eléctricos")
    return fig



def main():
    st.title('Wattzfinder: Sistema de Recomendación de Vehículos Eléctricos')
    
    file_path_datos = '../data/Electric_Vehicle_Population_Data_3000_FINAL.csv'

    st.sidebar.header("Configuración de Datos")
    num_rows = st.sidebar.slider('Número de filas a cargar', min_value=10, max_value=3000, value=500, step=100)

    carga_mensaje = st.empty()
    carga_mensaje.info(f"Cargando {num_rows} filas de datos...")


    df = cargar_datos(file_path_datos, num_rows=num_rows)
    time.sleep(1)


    carga_mensaje.success(f"Se han cargado {len(df)} filas de datos.")
    
    if not df.empty:
        st.sidebar.header("Filtros y Opciones")
        
        rango_min, rango_max = st.sidebar.slider(
            'Rango Eléctrico (millas)', 
            float(df['Electric Range'].min()), 
            float(df['Electric Range'].max()), 
            (float(df['Electric Range'].min()), float(df['Electric Range'].max()))
        )
        
        precio_min, precio_max = st.sidebar.slider(
            'Precio Base (USD)', 
            float(df['Base MSRP'].min()), 
            float(df['Base MSRP'].max()), 
            (float(df['Base MSRP'].min()), float(df['Base MSRP'].max()))
        )
        

        num_recomendaciones = st.sidebar.slider('Número de recomendaciones', min_value=1, max_value=10, value=5)
        
        df_filtrado = aplicar_filtros(df, rango_min, rango_max, precio_min, precio_max)
        
        G = construir_grafo(df_filtrado)
        
        opcion = st.sidebar.selectbox(
            "Seleccione un tipo de análisis:",
            ["Recomendaciones Dijkstra", "Detección de Comunidades", "Vecinos Más Cercanos"]
        )
        
        vin_seleccionado = st.selectbox('Seleccione un VIN de vehículo:', df_filtrado['VIN (1-10)'].unique())
        
        if opcion == "Recomendaciones Dijkstra":
            if st.button('Buscar vehículos similares'):
                mostrar_vehiculo_seleccionado(df_filtrado, vin_seleccionado)
                recomendaciones = dijkstra_algo(G, df_filtrado, vin_seleccionado, n=num_recomendaciones)
                st.write(f"Top {num_recomendaciones} vehículos recomendados según la similitud en MSRP:")
                for recomendacion in recomendaciones:
                    with st.expander(f"{recomendacion['Make']} {recomendacion['Model']} {recomendacion['Year']}"):
                        st.write(f"VIN: {recomendacion['VIN']}")
                        st.write(f"Marca: {recomendacion['Make']}")
                        st.write(f"Modelo: {recomendacion['Model']}")
                        st.write(f"Año: {recomendacion['Year']}")
                        st.write(f"Autonomía eléctrica: {recomendacion['Electric Range']} millas")
                        st.write(f"Precio base: ${recomendacion['Base MSRP']:,.2f}")
                        st.write(f"Ciudad: {recomendacion['City']}")
                        st.write(f"Estado: {recomendacion['State']}")
                        st.write(f"Tipo de vehículo eléctrico: {recomendacion['Electric Vehicle Type']}")
                        st.write(f"Diferencia de MSRP: ${recomendacion['Diferencia MSRP']:,.2f}")
                
                fig = visualizar_grafo(G, destacados=[r['VIN'] for r in recomendaciones] + [vin_seleccionado])
                st.pyplot(fig)

        elif opcion == "Detección de Comunidades":
            if st.button('Detectar Comunidades'):
                comunidades = detectar_comunidades(G)
                st.write("Comunidades detectadas:")
                for comunidad in set(comunidades.values()):
                    vins_comunidad = [vin for vin, com in comunidades.items() if com == comunidad]
                    st.write(f"Comunidad {comunidad}: {len(vins_comunidad)} vehículos")
                
                fig = visualizar_grafo(G, comunidades=comunidades)
                st.pyplot(fig)
        
        elif opcion == "Vecinos Más Cercanos":
            if st.button('Encontrar Vecinos Más Cercanos'):
                vecinos = vecinos_mas_cercanos(G, vin_seleccionado)
                st.write("Vecinos más cercanos:")
                for vin, distancia in vecinos:
                    st.write(f"VIN: {vin}, Distancia: {distancia:.2f}")
                
                fig = visualizar_grafo(G, destacados=[vin for vin, _ in vecinos] + [vin_seleccionado])
                st.pyplot(fig)
    
    else:
        st.error("Los datos no están disponibles.")

if __name__ == "__main__":
    main()
