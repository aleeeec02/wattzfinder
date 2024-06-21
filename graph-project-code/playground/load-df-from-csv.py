import pandas as pd

pd.set_option('display.max_columns', 19)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)

pd.set_option('display.max_colwidth', None)


file_path = '../data/Electric_Vehicle_Population_Data_3000_FINAL.csv'
df = pd.read_csv(file_path, sep='\t')

print(df)


print("alternative: show all c:<")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

