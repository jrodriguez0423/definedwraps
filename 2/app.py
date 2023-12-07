from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import csv
from datetime import datetime

app = Flask(__name__)

# Configure Flask-Mail for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Use port 465 for SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'definedwraps@gmail.com'
app.config['MAIL_PASSWORD'] = 'jovr epfv ynez vrlc'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get-quote')
def get_quote():
    return render_template('quote_form.html')

@app.route('/apparel')
def apparel():
    return render_template('apparel.html')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    # Get form data
    service_type = request.form.get('serviceType')
    vehicle_make = request.form.get('vehicleMake')
    vehicle_model = request.form.get('vehicleModel')
    name = request.form.get('name')
    number = request.form.get('number')
    email = request.form.get('email')

    try:
        # Prepare email message to send to the service provider
        msg = Message('New Quote Request',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"""
        Service Type: {service_type}
        Vehicle Make: {vehicle_make}
        Vehicle Model: {vehicle_model}
        Name: {name}
        Phone Number: {number}
        Email: {email}
        """

        # Send the email to the service provider
        mail.send(msg)

        # Prepare confirmation email to send to the user
        confirmation_msg = Message('Quote Request Confirmation',
                                    sender=app.config['MAIL_USERNAME'],
                                    recipients=[email])
        confirmation_msg.body = f"""
        Dear {name},

        Thank you for submitting your quote request. We have received the following details:

        Service Type: {service_type}
        Vehicle Make: {vehicle_make}
        Vehicle Model: {vehicle_model}
        Phone Number: {number}

        We will get back to you as soon as possible.

        Best regards,
        Defined Wraps
        """

        # Send the confirmation email to the user
        mail.send(confirmation_msg)

        return render_template('confirmation.html')

    except Exception as e:
        # Log the exception or handle it as you see fit
        print(e)
        return 'There was an issue processing your request. Please try again later.', 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
