# Download the helper library from https://www.twilio.com/docs/python/install
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from twilio.rest import Client


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


# Define Verify_otp() function
@app.route('/login' , methods=['POST'])
def verify_otp():
    username = request.form['username']
    password = request.form['password']
    mobile_number = request.form['number']

    if username == 'verify' and password == '12345':   
        account_sid = 'AC0a976ad1fea5c227ddd42560d232a152'
        auth_token = 'b0be7ab2a71f15a0bf0ea7ee17cd91f3'
        client = Client(account_sid, auth_token)

        verification = client.verify \
            .services('VAc91dc354e1703023b4f8b5e5d8fcad77') \
            .verifications \
            .create(to=mobile_number, channel='sms')

        print(verification.status)
        return render_template('otp_verify.html')
    else:
        return render_template('user_error.html')



@app.route('/otp', methods=['POST'])
def get_otp():
    print('processing')

    received_otp = request.form['received_otp']
    mobile_number = request.form['number']

    account_sid = 'AC0a976ad1fea5c227ddd42560d232a152'
    auth_token = 'b0be7ab2a71f15a0bf0ea7ee17cd91f3'
    client = Client(account_sid, auth_token)
                                            
    verification_check = client.verify \
        .services('VAc91dc354e1703023b4f8b5e5d8fcad77') \
        .verification_checks \
        .create(to=mobile_number, code=received_otp)
    print(verification_check.status)

    if verification_check.status == "pending":
        return render_template('otp_error.html')
    else:
        return redirect("https://collaborative-notepad.herokuapp.com/")


if __name__ == "__main__":
    app.run()

