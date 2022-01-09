import json
import csv

def read_dataframe(file_path, delimiter=';'):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=delimiter)
            data = list(csv_reader)
    except Exception as e:
        print(f'Unable to read from {file_path}')
        print(f'Error: {e.message}')
    else:
        return data

def format_to_json(dataframe):
    header = dataframe[0]
    municipios = {}
    municipios["municipios"] = [dict(zip(header, row)) for row in dataframe[1:]]

    return municipios

df = read_dataframe('/Users/kaos/workspace/CICE/municipios/municipios_madrid.csv')
data = format_to_json(df)


with open('data.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)