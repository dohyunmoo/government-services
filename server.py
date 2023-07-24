from flask import Flask, request, jsonify, make_response
import smtplib
from datetime import datetime
import requests

app = Flask(__name__)

# Mock database to hold user and vehicle details
# This is just for demonstration purposes and not suitable for production use
database = {
    "users": [
        {
            "id": 1,
            "name": "Dohyun Moon",
            "phone": "1234567890",
            "email": "1ml84h2o@gmail.com",
            "drivers_license": "ABC123"
        }
    ],
    "user_vehicle": [
        {
            "user_id": 1,
            "vehicle_id": 1
        }
    ],
    "vehicles": [
        {
            "id": 1,
            "license_plate": "XYZ987",
            "model": "Corolla",
            "make": "Toyota"
        }
    ]
}

@app.route('/confirm_user_vehicle', methods=['GET'])
def confirm_user_vehicle():
    data = request.json
    name = data.get('name')
    drivers_license = data.get('drivers_license')
    license_plate = data.get('license_plate')
    

    if not license_plate or not drivers_license or not name:
        return jsonify({"message": "Bad Request"}), 400

    vehicle = next((v for v in database['vehicles'] if v['license_plate'] == license_plate), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    pair = next((id for id in database['user_vehicle'] if id['vehicle_id'] == vehicle['id']))
    user = next((u for u in database['users'] if u['id'] == pair['user_id']))
    
    if user["drivers_license"] != drivers_license or user["name"] != name:
        return jsonify({"message": "User-Vehicle relationship does not match"}), 404

    return jsonify({"message": "User-Vehicle relationship confirmed"}), 200


@app.route('/create_user_ticket', methods=['POST'])
def create_user_ticket():
    data = request.json
    license_plate = data.get('license_plate')
    type = data.get('type')

    if not license_plate or not type:
        return jsonify({"message": "Bad Request"}), 400

    vehicle = next((v for v in database['vehicles'] if v['license_plate'] == license_plate), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404
    else:
        pair = next((id for id in database['user_vehicle'] if id['vehicle_id'] == vehicle['id']))
        user = next((u for u in database['users'] if u['id'] == pair['user_id']))
        drivers_license = user['drivers_license']
        cost = 100.00

        issue_date = datetime.now()
        due_date = datetime.now() + datetime.timedelta(days=21)

        json_data = {
            "drivers_license": drivers_license,
            "license_plate": license_plate,
            "province": "Ontario",
            "cost": cost,
            "type": type,
            "issue_date": issue_date,
            "due_date": due_date
        }
        
        res = make_response(jsonify(json_data), 200)
        
        API_ENDPOINT = ""
        # API_KEY = ""
        r = requests.post(url=API_ENDPOINT, data=json_data)
        
        return res


if __name__ == '__main__':
    app.run(port=5000)
