# import requests

# url = 'https://datos.comunidad.madrid/catalogo/dataset/032474a0-bf11-4465-bb92-392052962866/resource/ee750429-1e05-411a-b026-a57ea452a34a/download/municipio_comunidad_madrid.csv'
# response = request.get(url).content.decode()
# response = res.decode('utf-8')
import csv


with open('municipio_comunidad_madrid.csv', encoding='utf8', errors='replace') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        print(row)
    
