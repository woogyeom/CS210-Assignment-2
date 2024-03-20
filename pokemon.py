import csv
from collections import Counter

# 1
with open('pokemonTrain.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    fire_count = 0
    fire_above_40_count = 0

    atk_sum_above_40 = 0
    atk_sum_till_40 = 0
    atk_count_above_40 = 0
    atk_count_till_40 = 0

    def_sum_above_40 = 0
    def_sum_till_40 = 0
    def_count_above_40 = 0
    def_count_till_40 = 0

    hp_sum_above_40 = 0
    hp_sum_till_40 = 0
    hp_count_above_40 = 0
    hp_count_till_40 = 0

    weakness_dict = {}

    for row in reader:
        if row['type'] != 'NaN':
            pokemontype = row['type']
            weakness = row['weakness']
            if pokemontype in weakness_dict:
                weakness_dict[pokemontype].append(weakness)
            else:
                weakness_dict[pokemontype] = [weakness]

            if row['type'] == 'fire':
                fire_count += 1
                if float(row['level']) >= 40:
                    fire_above_40_count += 1

        if float(row['level']) <= 40:
            if row['atk'] != 'NaN':
                atk_sum_till_40 += (float)(row['atk'])
                atk_count_till_40 += 1
            if row['def'] != 'NaN':
                def_sum_till_40 += (float)(row['def'])
                def_count_till_40 += 1
            if row['hp'] != "NaN":
                hp_sum_till_40 += (float)(row['hp'])
                hp_count_till_40 += 1
        else:
            if row['atk'] != 'NaN':
                atk_sum_above_40 += (float)(row['atk'])
                atk_count_above_40 += 1
            if row['def'] != 'NaN':
                def_sum_above_40 += (float)(row['def'])
                def_count_above_40 += 1
            if row['hp'] != "NaN":
                hp_sum_above_40 += (float)(row['hp'])
                hp_count_above_40 += 1

if atk_count_above_40 > 0:
    atk_above_40 = round((atk_sum_above_40 / atk_count_above_40), 1)
else:
    atk_above_40 = 0.0

if atk_count_till_40 > 0:
    atk_till_40 = round((atk_sum_till_40 / atk_count_till_40), 1)
else:
    atk_till_40 = 0.0

if def_count_above_40 > 0:
    def_above_40 = round((def_sum_above_40 / def_count_above_40), 1)
else:
    def_above_40 = 0.0

if def_count_till_40 > 0:
    def_till_40 = round((def_sum_till_40 / def_count_till_40), 1)
else:
    def_till_40 = 0.0

if hp_count_above_40 > 0:
    hp_above_40 = round((hp_sum_above_40 / hp_count_above_40), 1)
else:
    hp_above_40 = 0.0

if hp_count_till_40 > 0:
    hp_till_40 = round((hp_sum_till_40 / hp_count_till_40), 1)
else:
    hp_till_40 = 0.0

if fire_count > 0:
    percent = round((fire_above_40_count / fire_count) * 100)
else:
    percent = 0

with open('pokemon1.txt', 'w') as file:
    file.write(f"Percentage of fire type Pokemons at or above level 40 = {percent}")

# 2 & 3
with open('pokemonTrain.csv', newline='') as csvfile:
    common_weakness_dict = {}
    for pokemontype, weakness in weakness_dict.items():
        weakness_counter = Counter(weakness)
        common_weakness = weakness_counter.most_common(1)
        if common_weakness:
            common_weakness_dict[pokemontype] = common_weakness[0][0]
    print(common_weakness_dict)
    print(f'atk <= 40: {atk_till_40}, atk > 40: {atk_above_40}, def <= 40: {def_till_40}, def > 40: {def_above_40}, hp <= 40: {hp_till_40}, hp > 40: {hp_above_40}')
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    for row in rows:
        if row['type'] == 'NaN':
            for key, val in common_weakness_dict.items():
                if val == row['weakness']:
                    row['type'] = key
        if float(row['level']) <= 40:
            if row['atk'] == 'NaN':
                row['atk'] = atk_till_40
            if row['def'] == 'NaN':
                row['def'] = def_till_40
            if row['hp'] == "NaN":
                row['hp'] = hp_till_40
        else:
            if row['atk'] == 'NaN':
                row['atk'] = atk_above_40
            if row['def'] == 'NaN':
                row['def'] = def_above_40
            if row['hp'] == "NaN":
                row['hp'] = hp_above_40

with open('pokemonResult.csv', 'w', newline='') as resultfile:
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(resultfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 4
type_personality_dict = {}
with open('pokemonResult.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pokemon_type = row['type']
        personality = row['personality']
        if pokemon_type in type_personality_dict:
            type_personality_dict[pokemon_type].append(personality)
        else:
            type_personality_dict[pokemon_type] = [personality]
type_personality_dict = dict(sorted(type_personality_dict.items()))
with open('pokemon4.txt', 'w') as file:
    for pokemon_type, personality in type_personality_dict.items():
        personality.sort()
        file.write(f"{pokemon_type}: {', '.join(personality)}\n")

# 5
stage3_avg_hp = 0
stage3_sum_hp = 0
stage3_count = 0
with open('pokemonResult.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['stage'] == '3.0':
            stage3_sum_hp += (float)(row['hp'])
            stage3_count += 1
    if stage3_count > 0:
        stage3_avg_hp = round(stage3_sum_hp / stage3_count)
    else:
        stage3_avg_hp = 0
with open('pokemon5.txt', 'w') as file:
    file.write(f'Average hit point for Pokemons of stage 3.0 = {stage3_avg_hp}')