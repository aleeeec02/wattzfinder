import pandas as pd
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt



def cargar_datos(file_path):
    try:
        return pd.read_csv(file_path, delimiter=';')
    except Exception as e:
        st.error(f"No se pudieron cargar los datos: {e}")
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

def dijkstra_algo(G, vin_inicio):
    longitudes_camino = nx.single_source_dijkstra_path_length(G, source=vin_inicio, weight='weight')
    carros_ordenados = sorted(longitudes_camino.items(), key=lambda x: x[1])
    return carros_ordenados[1:6]



def main():
    st.title('Wattzfinder: Sistema de Recomendación de Vehículos Eléctricos')
    file_path_datos = '../data/Electric_Vehicle_Population_Data_3000_FINAL.csv'  
    df = cargar_datos(file_path_datos)

    if not df.empty:
        G = construir_grafo(df)
        vin_seleccionado = st.selectbox('Seleccione un VIN de vehículo:', df['VIN (1-10)'].unique())
        if st.button('Buscar vehículos similares'):
            recomendaciones = dijkstra_algo(G, vin_seleccionado)
            st.write("Vehículos recomendados según la similitud en MSRP:")
            for vin, diferencia in recomendaciones:
                st.write(f"VIN: {vin}, Diferencia de MSRP: ${diferencia}")

        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='deepskyblue', edge_color='magenta', node_size=500, ax=ax)
        st.pyplot(fig)

    else:
        st.error("Los datos no están disponibles.")

if __name__ == "__main__":
    main()

