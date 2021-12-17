from std import Std
import requests
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

url = 'https://datos.comunidad.madrid/catalogo/dataset/b3d55e40-8263-4c0b-827d-2bb23b5e7bab/resource/907a2df0-2334-4ca7-aed6-0fa199c893ad/download/covid19_tia_zonas_basicas_salud_s.json'
filename = 'covid.json'
dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, filename)


def download_data():
    res = requests.get(url).json()
    with open(filepath, 'w', encoding='utf8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)
    return res

def get_data():
    try:
        with open(filepath, encoding='utf8') as file:
            return json.load(file)
    except Exception:
        return {}

def fetch_data():
    if os.path.isfile(filepath):
        data = get_data()['data']
        today = datetime.now().date().isoformat()
        last_report = to_iso_format(data[0]['fecha_informe'].split(' ')[0])

        if get_weeks_between(last_report, today) <= 1:
            return data

    data = download_data()
    return data.get('data')



def get_key_by_date(data, key):
    result = {}
    for zone in data:
        sdate = zone['fecha_informe'].split(' ')[0]
        value = result.setdefault(sdate, [])
        value.append(zone[key])
    return result

def to_iso_format(date_str):
    return date_str.replace('/', '-')

def get_weeks_between(last_report_str, day_str_iso):
    week_days = 7
    last_report_iso = to_iso_format(last_report_str)
    last_report = datetime.fromisoformat(last_report_iso)
    day_to_predict = datetime.fromisoformat(day_str_iso)
    return (day_to_predict - last_report).days / week_days

data = fetch_data()

confirmed_per_week = [sum(confirmed) for confirmed in get_key_by_date(data, 'casos_confirmados_totales').values()]
confirmed_per_week.reverse()
weeks = list(range(len(confirmed_per_week)))
# first week starting at 1
# weeks = list(range(1, len(confirmed_per_week) + 1))

cct_std = Std(weeks, confirmed_per_week)
print(f'Gradient: {cct_std.gradient:.1f}')
print(f'Interception: {cct_std.interception:.2f}')
print(f'Confirmed mean: {cct_std.y_mean:.1f}')
print(f'Pearson: {cct_std.r:.4f}')

# for predictions
date1 = '2021-12-31'
date2 = '2020-11-01'
date3 = '2021-02-21'
last_day_report_str = data[0]['fecha_informe'].split()[0]
week_date1 = get_weeks_between(last_day_report_str, date1)
week_date2 = get_weeks_between(last_day_report_str, date2)
week_date3 = get_weeks_between(last_day_report_str, date3)

weeks_to_predict = [cct_std.n + weeks for weeks in (week_date1, week_date2, week_date3)]
predicts_generator = [cct_std.linear_predict(week) for week in weeks_to_predict]

tia_by_week = get_key_by_date(data, 'tasa_incidencia_acumulada_ultimos_14dias')

tia_2020 = tia_by_week['2020/12/15']
tia_2021 = tia_by_week['2021/12/14']

tia_zone_2020 = list(range(1, len(tia_2020) + 1))
tia_2020_std = Std(tia_zone_2020, tia_2020)

tia_zone_2021 = list(range(1, len(tia_2021) + 1))
tia_2021_std = Std(tia_zone_2021, tia_2021)

print('Mean accumulated incidence at 14 days:', tia_2020_std.y_mean)
print('Mean accumulated incidence at 14 days:', tia_2021_std.y_mean)
print('t Student:', tia_2021_std.t_statistic(tia_2020_std))


fig, axs = plt.subplots(1, 2, figsize=(15, 6))
axs[0].set_title("Accumulated Cases / Prediction")
axs[0].plot(cct_std.x, cct_std.y, label="Accumulated Cases")
axs[0].plot(cct_std.x, cct_std.linear_predictions, label="Prediction")

axs[1].set_title("Week prediction for accumulated cases")
for week, predict in zip(weeks_to_predict, predicts_generator):
    axs[1].scatter(week, predict, label=f'Predict_{week:.0f}_week')

for ax in axs.flat:
    ax.set(xlabel='Weeks', ylabel='Cases')
    ax.label_outer()
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(15, 6))
for i, (ax, tia) in enumerate(zip(axs.flat, (tia_2020_std, tia_2021_std))):
    ax.set_title(f'Accumulated Incidence 202{i}')
    ax.plot(tia.x, tia.y, label='Accumulated Incidence 202{i}')

    ax.set(xlabel='Zones', ylabel='Accumulated Incidence')
    ax.label_outer()
plt.show()

fig, axs = plt.subplots(1, 2, figsize=(15, 6))
for i, (ax, tia) in enumerate(zip(axs.flat, (tia_2020_std, tia_2021_std))):
    ax.set_title(f'Accumulated Incidence 202{i}')
    ax.hist(tia.y, bins='auto', label=f'TIA14 202{i}')

    ax.set(xlabel=f'TIA14', ylabel='Probability')
    ax.label_outer()
plt.show()

