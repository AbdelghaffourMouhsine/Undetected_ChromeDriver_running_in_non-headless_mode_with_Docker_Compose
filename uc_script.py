import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pickle
from selenium.common.exceptions import TimeoutException, WebDriverException

# Import our custom utility module
from uc_utils import create_driver

def load_udemy_cookies(driver, cookies_path="cookies/udemy_usmba_account_cookies.pkl"):
        """
        Load Udemy cookies from a saved file
        
        Args:
            cookies_path (str): Path to the cookies file
            
        Returns:
            bool: True if cookies were loaded successfully, False otherwise
        """
        try:
            try:
                driver.get('https://www.udemy.com/')
            except (TimeoutException, WebDriverException) as e:
                print(f"Timeout while loading Udemy homepage: {e}")
                # Try to refresh the page
                try:
                    driver.refresh()
                except Exception:
                    pass
            
            with open(cookies_path, "rb") as file:
                cookies = pickle.load(file)
            
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            driver.refresh()
            if cookies:
                time.sleep(2)  # Wait for the page to load after adding cookies
                # Take a screenshot for verification
                driver.save_screenshot('udemy_cookies_loaded.png')
                while 'www.udemy.com needs to review the security of your connection' in driver.page_source or 'www.udemy.com doit vérifier la sécurité de votre connexion' in driver.page_source:
                    print("Waiting for Udemy to load...")
                    driver.save_screenshot('udemy_cookies_loaded.png')
                    time.sleep(2)
                
                print("Udemy cookies loaded successfully")

            return True
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return False
        
def main():
    print("Starting undetected-chromedriver...")
    
    # Create the driver using our utility function
    driver = create_driver(headless=False, use_subprocess=True)
    
    try:
        print("Navigating to Udemy... and loading cookies")
        load_udemy_cookies(driver)
        print("Successfully loaded Udemy cookies")

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check if we passed the bot detection
        print(f"Page title: {driver.title}")
        page_source = driver.page_source
            
        # Print some info to verify everything is working
        print(f"User-Agent: {driver.execute_script('return navigator.userAgent')}")
        
        # Sleep to keep the container running for testing
        print("Test complete. Waiting 10 seconds before closing...")
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()
        print("Driver closed.")

if __name__ == "__main__":
    main()