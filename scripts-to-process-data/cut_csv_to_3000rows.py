import pandas as pd
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python cut_csv.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    df = pd.read_csv(file_path, sep='\t', nrows=3000)
    
    output_path = file_path.replace('.csv', '_cut.csv')
    
    df.to_csv(output_path, index=False)
    
    print(f"File has been cut and saved as: {output_path}")

if __name__ == "__main__":
    main()

