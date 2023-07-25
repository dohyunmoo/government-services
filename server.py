from flask import Flask, request, jsonify, make_response
import smtplib
from datetime import datetime, timedelta
import requests
import json

app = Flask(__name__)

# Mock database to hold user and vehicle details
# This is just for demonstration purposes and not suitable for production use
database = {
    "users": [
        {
            "id": 4,
            "firebase_id": "1234gh5",
            "name": "test1",
            "phone_number": "905-333-3333",
            "email": "test@uwaterloo.ca",
            "drivers_licence": "dasjkh"
        },
        {
            "id": 5,
            "firebase_id": "qCarJOpIzVfjU1NpLkiV8Re0clW2",
            "name": "Sarman Test 5",
            "phone_number": "",
            "email": "test5@sarman.com",
            "drivers_licence": "D61044070950228"
        },
        {
            "id": 6,
            "firebase_id": "KXQ8a0w1i9Npchz3lu3Hx8YYA7u1",
            "name": "Sarman Test 6",
            "phone_number": "",
            "email": "test6@sarman.com",
            "drivers_licence": "23hdjskfh7824ej"
        },
        {
            "id": 7,
            "firebase_id": "EpTiMrZijtenURS6BmTpGP5LTq33",
            "name": "Sarman Test 7",
            "phone_number": "",
            "email": "test7@sarman.com",
            "drivers_licence": "halfajksfnjkhearted"
        }
    ],
    "user_vehicle": [
        {
            "user_id": 5,
            "vehicle_id": 6
        },
        {
            "user_id": 5,
            "vehicle_id": 7
        }
    ],
    "vehicles": [
        {
            "id": 6,
            "licence_plate": "Asf",
            "make": "Asf",
            "model": "Asf",
            "year": 0,
            "province": "ontario"
        },
        {
            "id": 7,
            "licence_plate": "Sda",
            "make": "Sda",
            "model": "Sd",
            "year": 2015,
            "province": "ontario"
        },
        {
            "id": 7,
            "licence_plate": "A1B2C3",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2015,
            "province": "ontario"
        }
    ]
}

@app.route('/confirm_user_vehicle', methods=['GET'])
def confirm_user_vehicle():
    data = request.json
    name = data.get('name')
    drivers_licence = data.get('drivers_licence')
    licence_plate = data.get('licence_plate')
    province = data.get('province')
    

    if not licence_plate or not drivers_licence or not name or not province:
        return jsonify({"message": "Bad Request"}), 400

    vehicle = next((v for v in database['vehicles'] if v['licence_plate'] == licence_plate and v['province'] == province), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    pair = next((id for id in database['user_vehicle'] if id['vehicle_id'] == vehicle['id']))
    user = next((u for u in database['users'] if u['id'] == pair['user_id']))
    
    if user["drivers_licence"] != drivers_licence or user["name"] != name:
        return jsonify({"message": "User-Vehicle relationship does not match"}), 404

    return jsonify({"message": "User-Vehicle relationship confirmed"}), 200


@app.route('/create_user_ticket', methods=['POST'])
def create_user_ticket():
    data = request.json
    licence_plate = data.get('licence_plate')
    province = data.get('province')
    cost = data.get('cost')
    type = data.get('type')

    if not licence_plate or not type:
        return jsonify({"message": "Bad Request"}), 400

    vehicle = next((v for v in database['vehicles'] if v['licence_plate'] == licence_plate), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404
    else:
        issue_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        due_date = (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%dT%H:%M:%SZ")

        json_data = {
            "ticket": {
                "licence_plate": licence_plate,
                "province": province,
                "cost": cost,
                "penalty_type": type,
                "issue_date": issue_date,
                "due_date": due_date
            }
        }
        
        res = make_response(jsonify(json_data), 200)
        print("res:",json_data)
        
        API_ENDPOINT = "https://rails-ticket-server-d195e679f8ce.herokuapp.com/api/v1/tickets"
        # API_KEY = ""
        r = requests.post(url=API_ENDPOINT, headers={ "Content-Type" : "application/json" }, json=json_data)
        print(r)
        return res


if __name__ == '__main__':
    app.run(port=5000)
