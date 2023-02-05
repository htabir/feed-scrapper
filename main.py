from time import sleep
from bs4 import BeautifulSoup
import csv

import requests
import json

url = 'https://www.feedtables.com/views/ajax'

# extracted the values from the site, told chat gpt to make a map out of them
feed_categories = {
    # 'All': 'All',
    '15': 'Cereal grains',
    '17': 'Cereal byproducts',
    '19': 'Legumes and oilseeds',
    '21': 'Oil byproducts',
    '24': 'Roots and byproducts',
    '26': 'Fruits and byproducts',
    '28': 'Other plant products',
    '30': 'Animal products',
    '32': 'Dairy products',
    '34': 'Oils and fats',
    '36': 'Mineral products',
    '38': 'Amino acids'
}

parameter_category = {
    # 'All': 'All',
    '71': 'Amino acids',
    '10457': 'Environmental impact',
    '72': 'Fatty acids',
    '80': 'Fish',
    '78': 'Horses',
    '69': 'Main constituents',
    '70': 'Mineral elements',
    '74': 'Other parameters',
    '75': 'Pigs',
    '1432': 'Pigs, amino acids',
    '76': 'Poultry',
    '1433': 'Poultry, amino acids',
    '79': 'Rabbits',
    '77': 'Ruminants',
    '73': 'Vitamins and pigments'
}


def scrap_fed():
    for fc in feed_categories:
        for pc in parameter_category:
            # generated in headers.py
            with open('headers.json', 'r') as f:
                headers = json.load(f)

            # generated in body.py
            with open('body.json', 'r') as f:
                body = json.load(f)

            print(f"Grabbing for {feed_categories[fc]} and {parameter_category[pc]}")
            print("=====================================")

            # requesting for data with the headers and body
            response = requests.post(url, headers=headers, data=body)

            # checking if the request was successful
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                return
            else:
                print("Log: Fetching Complete")

                # parsing the response as json
                raw = json.loads(response.text)

                # checking if the data is present
                if len(raw) == 3 and 'data' in raw[2]:
                    data = raw[2]['data']

                    # parsing the data as html with beautiful soup
                    soup = BeautifulSoup(data, 'html.parser')
                    table = soup.find('table', class_='views-table sticky-enabled cols-21')

                    print("Log: Table Found")

                    # extracting the data from the table
                    table_data = []
                    header = [th.text.strip() for th in table.thead.find_all('th')]
                    table_data.append(header)

                    total_row = 0
                    for tr in table.tbody.find_all('tr'):
                        row = [td.text.strip() for td in tr.find_all('td')]
                        if row:
                            total_row += 1
                            table_data.append(row)

                    print(f"Log: {total_row} rows found")

                    # saving the data as csv
                    filename = (f"{feed_categories[fc]}-{parameter_category[pc]}.csv".replace(' ', '_')).lower()
                    with open(f"data/{filename}", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(table_data)
                    print(f"Log: {filename} saved")
                    print("\n")

                else:
                    print("No data")
                    continue

            # sleeping for 5 seconds to avoid getting blocked
            sleep(5)


if __name__ == '__main__':
    scrap_fed()
