#!/usr/bin/env bash

# Navigate to the application directory
cd /home/site/wwwroot

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Start the Twiscope bot
python main.py
