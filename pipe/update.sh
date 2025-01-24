#!/usr/bin/env bash

# Stop the MagicMirror process managed by PM2
pm2 stop MagicMirror

# Change this directory to the directory
cd /home/pi/AzubiReflektor

# Pull main branch for updates
git pull origin main

# update the npm packages
npm install

# Set the DISPLAY environment variable
export DISPLAY=:0

# Start the MagicMirror process using PM2
pm2 start MagicMirror
