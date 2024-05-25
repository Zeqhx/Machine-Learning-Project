from pywebio.input import input, input_group, FLOAT, select, checkbox
from pywebio.output import put_html
from pywebio import start_server
import numpy as np

import joblib

model = joblib.load('HousePricing.pkl')

html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Predicted House Price</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      h1 {
        color: #333;
        font-size: 3rem;
      }
      p {
        color: #333;
        font-size: 2rem;
      }
      a {
        color: #126bd7;
        text-decoration: none;
        font-size: 1.5rem;
        margin-top: 20px;
      }
      #predictedPrice {
        color: green;
        font-size: 2.5rem;
      }
    </style>
  </head>
  <body>
    <h1>Predicted House Price</h1>
    <p>
      The predicted house price is: <span id="predictedPrice">RM %price%</span>
    </p>
    <a href="">Go back</a>
  </body>
</html>
"""


property_type_dict = {
    "1-sty Terrace/Link House": 0,
    "1.5-sty Terrace/Link House": 1,
    "2-sty Terrace/Link House": 2,
    "2.5-sty Terrace/Link House": 3,
    "3-sty Terrace/Link House": 4,
    "3.5-sty Terrace/Link House": 5,
    "4-sty Terrace/Link House": 6,
    "4.5-sty Terrace/Link House": 7,
    "Apartment": 8,
    "Bungalow": 9,
    "Cluster House": 10,
    "Condominium": 11,
    "Flat": 12,
    "Residential Land": 13,
    "Semi-detached House": 14,
    "Serviced Residence": 15,
    "Townhouse": 16
}

location_dict = {
    "Ampang": 0,
    "Ampang Hilir": 1,
    "Bandar Damai Perdana": 2,
    "Bandar Menjalara": 3,
    "Bandar Tasik Selatan": 4,
    "Bangsar": 5,
    "Bangsar South": 6,
    "Batu Caves": 7,
    "Brickfields": 8,
    "Bukit Bintang": 9,
    "Bukit Jalil": 10,
    "Bukit Tunku (Kenny Hills)": 11,
    "Chan Sow Lin": 12,
    "Cheras": 13,
    "City Centre": 14,
    "Country Heights Damansara": 15,
    "Damansara": 16,
    "Damansara Heights": 17,
    "Desa Pandan": 18,
    "Desa ParkCity": 19,
    "Desa Petaling": 20,
    "Dutamas": 21,
    "Gombak": 22,
    "Jalan Ipoh": 23,
    "Jalan Klang Lama (Old Klang Road)": 24,
    "Jalan Kuching": 25,
    "Jalan Sultan Ismail": 26,
    "Jinjang": 27,
    "KL City": 28,
    "KL Eco City": 29,
    "KL Sentral": 30,
    "KLCC": 31,
    "Kepong": 32,
    "Keramat": 33,
    "Kuchai Lama": 34,
    "Mid Valley City": 35,
    "Mont Kiara": 36,
    "OUG": 37,
    "Pandan Indah": 38,
    "Pandan Jaya": 39,
    "Pandan Perdana": 40,
    "Pantai": 41,
    "Puchong": 42,
    "Rawang": 43,
    "Salak Selatan": 44,
    "Segambut": 45,
    "Sentul": 46,
    "Seputeh": 47,
    "Setapak": 48,
    "Setiawangsa": 49,
    "Sri Hartamas": 50,
    "Sri Petaling": 51,
    "Sungai Besi": 52,
    "Taman Desa": 53,
    "Taman Melawati": 54,
    "Taman Tun Dr Ismail": 55,
    "Titiwangsa": 56,
    "Wangsa Maju": 57,
    "taman cheras perdana": 58
}

furnishing_mapping = {
    'Fully Furnished': (1, 0, 0),
    'Partly Furnished': (0, 1, 0),
    'Unfurnished': (0, 0, 1)
}

property_type_keys = list(property_type_dict.keys())
location_keys = list(location_dict.keys())

full_furnishing = 0
part_furnishing = 0
unfurnishing = 0


def predictPrice():
    form = input_group("House Price Prediction",
            [
            input("Enter the number of bedrooms", name="bedrooms", type=FLOAT, required=True),
            input("Enter the number of bathrooms", name="bathrooms", type=FLOAT, required=True),
            input("Enter the number of House Size in SqFT", name="sqft", type=FLOAT, required=True),
            checkbox("Select Furnishing", options=['Fully Furnished', 'Partly Furnished', 'Unfurnished'], name="furnishing", inline=True, required=True),
            input("Enter the Price per Sqft", name="price_per_sqft", type=FLOAT, required=True),
            select("Select Property Type", options=property_type_keys, name="property_type"),
            input("Enter the number of car parks", name="car_parks", type=FLOAT, required=True),
            select("Select Location", options=location_keys, name="location")
            ])
    bedrooms = form['bedrooms']
    bathrooms = form['bathrooms']
    sqft = form['sqft']
    price_per_sqft = form['price_per_sqft']
    furnishing = form['furnishing'][0]
    car_parks = form['car_parks']
    property_type = property_type_dict[form['property_type']]
    location = location_dict[form['location']]
    full_furnishing, part_furnishing, unfurnishing = furnishing_mapping.get(furnishing, (0, 0, 1))
    X = np.array([[location, bedrooms, bathrooms, car_parks, property_type, sqft, full_furnishing, part_furnishing, unfurnishing, price_per_sqft]])
    price = model.predict(X)
    predicted_price = "{:,.2f}".format(price[0])
    put_html(html.replace("%price%", predicted_price))
    
start_server(predictPrice, port=8080)
