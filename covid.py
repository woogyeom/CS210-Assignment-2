import csv
from collections import Counter, defaultdict
import numpy as np

province_tude_dict = defaultdict(list)

with open('covidTrain.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        province = row['province']
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        province_tude_dict[province].append((float(latitude), float(longitude)))
    
    # print(province_tude_dict)
    
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
            avg_latitude = round((sum_latitude / latitude_count), 2)
        else:
            avg_latitude = 0
        if longitude_count > 0:
            avg_longitude = round((sum_longitude / longitude_count), 2)
        else:
            avg_longitude = 0
        
        province_avg_tude_dict[province].append((avg_latitude, avg_longitude))


    print(province_avg_tude_dict)

    rows = list(reader)
    for row in rows:
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
