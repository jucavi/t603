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
    with open(filepath, 'w', encoding='utf8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)

def get_data():
    try:
        with open(filepath, encoding='utf8') as file:
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

def get_weeks_between(last_day_report_str, day_str):
    week_days = 7
    date_format = '%Y/%m/%d'
    last_day_report = datetime.strptime(last_day_report_str, date_format)
    day_to_predict = datetime.strptime(day_str, date_format)
    return (day_to_predict - last_day_report).days / week_days

data = get_data()['data']
confirmed_per_week = [sum(confirmed) for confirmed in get_key_by_date(data, 'casos_confirmados_totales').values()]
confirmed_per_week.reverse()
# first week starting at 1
# weeks = list(range(1, len(confirmed_per_week) + 1))
weeks = list(range(len(confirmed_per_week)))

cct_std = Std(weeks, confirmed_per_week)
print(f'Gradient: {cct_std.gradient:.1f}')
print(f'Interception: {cct_std.interception:.2f}')
print(f'Confirmed mean: {cct_std.y_mean:.1f}')
print(f'Pearson: {cct_std.r:.4f}')

date1 = '2021/12/31'
date2 = '2020/11/01'
date3 = '2021/02/21'
last_day_report_str = data[0]['fecha_informe'].split()[0]

week_date1 = get_weeks_between(last_day_report_str, date1)
week_date2 = get_weeks_between(last_day_report_str, date2)
week_date3 = get_weeks_between(last_day_report_str, date3)
weeks_to_predict = [cct_std.n + weeks for weeks in (week_date1, week_date2, week_date3)]

predicts_generator = [cct_std.linear_predict(week) for week in weeks_to_predict]

plt.xlabel('Weeks')
plt.ylabel('Accumulated Cases')
for week, predict in zip(weeks_to_predict, predicts_generator):
    plt.scatter(week, predict, label=f'Predict_{week:.0f}_week')
plt.plot(cct_std.x, cct_std.y, label="Accumulated Cases")
plt.plot(cct_std.x, cct_std.linear_predictions, label="Prediction")
plt.show()



tia_by_week = get_key_by_date(data, 'tasa_incidencia_acumulada_ultimos_14dias')
tia_2020 = tia_by_week['2020/12/15']
tia_2021 = tia_by_week['2021/12/14']
tia_zone_2020 = list(range(1, len(tia_2020) + 1))
tia_zone_2021 = list(range(1, len(tia_2021) + 1))

tia_2020_std = Std(tia_zone_2020, tia_2020)
tia_2021_std = Std(tia_zone_2021, tia_2021)
print('Accumulated incidence at 14 days:', tia_2020_std.y_mean)
print('Accumulated incidence at 14 days:', tia_2021_std.y_mean)

plt.xlabel('Zones')
plt.ylabel('Accumulated Incidence')
plt.plot(tia_2020_std.x, tia_2020_std.y, label="Accumulated Incidence 2020")
plt.plot(tia_2021_std.x, tia_2021_std.y, label="Accumulated Incidence 2021")
plt.show()
