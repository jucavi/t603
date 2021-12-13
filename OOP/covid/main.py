from std import Std
import requests
import json
import os
import matplotlib.pyplot as plt

url = 'https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/907a2df0-2334-4ca7-aed6-0fa199c893ad/download/covid19_tia_zonas_basicas_salud_s.json'
filename = 'covid.json'
dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, filename)
print(dirname)

if not os.path.isfile(filepath):
    res = requests.get(url).json()
    with open(filepath, 'w') as file:
        json.dump(res, file, indent=4)
        
def get_data():
    try:
        with open(filepath) as file:
            return json.load(file)['data']
    except Exception as e:
        print(e)
        return []

def get_by_date(data):
    result = {}
    for zone in data:
        sdate = zone['fecha_informe'].split(' ')[0]
        value = result.setdefault(sdate, [])
        value.append(zone)
    return result

def confirmed_per_week(data):
    return list(map(lambda key: data[key], sorted(data.keys())))

data = get_data()
data = get_by_date(data)
conf_per_week = confirmed_per_week(data)
total_conf_per_week = [sum(zone['casos_confirmados_totales'] for zone in week) for week in conf_per_week]
weeks = list(range(len(conf_per_week)))

std = Std(weeks, total_conf_per_week)
predicts = [std.predict(week) for week in weeks]

plt.xlabel('Weeks')
plt.ylabel('Acumulated Cases')
plt.plot(weeks, total_conf_per_week, '-b')
plt.plot(weeks, predicts, '-r')
plt.show()

