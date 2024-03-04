import requests

url = "http://127.0.0.1:5000/create_user_ticket"

json_data = [
    {
        "licence_plate": "SAT12",
        "province": "ontario",
        "cost": 100,
        "type": "parking",
        "ticket_number": 1,
    },
    {
        "licence_plate": "SAT12",
        "province": "ontario",
        "cost": 150,
        "type": "speeding",
        "ticket_number": 2,
    },
    {
        "licence_plate": "SAT12",
        "province": "ontario",
        "cost": 50,
        "type": "speeding",
        "ticket_number": 3,
    },
    {
        "licence_plate": "SAT12",
        "province": "ontario",
        "cost": 200,
        "type": "redlight",
        "ticket_number": 4,
    }
]

for data in json_data:
    response = requests.post(url, json=data)
    print(data)
    if response.status_code == 200:
        print("Success! Data sent to", url)
        data = response.json()  # Assuming response is JSON format
    else:
        print("Error:", response.status_code)