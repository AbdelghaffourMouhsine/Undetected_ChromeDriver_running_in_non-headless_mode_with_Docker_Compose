#!/bin/bash
echo "Starting container environment..."

# Start Xvfb
Xvfb :99 -screen 0 1920x1080x24 -ac &

# Start VNC server
x11vnc -display :99 -forever -nopw -quiet &

# Start a lightweight window manager
fluxbox &

echo "Container is running and ready."
echo "Run scripts with: docker exec -it uc-chrome-container python /app/uc_script.py"

# Keep the container running
tail -f /dev/null
