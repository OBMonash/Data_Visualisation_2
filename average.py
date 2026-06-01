import csv
from alive_progress import alive_bar

filename = "Raw data\\players_list_foa_converted.csv"
new_file_path = "rated_player_count.csv"
fields = []
rows = []

# with open(filename, 'r', newline='', encoding='latin-1') as file:
#     file_reader = csv.reader(file)

#     fields = next(file_reader)
#     for row in file_reader:
#         rows.append(row)
    
# for row in rows[:5]:
#     print(f"Player: {row[1]}")
#     print(f"{row[2]} is from {row[4]} plays for {row[5]}")

with open(filename, 'r', encoding='latin-1', newline='') as file:
    dict_reader = csv.DictReader(file)

    fields = dict_reader.fieldnames

    for row in dict_reader:
        # print(row)
        rows.append(row)

    # for field in fields:
    #     print(field)

    # for row in rows[0]:
    #     print(row)

# Load country codes into a dictionary for lookup
country_map = {}
with open('Raw data\\active_country_codes.csv', 'r', newline='') as country_file:
    dict_reader = csv.DictReader(country_file)
    for check_row in dict_reader:
        country_map[check_row['FIDE']] = check_row['Common Name']

# Map FIDE codes to country names
with alive_bar(len(rows), title='Mapping country codes') as bar:
    for row in rows:
        if row['country'] in country_map:
            row['country'] = country_map[row['country']]
        
        if row['country'] == 'United States':
            row['country'] = 'United States of America'

        if row['rating'] == '':
            row['rating'] = '0'
        if row['blitz_rating'] == '':
            row['blitz_rating'] = '0'
        if row['rapid_rating'] == '':
            row['rapid_rating'] = '0'
        bar()

new_fields = ['Country','total_player_count','all_master_player_count', 'titled_female_player_count', 'rating_sum', 'rating_average', 'CM_count', 'FM_count', 'IM_count','GM_count', 'WCM_count', 'WFM_count', 'WIM_count', 'WGM_count', 'population']
new_rows: list[dict] = []
entry_found = False

with alive_bar(len(rows), title='Processing data') as bar:
    for row in rows:
        entry_found = False
        if row['rating'] != '0':
            for new_row in new_rows:
                if row['country'] == new_row['country']:
                    new_row['total_player_count'] += 1
                    if row['title'] != '':
                        new_row['all_master_player_count'] += 1
                        new_row['rating_sum'] += round(float(row['rating']), 3)
                        new_row['rating_average'] = round(new_row['rating_sum'] / new_row['all_master_player_count'], 2)
                        if row['sex'] == 'F':
                            new_row['titled_female_player_count'] += 1

                        if row['title'] == 'CM':
                            new_row['CM_count'] += 1
                        elif row['title'] == 'FM':
                            new_row['FM_count'] += 1
                        elif row['title'] == 'IM':
                            new_row['IM_count'] += 1
                        elif row['title'] == 'GM':
                            new_row['GM_count'] += 1
                        elif row['title'] == 'WCM':
                            new_row['WCM_count'] += 1
                        elif row['title'] == 'WFM':
                            new_row['WFM_count'] += 1
                        elif row['title'] == 'WIM':
                            new_row['WIM_count'] += 1
                        elif row['title'] == 'WGM':
                            new_row['WGM_count'] += 1
                    entry_found = True
        
            if not entry_found:
                new_rows.append({'country': row['country'], 'total_player_count': 1, 'all_master_player_count': 1 if row['title'] != '' else 0, 'titled_female_player_count': 1 if row['sex'] == 'F' and row['title'] != '' else 0, 'rating_sum': float(row['rating']), 'rating_average': float(row['rating']), 'CM_count': 0, 'FM_count': 0, 'IM_count': 0, 'GM_count': 0, 'WCM_count': 0, 'WFM_count': 0, 'WIM_count': 0, 'WGM_count': 0, 'population': 0})
                if row['title'] == 'CM':
                    new_rows[-1]['CM_count'] += 1
                elif row['title'] == 'FM':
                    new_rows[-1]['FM_count'] += 1
                elif row['title'] == 'IM':
                    new_rows[-1]['IM_count'] += 1
                elif row['title'] == 'GM':
                    new_rows[-1]['GM_count'] += 1
                elif row['title'] == 'WCM':
                    new_rows[-1]['WCM_count'] += 1
                elif row['title'] == 'WFM':
                    new_rows[-1]['WFM_count'] += 1
                elif row['title'] == 'WIM':
                    new_rows[-1]['WIM_count'] += 1
                elif row['title'] == 'WGM':
                    new_rows[-1]['WGM_count'] += 1
        bar()

