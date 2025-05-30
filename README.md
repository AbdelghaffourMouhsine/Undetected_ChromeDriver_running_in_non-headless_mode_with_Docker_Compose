# Undetected ChromeDriver Docker Setup

This project provides a Docker setup for running web automation tasks using undetected-chromedriver, which helps bypass bot detection systems.

## Files Included

- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image configuration
- `docker-compose.yml` - Docker Compose configuration
- `uc_script.py` - Example Python script using undetected-chromedriver

## How to Use

1. Make sure Docker and Docker Compose are installed on your system.

2. Build and run the container:
   ```bash
   docker-compose up --build
   ```

3. View the results in the console output. The script will:
   - Launch Chrome with undetected-chromedriver
   - Visit a test website (nowsecure.nl)
   - Take a screenshot
   - Report whether it was detected as a bot

4. Check the `screenshot.png` file after running to see the rendered page.

## Customizing

- Edit `uc_script.py` to implement your own web automation tasks
- Modify the Chrome options in `uc_script.py` to adjust browser behavior
- Uncomment the VNC port in `docker-compose.yml` if you need to see the browser GUI

## Troubleshooting

If you encounter issues:

1. Try removing the `--headless` flag in `uc_script.py` and enable VNC in `docker-compose.yml`
2. Connect to the container with VNC viewer at localhost:5900
3. Check the Chrome version compatibility with your undetected-chromedriver version