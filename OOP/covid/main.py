from std import Std
import requests
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

url = 'https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/907a2df0-2334-4ca7-aed6-0fa199c893ad/download/covid19_tia_zonas_basicas_salud_s.json'
filename = 'covid.json'
dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, filename)

if not os.path.isfile(filepath):
    res = requests.get(url).json()
    with open(filepath, 'w') as file:
        json.dump(res, file, indent=4)

def get_data():
    try:
        with open(filepath) as file:
            return json.load(file)
    except Exception:
        return {}

def get_key_by_date(data, key):
    result = {}
    for zone in data:
        sdate = zone['fecha_informe'].split(' ')[0]
        value = result.setdefault(sdate, [])
        value.append(zone[key])
    return result

# def prediction_for_day(data, std_obj, day):
#     week_days = 7
#     date_time = data[0]['fecha_informe']
#     date = date_time.split()[0]
#     last_day = int(date.split('/')[2])
#     return std_obj.linear_predict(std_obj.n + (day - last_day) / week_days)

def prediction_for_day(data, std_obj, day_str):
    week_days = 7
    date_format = '%Y/%m/%d'
    last_date_time_report = data[0]['fecha_informe']
    last_date_report_str = last_date_time_report.split()[0]
    try:
        last_day_report = datetime.strptime(last_date_report_str, date_format)
        day_to_predict = datetime.strptime(day_str, date_format)
        delta = day_to_predict - last_day_report
        if delta.days <= 0:
            raise ValueError
        return std_obj.linear_predict(std_obj.n + delta.days / week_days)
    except Exception as e:
        print('Error:', e)

data = get_data()['data']
confirmed_per_week = [sum(confirmed) for confirmed in get_key_by_date(data, 'casos_confirmados_totales').values()]
confirmed_per_week.reverse()
weeks = list(range(1, len(confirmed_per_week) + 1))

std = Std(weeks, confirmed_per_week)

print(f'Gradient: {std.gradient:.1f}')
print(f'Interception: {std.interception:.2f}')
print(f'Confirmed mean: {std.y_mean:.1f}')
print(f'Pearson: {std.r:.4f}')


plt.xlabel('Weeks')
plt.ylabel('Acumulated Cases')
plt.plot(std.x, std.y, label="Acumulated Cases")
plt.plot(std.x, std.linear_predictions, label="Prediction")
plt.show()

print(prediction_for_day(data, std, '2021/12/31'))
