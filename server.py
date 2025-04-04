from flask import Flask, request, jsonify
from flask_cors import CORS
import assistant  # Importing the voice assistant module
import random
import requests

app = Flask(__name__)
CORS(app)

otp_storage = {}  # Store OTPs temporarily

# Send OTP using Twilio
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
USER_PHONE_NUMBER = "your_phone_number"

def send_otp():
    otp = random.randint(100000, 999999)
    otp_storage["otp"] = otp
    message = f"Your authentication OTP is: {otp}"

    requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        data={"From": TWILIO_PHONE_NUMBER, "To": USER_PHONE_NUMBER, "Body": message}
    )
    return "OTP sent!"

@app.route('/send-otp', methods=['GET'])
def send_otp_route():
    return send_otp()

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    if data.get("otp") == otp_storage.get("otp"):
        return jsonify({"status": "success", "message": "OTP verified!"})
    return jsonify({"status": "failed", "message": "Invalid OTP!"})

@app.route('/execute-command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get("command")

    if command:
        assistant.process_command(command)
        return jsonify({"status": "success", "message": f"Command '{command}' executed"})
    
    return jsonify({"status": "failed", "message": "No command received"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