population_dict = {}
with open('Raw data\\geo-population_EN.csv', 'r', newline='', encoding='latin-1') as population_file:
    dict_reader = csv.DictReader(population_file)
    for population_row in dict_reader:
        population_dict[population_row['Country']] = int(population_row['Population'])

country_aliases = {
    'United States': 'United States of America',
    'England': 'United Kingdom',
    'Swaziland': 'eSwatini',
    'Cape Verde': 'Cabo Verde',
    'Ivory Coast': "Côte d'Ivoire",
    'Congo-Kinshasa': 'Dem. Rep. Congo',
    'Equitorial Guinea': 'Eq. Guinea',
    'Chinese Taipei': 'Taiwan',
    'South Sudan': 'S. Sudan',
    'Central African Republic': 'Central African Rep.',
    'Bosnia-Herzegovina': 'Bosnia and Herzegovina',
    'Comoros Islands': 'Comoros',
    'East Timor': 'Timor-Leste',
    'Congo': 'Republic of the Congo',
    'Vatican': 'Vatican City',
}

for new_row in new_rows:
    if new_row['country'] in population_dict:
        new_row['population'] = population_dict[new_row['country']]
    elif new_row['country'] in country_aliases:
        alias = country_aliases[new_row['country']]
        new_row['population'] = population_dict.get(alias, new_row['population'])

for new_row in new_rows:
    if new_row['country'] == 'United States':
        new_row['country'] = 'United States of America'
    elif new_row['country'] == 'England':
        new_row['country'] = 'United Kingdom'
    elif new_row['country'] == 'Swaziland':
        new_row['country'] = 'eSwatini'
    elif new_row['country'] == 'Cape Verde':
        new_row['country'] = 'Cabo Verde'
    elif new_row['country'] == 'Ivory Coast':
        new_row['country'] = "Côte d'Ivoire"
    elif new_row['country'] == 'Congo-Kinshasa':
        new_row['country'] = 'Dem. Rep. Congo'
    elif new_row['country'] == 'Equitorial Guinea':
        new_row['country'] = 'Eq. Guinea'
    elif new_row['country'] == 'Chinese Taipei':
        new_row['country'] = 'Taiwan'
    elif new_row['country'] == 'South Sudan':
        new_row['country'] = 'S. Sudan'
    elif new_row['country'] == 'Central African Republic':
        new_row['country'] = 'Central African Rep.'

# for row in new_rows:
#     print(row)
        
player_sum = 0
for row in new_rows:
    player_sum += row['all_master_player_count']
print(player_sum)

with alive_bar(len(new_rows), title='Creating file') as bar:
    with open(new_file_path, 'w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(new_fields)

        for new_row in new_rows:
            writer.writerow([new_row['country'], new_row['total_player_count'], new_row['all_master_player_count'], new_row['titled_female_player_count'], new_row['rating_sum'], new_row['rating_average'], new_row['CM_count'], new_row['FM_count'], new_row['IM_count'], new_row['GM_count'], new_row['WCM_count'], new_row['WFM_count'], new_row['WIM_count'], new_row['WGM_count'], new_row['population']])
            bar()

print('\nFile created successfully. Output path: ' + new_file_path)
