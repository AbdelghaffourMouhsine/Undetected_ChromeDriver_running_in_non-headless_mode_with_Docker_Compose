import undetected_chromedriver as uc
import os
import time
import subprocess
import atexit

# Keep track of processes we started
_started_processes = []

def _cleanup_processes():
    """Clean up any processes we started when the script exits"""
    for process in _started_processes:
        try:
            process.terminate()
        except:
            pass

# Register cleanup function
atexit.register(_cleanup_processes)

def _run_command(command, check_if_running_cmd=None):
    """Run a command and return the process"""
    if check_if_running_cmd:
        try:
            # Check if the process is already running
            result = subprocess.run(check_if_running_cmd, capture_output=True, shell=True)
            if result.returncode == 0 and result.stdout.strip():
                return None
        except Exception:
            pass
    
    try:
        # Start the process
        process = subprocess.Popen(command, shell=True)
        _started_processes.append(process)
        return process
    except Exception:
        return None

def ensure_display_running():
    """Ensure X server and related components are running"""
    # Set DISPLAY environment variable if not set
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':99'
    
    # Check if Xvfb is running
    _run_command(
        "Xvfb :99 -screen 0 1920x1080x24 -ac", 
        "pgrep Xvfb"
    )
    time.sleep(1)
    
    # Check if x11vnc is running
    _run_command(
        "x11vnc -display :99 -forever -nopw -quiet", 
        "pgrep x11vnc"
    )
    
    # Check if fluxbox is running
    _run_command(
        "fluxbox", 
        "pgrep fluxbox"
    )
    time.sleep(0.5)

def create_driver(headless=False, **kwargs):
    """Create an undetected Chrome driver with proper setup for Docker environment"""
    # Ensure display is running first
    ensure_display_running()
    
    # Configure Chrome options
    options = kwargs.pop('options', uc.ChromeOptions())
    
    # Add required arguments for running in Docker
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # Set headless mode explicitly
    options.headless = headless
    
    # Initialize the driver
    driver = uc.Chrome(options=options, **kwargs)
    return driver
