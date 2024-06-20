import pandas as pd
import sys

def convert_excel_to_csv(excel_path):
    try:
        df = pd.read_excel(excel_path)
        
        csv_path = excel_path.replace('.xlsx', '.csv')
        
        df.to_csv(csv_path, index=False)
        print(f"File successfully converted and saved as: {csv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_excel_to_csv.py <path_to_excel_file>")
    else:
        excel_file_path = sys.argv[1]
        convert_excel_to_csv(excel_file_path)
        
