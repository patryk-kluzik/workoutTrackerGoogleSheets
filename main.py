import os
from datetime import datetime

import requests

EXERCISE_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'


headers = {
    'x-app-id': os.environ["APP_ID"],
    'x-app-key': os.environ["APP_KEY"],
}

user_input = input("What did you do? ")

params = {
    'query': user_input
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=headers, json=params)


workouts = response.json()

workout_params = [
    {"exercise": workout["name"].title(),
     "duration": workout["duration_min"],
     "calories": workout["nf_calories"]} for workout in workouts["exercises"]]

sheety_params = {
    "workout": {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "time": datetime.now().strftime("%X"),
    }
}

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

auth_header = {
    "Authorization": os.environ["AUTH_HEADER_SHEETY"],
}

print(sheety_params)

for workout in workout_params:
    sheety_params["workout"].update(workout)
    response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, headers=auth_header)
    print(response.text)

