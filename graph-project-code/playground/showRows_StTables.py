
import pandas as pd
import streamlit as st


def load_data(filepath):
    try:
        df = pd.read_csv(filepath, delimiter='\t')
        return df
    except Exception as e:
        st.error(f"No se pudieron cargar los datos: {e}")
        return pd.DataFrame()


def main():
    st.title('Wattzfinder: Sistema de recomendación de carros eléctricos basado en algoritmos de grafos')

    data_file_path = '../data/Electric_Vehicle_Population_Data_3000_FINAL.csv'
    df = load_data(data_file_path)

    if not df.empty:
        st.write("Aquí hay una muestra de los datos de vehículos eléctricos:")
        st.write(df.head()) 

        st.write("Datos completos del vehículo eléctrico:")
        st.dataframe(df) 
    else:
        st.write("No hay datos disponibles para mostrar.")


if __name__ == "__main__":
    main()
