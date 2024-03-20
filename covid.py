import csv
from collections import Counter, defaultdict
import numpy as np

province_tude_dict = defaultdict(list)
province_city_dict = defaultdict(list)
province_symptom_dict = defaultdict(list)

with open('covidTrain.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        province = row['province']
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        province_tude_dict[province].append((float(latitude), float(longitude)))
        if row['city'] != 'NaN':
            province_city_dict[province].append(row['city'])
        if row['symptoms'] != 'NaN':
            symptoms = [symptom.strip() for symptom in row['symptoms'].split(';')]
            province_symptom_dict[province].extend(symptoms)

province_avg_tude_dict = defaultdict(list)
for province, tude_list in province_tude_dict.items():
    sum_latitude = 0
    sum_longitude = 0
    latitude_count = 0
    longitude_count = 0
    for tude in tude_list:
        if not np.isnan(tude[0]):
            sum_latitude += tude[0]
            latitude_count += 1
        if not np.isnan(tude[1]):
            sum_longitude += tude[1]
            longitude_count += 1
    if latitude_count > 0:
        avg_latitude = (sum_latitude / latitude_count)
    else:
        avg_latitude = 0
    if longitude_count > 0:
        avg_longitude = (sum_longitude / longitude_count)
    else:
        avg_longitude = 0
    province_avg_tude_dict[province].append((avg_latitude, avg_longitude))

common_province_city_dict = {}
for province, city in province_city_dict.items():
    city_counter = Counter(city)
    common_city = city_counter.most_common()
    common_city = sorted(common_city, key=lambda x: (-x[1], x[0]))
    if common_city:
        common_province_city_dict[province] = common_city[0][0]

common_province_symptom_dict = {}
for province, symptom in province_symptom_dict.items():
    symptom_counter = Counter(symptom)
    common_symptom = symptom_counter.most_common()
    common_symptom = sorted(common_symptom, key=lambda x: (-x[1], x[0]))
    if common_symptom:
        common_province_symptom_dict[province] = common_symptom[0][0]

with open('covidTrain.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    for row in rows:
        province = row['province']
        if row['age'].__contains__('-'):
            age = round(((int)(row['age'].split('-')[0]) + (int)(row['age'].split('-')[1])) / 2)
        date = row['date_onset_symptoms'].split('.')
        new_date = date[1] + '.' + date[0] + '.' + date[2]
        row['date_onset_symptoms'] = new_date
        date = row['date_admission_hospital'].split('.')
        new_date = date[1] + '.' + date[0] + '.' + date[2]
        row['date_admission_hospital'] = new_date
        date = row['date_confirmation'].split('.')
        new_date = date[1] + '.' + date[0] + '.' + date[2]
        row['date_confirmation'] = new_date
        if row['latitude'] == 'NaN':
            row['latitude'] = round((province_avg_tude_dict[province][0][0]), 2)
        if row['longitude'] == 'NaN':
            row['latitude'] = round((province_avg_tude_dict[province][0][1]), 2)
        if row['city'] == 'NaN':
            row['city'] = common_province_city_dict[province]
        if row['symptoms'] == 'NaN':
            row['symptoms'] = common_province_symptom_dict[province]

with open('covidResult.csv', 'w', newline='') as resultfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(resultfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)