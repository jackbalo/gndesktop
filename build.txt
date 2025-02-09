#!/bin/bash

# Exit on any error
set -e  

# Install dependencies
pip install -r requirements.txt  

# Run database migrations
flask db upgrade
