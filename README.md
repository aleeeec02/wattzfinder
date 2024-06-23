# wattzfinder


## data to process
### `D:\@USER\wattzfinder\data`
_files inside_

1. Electric_Vehicle_Population_Data_3000_FINAL.csv
   - 3000 rows of data, 19 columns
   - **.csv** tab-limited

2. newColumnsGreen-Electric_Vehicle_Population_Data_modified_2024-04-27_091029.xlsx
    - excel **.xlsx file** with tabs
    - 166 801 rows, 19 columns 
    - green + Base MSRP column modified, Descuentos column, Precio Final column

3. newColumns_Electric_Vehicle_Population_Data_2024-04-27_091029.csv
    - **.csv file** with tabs
    - 166 801 rows, 19 columns
    - each column is separated by different column (not like the just comas on the raw data version)
    - Base MSRP column modified, Descuentos column, Precio Final column

4. rawVisualBlue- Electric_Vehicle_Population_Data.xlsx
    - excel **.xlsx file** with tabs
    - 166 801 rows, 17 columns 
    - blue, raw data, not added columns
    - only purpose is to visualize original raw data orderly
 
5. raw_Electric_Vehicle_Population_Data.csv
    - **.csv file**, comma delimited
    - 166 801 rows, 17 columns
    - file gotten from kaggle, not added columns, original delimitor
    
6. raw_Electric_Vehicle_Population_Data archive.zip'
### `D:\@USER\wattzfinder\data\RAW-Electric_Vehicle_Population_Data archive` 
(gotten from the zip, no modifications, straight from kaggle)

_files inside_
1.  Electric_Vehicle_Population_Data.csv
    - original no modifications at all from kaggle, csv separated by comas
    - 166 801 rows, 17 columns






## scripts to process data
### `D:\@USER\wattzfinder\scripts-to-process-data`
_files inside_

1. add_2NewColumns_modify1Column_csv.py
   - add 2 New columns based on `Base MSRP` column: a. Descuentos b. Precio Final
   - outputs as .csv
   - name: {originalName}_modified_{date-hour}.csv

2. convert_excel_to_csv.py
   - convert a .xlsx file into a .csv
   - use argument as input file
   - outputs as .csv
   - name: {originalName}.csv (only .xlsx entension is changed to .csv)
 
3. cut_csv_to_3000rows.py
    - use pandas to cut until 3000 rows of data
    - select all columns.
    - use argument as input file
    - outputs as tabbed .csv
    - name: {originalName}_cut.csv
  



