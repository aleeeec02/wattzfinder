import pandas as pd
import numpy as np
import sys
from datetime import datetime

def main(csv_file):
    df = pd.read_csv(csv_file)
    original_name = csv_file.split('.csv')[0]
    indices_precio_original_cero = df['Base MSRP'] == 0
    non_zero_msrp = df[df['Base MSRP'] != 0]['Base MSRP']
    percentiles = {
        'p10': non_zero_msrp.quantile(0.1),
        'p20': non_zero_msrp.quantile(0.2),
        'p30': non_zero_msrp.quantile(0.3),
        'p40': non_zero_msrp.quantile(0.4),
        'p50': non_zero_msrp.quantile(0.5),
        'p60': non_zero_msrp.quantile(0.6),
        'p70': non_zero_msrp.quantile(0.7),
        'p80': non_zero_msrp.quantile(0.8),
        'p90': non_zero_msrp.quantile(0.9)
    }

    def reemplazar_cero_con_percentiles(row):
        if row['Base MSRP'] == 0:
            percentil_elegido = np.random.choice(list(percentiles.keys()))
            return percentiles[percentil_elegido]
        return row['Base MSRP']

    df['Base MSRP'] = df.apply(reemplazar_cero_con_percentiles, axis=1)
    df['Descuentos'] = 0.0
    discount_percentage = np.random.uniform(8, 40, sum(indices_precio_original_cero)) / 100
    discount_values = (discount_percentage * df.loc[indices_precio_original_cero, 'Base MSRP']).round()
    df.loc[indices_precio_original_cero, 'Descuentos'] = discount_values.astype(int)


    df['Precio Final'] = (df['Base MSRP'] - df['Descuentos']).round()
    df['Precio Final'] = df['Precio Final'].astype(int)
    ahora = datetime.now()
    cadena_fecha_hora = ahora.strftime("%Y-%m-%d_%H%M%S")
    nuevo_nombre_archivo = '{}_modified_{}.csv'.format(original_name, cadena_fecha_hora)
    df.to_csv(nuevo_nombre_archivo, index=False)
    print(f"{nuevo_nombre_archivo} ha sido guardado.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python modify-csv.py <archivoNombre.csv>")
        sys.exit(1)
    main(sys.argv[1])



