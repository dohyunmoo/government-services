from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Mock database to hold user and vehicle details
# This is just for demonstration purposes and not suitable for production use
database = {
    "users": [
        {
            "name": "Dohyun Moon",
            "email": "1ml84h2o@gmail.com",
            "drivers_license": "ABC123"
        }
    ],
    "vehicles": [
        {
            "license_plate": "XYZ987",
            "user_id": 0  # Index of the user in the "users" list
        }
    ]
}

@app.route('/confirm_user_vehicle', methods=['POST'])
def confirm_user_vehicle():
    data = request.json
    user_email = data.get('user_email')
    license_plate = data.get('license_plate')

    if not user_email or not license_plate:
        return jsonify({"message": "Bad Request"}), 400

    user = next((u for u in database['users'] if u['email'] == user_email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    vehicle = next((v for v in database['vehicles'] if v['license_plate'] == license_plate), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    return jsonify({"message": "User-Vehicle relationship confirmed"}), 200


@app.route('/create_user_ticket', methods=['POST'])
def create_user_ticket():
    data = request.json
    user_email = data.get('user_email')
    license_plate = data.get('license_plate')

    if not user_email or not license_plate:
        return jsonify({"message": "Bad Request"}), 400

    user = next((u for u in database['users'] if u['email'] == user_email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    vehicle = next((v for v in database['vehicles'] if v['license_plate'] == license_plate), None)
    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404

    # Create the ticket in your database (this is just a mock, so we do nothing here)

    # Send email notification to the user
    send_email(user_email, "Ticket Created", "Your ticket has been created.")

    return jsonify({"message": "Ticket created successfully"}), 200


def send_email(to_email, subject, body):
    # This function is used to send emails (mock implementation)
    from_email = "noreply@example.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Mock sending email (display message in console)
    print("Sending email to:", to_email)
    print("Subject:", subject)
    print("Body:", body)
    print("Email sent successfully")


if __name__ == '__main__':
    app.run(port=5000)
