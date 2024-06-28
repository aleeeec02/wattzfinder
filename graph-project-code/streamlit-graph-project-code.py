import pandas as pd
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
from community import community_louvain
import numpy as np
import time
import requests
import os
from collections import deque


def cargar_datos(num_rows=100):
    local_path = os.path.join('..', 'data', 'Electric_Vehicle_Population_Data_3000_FINAL.csv')
    url = 'https://raw.githubusercontent.com/aleeeec02/wattzfinder/main/data/Electric_Vehicle_Population_Data_3000_FINAL.csv'

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



def aplicar_filtros(df, rango_min, rango_max, precio_min, precio_max, marcas):
    df_filtrado = df[
        (df['Electric Range'] >= rango_min) & 
        (df['Electric Range'] <= rango_max) & 
        (df['Base MSRP'] >= precio_min) & 
        (df['Base MSRP'] <= precio_max)
    ]

    if marcas:
        df_filtrado = df_filtrado[df_filtrado['Make'].isin(marcas)]
    
    return df_filtrado



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




def bfs_vehiculos_similares(G, df, query, num_resultados=6, offset=0):
    query = query.lower()
    resultados = []
    visitados = set()

    def calcular_puntuacion(vehiculo):
        puntuacion = 0
        nombre_completo = f"{vehiculo['Make']} {vehiculo['Model']} {vehiculo['Model Year']}".lower()
        if query in nombre_completo:
            puntuacion += 5
        if query in vehiculo['Make'].lower():
            puntuacion += 3
        if query in vehiculo['Model'].lower():
            puntuacion += 2
        if query in str(vehiculo['Model Year']).lower():
            puntuacion += 1
        if query in vehiculo['VIN (1-10)'].lower():
            puntuacion += 4
        return puntuacion

    for start_node in G.nodes():
        if start_node in visitados:
            continue
        
        cola = deque([(start_node, 0)])
        while cola:
            node, distancia = cola.popleft()
            if node not in visitados:
                visitados.add(node)
                vehiculo = df[df['VIN (1-10)'] == node].iloc[0]
                puntuacion = calcular_puntuacion(vehiculo)
                
                if puntuacion > 0:
                    resultados.append((node, distancia, puntuacion))
                
                for vecino in G.neighbors(node):
                    if vecino not in visitados:
                        cola.append((vecino, distancia + 1))
        
        if len(resultados) >= num_resultados * 3:
            break

    resultados_ordenados = sorted(resultados, key=lambda x: (-x[2], x[1]))
    return resultados_ordenados[offset:offset+num_resultados]


def bfs_vehiculos_similares(G, df, query, num_resultados=6, offset=0):
    query = query.lower()
    resultados = []
    visitados = set()

    def calcular_puntuacion(vehiculo):
        puntuacion = 0
        nombre_completo = f"{vehiculo['Make']} {vehiculo['Model']} {vehiculo['Model Year']}".lower()
        if query in nombre_completo:
            puntuacion += 5
        if query in vehiculo['Make'].lower():
            puntuacion += 3
        if query in vehiculo['Model'].lower():
            puntuacion += 2
        if query in str(vehiculo['Model Year']).lower():
            puntuacion += 1
        if query in vehiculo['VIN (1-10)'].lower():
            puntuacion += 4
        return puntuacion

    for start_node in G.nodes():
        if start_node in visitados:
            continue
        
        cola = deque([(start_node, 0)])
        while cola:
            node, distancia = cola.popleft()
            if node not in visitados:
                visitados.add(node)
                vehiculo = df[df['VIN (1-10)'] == node].iloc[0]
                puntuacion = calcular_puntuacion(vehiculo)
                
                if puntuacion > 0:
                    resultados.append((node, distancia, puntuacion))
                
                for vecino in G.neighbors(node):
                    if vecino not in visitados:
                        cola.append((vecino, distancia + 1))
        
        if len(resultados) >= num_resultados * 3:
            break

    resultados_ordenados = sorted(resultados, key=lambda x: (-x[2], x[1]))
    return resultados_ordenados[offset:offset+num_resultados]

def mostrar_resultados(df, resultados):
    for vin, _, _ in resultados:
        vehiculo = df[df['VIN (1-10)'] == vin].iloc[0]
        with st.expander(f"{vehiculo['Make']} {vehiculo['Model']} {vehiculo['Model Year']}"):
            st.write(f"VIN: {vin}")
            st.write(f"Marca: {vehiculo['Make']}")
            st.write(f"Modelo: {vehiculo['Model']}")
            st.write(f"Año: {vehiculo['Model Year']}")
            st.write(f"Autonomía eléctrica: {vehiculo['Electric Range']} millas")
            st.write(f"Precio base: ${vehiculo['Base MSRP']:,.2f}")
            st.write(f"Tipo de vehículo eléctrico: {vehiculo['Electric Vehicle Type']}")


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

def guardar_estado_sesion(key):
    def inner():
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]
    return inner



def cargar_estado_sesion(key, default):
    return st.session_state.get(key, default)




