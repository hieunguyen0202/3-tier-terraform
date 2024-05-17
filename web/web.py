from flask import Flask, render_template, request, redirect, url_for
import requests  # Import requests library to make HTTP requests
import subprocess
import json

app = Flask(__name__)

# Define the URL of the backend server
BACKEND_URL = "http://10.0.3.4:80"  # Replace with the actual IP address of your backend server


def get_instance_metadata(metadata_key):
    metadata_server_url = "http://metadata.google.internal/computeMetadata/v1/instance/"
    headers = {"Metadata-Flavor": "Google"}
    response = requests.get(metadata_server_url + metadata_key, headers=headers)
    return response.text if response.status_code == 200 else None

def get_instance_zone():
    return get_instance_metadata("zone").split('/')[-1]

def get_instance_name():
    return get_instance_metadata("name")



def get_instance_region():
    zone = get_instance_zone()
    region = "-".join(zone.split("-")[:-1])
    return region

@app.route('/')
def index():
    instance_zone = get_instance_zone()
    instance_name = get_instance_name()
    
    instance_region = get_instance_region()
    return render_template('index.html', instance_zone=instance_zone, instance_name=instance_name, instance_region=instance_region)

@app.route('/get-data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        # Retrieve data based on user input ID
        input_id = request.form['input_id']
        
        # Make a GET request to the backend server's API endpoint for retrieving data
        response = requests.post(f"{BACKEND_URL}/api/get-data", json={"input_id": input_id})
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return render_template('data.html', data=data, input_id=input_id)
        else:
            # Handle error response from backend
            return "Error: Unable to retrieve data from the backend server"
    return render_template('get_data.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract data from the form
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phonenumber = request.form['phonenumber']
        password = request.form['password']

        # Make a POST request to the backend server's API endpoint for submitting data
        response = requests.post(f"{BACKEND_URL}/api/submit", json={
            "name": name,
            "email": email,
            "address": address,
            "phonenumber": phonenumber,
            "password": password
        })

        # Check if the request was successful
        if response.status_code == 200:
            return redirect(url_for('index'))  # Redirect to the homepage
        else:
            return "Error: Unable to submit data to the backend server"

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    if request.method == 'POST':
        # Make a POST request to the backend server's API endpoint for deleting data
        response = requests.post(f"{BACKEND_URL}/api/delete/{id}")

        # Check if the request was successful
        if response.status_code == 200:
            return redirect(url_for('get_data'))
        else:
            return "Error: Unable to delete user data from the backend server"
    return render_template('delete.html', id=id)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')