import requests
import csv
import sqlite3

api_key = "QLK9QYCKSKF47REC3V5HUNRAG"
cities = ["Vilnius", "Kaunas", "Klaipeda"]
csv_file = 'weather_data.csv'

def fetch_city_weather_data(city):
     
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=us&key={api_key}&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def write_header_to_csv():
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'Max Temperature', 'Min Temperature', 'Humidity', 'Conditions'])  # Header

def write_data_to_csv(data):

    city_name = data['address']
    max_temp = data['days'][0]['tempmax']
    min_temp = data['days'][0]['tempmin']
    humidity = data['days'][0]['humidity']
    conditions = data['days'][0]['conditions']

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        for day in data["days"]:
            writer.writerow([city_name, day['tempmax'], day['tempmin'], day['humidity'], day['conditions']])  # Data

def write_data_to_db(data):

    # Connect to the database
    connect = sqlite3.connect('weather_database.db')
    cursor = connect.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS weather 
    ''')

    # Create the table (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE weather (
            City TEXT,
            MaxTemperature FLOAT,
            MinTemperature FLOAT,
            Humidity FLOAT,
            Conditions TEXT
        )
    ''')
    # Open the CSV file
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Insert data into the table
            cursor.execute('''
                INSERT INTO weather (City, MaxTemperature, MinTemperature, Humidity, Conditions)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['City'], row['Max Temperature'], row['Min Temperature'], row['Humidity'], row['Conditions']))

    # Commit and close the connection
    connect.commit()
    connect.close()
    

def main():
    write_header_to_csv()
    for city in cities:
        data = fetch_city_weather_data(city)
        write_data_to_csv(data)
        write_data_to_db(data)
 
if __name__ == "__main__":
    main()  