def main():
    if 'num_rows' not in st.session_state:
        st.session_state['num_rows'] = 100
    if 'marcas_seleccionadas' not in st.session_state:
        st.session_state['marcas_seleccionadas'] = []
    if 'rango_min' not in st.session_state:
        st.session_state['rango_min'] = 0
    if 'rango_max' not in st.session_state:
        st.session_state['rango_max'] = 300
    if 'precio_min' not in st.session_state:
        st.session_state['precio_min'] = 0
    if 'precio_max' not in st.session_state:
        st.session_state['precio_max'] = 100000
    if 'num_recomendaciones' not in st.session_state:
        st.session_state['num_recomendaciones'] = 5

    st.title('Wattzfinder: Sistema de Recomendación de Vehículos Eléctricos')
    

    st.sidebar.header("Configuración de Datos")
    num_rows = st.sidebar.number_input(
                'Número de filas a cargar', 
                min_value=10, 
                max_value=3000, 
                value=st.session_state['num_rows'],
                step=1,
                on_change=guardar_estado_sesion('num_rows')
            )


    carga_mensaje = st.empty()
    carga_mensaje.info(f"Cargando {num_rows} filas de datos...")

    df = cargar_datos(num_rows=num_rows)
    time.sleep(1)
    carga_mensaje.success(f"Se han cargado {len(df)} filas de datos.")
    



    if not df.empty:
        st.sidebar.header("Filtros y Opciones")
        
        todas_las_marcas = sorted(df['Make'].unique())
        marcas_seleccionadas = st.sidebar.multiselect(
            'Seleccione las marcas',
            options=todas_las_marcas,
            default=cargar_estado_sesion('marcas_seleccionadas', todas_las_marcas),
            on_change=guardar_estado_sesion('marcas_seleccionadas')
        )


        rango_min, rango_max = st.sidebar.slider(
            'Rango Eléctrico (millas)', 
            float(df['Electric Range'].min()), 
            float(df['Electric Range'].max()), 
            value=cargar_estado_sesion('rango_electrico', (float(df['Electric Range'].min()), float(df['Electric Range'].max()))),
            on_change=guardar_estado_sesion('rango_electrico')
        )
        


        precio_min, precio_max = st.sidebar.slider(
            'Precio Base (USD)', 
            float(df['Base MSRP'].min()), 
            float(df['Base MSRP'].max()), 
            value=cargar_estado_sesion('rango_precio', (float(df['Base MSRP'].min()), float(df['Base MSRP'].max()))),
            on_change=guardar_estado_sesion('rango_precio')
        )

        

        num_recomendaciones = st.sidebar.slider('Número de recomendaciones', 
                    min_value=1, 
                    max_value=10, 
                    value=cargar_estado_sesion('num_recomendaciones', 5),
                    on_change=guardar_estado_sesion('num_recomendaciones'))



        df_filtrado = aplicar_filtros(df, rango_min, rango_max, precio_min, precio_max, marcas_seleccionadas)

        st.write(f"Número de vehículos después de filtrar: {len(df_filtrado)}")
        
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
                st.write(f"**Top {num_recomendaciones} vehículos recomendados según la similitud en MSRP:**")
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
                    with st.expander(f"VIN: {vin} - Distancia: {distancia:.2f}"):
                        vehiculo = df[df['VIN (1-10)'] == vin].iloc[0]
                        st.write(f"**VIN:** {vin}")
                        st.write(f"**Distancia:** {distancia:.2f} millas")
                        st.write(f"**Marca:** {vehiculo['Make']}")
                        st.write(f"**Modelo:** {vehiculo['Model']}")
                        st.write(f"**Año:** {vehiculo['Model Year']}")
                        st.write(f"**Autonomía Eléctrica:** {vehiculo['Electric Range']} millas")
                        st.write(f"**Precio Base:** ${vehiculo['Base MSRP']:,.2f}")
                        st.write(f"**Ciudad:** {vehiculo['City']}")
                        st.write(f"**Estado:** {vehiculo['State']}")
                        st.write(f"**Tipo de Vehículo Eléctrico:** {vehiculo['Electric Vehicle Type']}")

                fig = visualizar_grafo(G, destacados=[vin for vin, _ in vecinos] + [vin_seleccionado])
                st.pyplot(fig)

    query = st.text_input("Buscar vehículos:", "")


    
    if query:
        if 'offset' not in st.session_state:
            st.session_state.offset = 0

        col1, col2 = st.columns(2)
        if col1.button("Anterior") and st.session_state.offset > 0:
            st.session_state.offset -= 6
        if col2.button("Siguiente"):
            st.session_state.offset += 6

        resultados = bfs_vehiculos_similares(G, df_filtrado, query, num_resultados=6, offset=st.session_state.offset)
        
        if resultados:
            st.write(f"Mostrando resultados {st.session_state.offset + 1} - {st.session_state.offset + len(resultados)}")
            mostrar_resultados(df_filtrado, resultados)
        else:
            st.write("No se encontraron más resultados.")
            if st.session_state.offset > 0:
                st.session_state.offset -= 6
    
    else:
        st.error("Los datos no están disponibles.")

if __name__ == "__main__":
    main()