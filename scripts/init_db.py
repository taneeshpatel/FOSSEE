#!/usr/bin/env python
"""
Initialize the SQLite database for Chemical Equipment Parameter Visualizer.
Run this script to create/update database tables before starting the backend.
Both the web frontend and desktop app use this database via the Django API.
"""
import os
import subprocess
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_root, 'backend')

result = subprocess.call([sys.executable, 'manage.py', 'migrate'], cwd=backend_dir)
sys.exit(result)
