#!/bin/bash

# Navigate to the directory where the app is located
cd /home/nguyenxuanhieu_bd/app

# Update system packages
sudo apt-get update

# Install required packages
sudo apt-get install -y python3-venv

# Set up virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run your Python app app
python app.py