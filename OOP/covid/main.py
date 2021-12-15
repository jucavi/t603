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

# def prediction_for_day(data, std_obj, day):
#     week_days = 7
#     date_time = data[0]['fecha_informe']
#     date = date_time.split()[0]
#     last_day = int(date.split('/')[2])
#     return std_obj.linear_predict(std_obj.n + (day - last_day) / week_days)

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
print('t Student:', tia_2020_std.t_statistic(tia_2021_std))


ax1 = plt.subplot(221)
ax1.plot(cct_std.x, cct_std.y, label="Accumulated Cases")
ax1.plot(cct_std.x, cct_std.linear_predictions, label="Prediction")
plt.legend(loc='upper left')


ax2 = plt.subplot(222)
for week, predict in zip(weeks_to_predict, predicts_generator):
    ax2.scatter(week, predict, label=f'Predict_{week:.0f}_week')
plt.legend(loc='upper left')

ax3 = plt.subplot(212)
ax3.plot(tia_2020_std.x, tia_2020_std.y, label="Accumulated Incidence 2020")
ax3.plot(tia_2021_std.x, tia_2021_std.y, label="Accumulated Incidence 2021")
plt.legend(loc='upper left')
plt.show()

