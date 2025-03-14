import RPi.GPIO as GPIO
import requests
import time
from collections import deque

# Define GPIO to LCD mapping
LCD_RS = 15
LCD_E  = 12
LCD_D4 = 23
LCD_D5 = 21
LCD_D6 = 19
LCD_D7 = 24

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# GPIO Pin configuration
SWITCH2 = 19    # Face Recognition Trigger
SWITCH3 = 21    # System Reset
SWITCH4 = 23    # Emergency Shutdown
BUZZER_PIN = 38
RELAY_PIN = 36

# Server Configuration
SERVER_URL = 'http://192.168.14.20:5000'  # Replace with laptop's IP
CORRECT_PASSWORD = "1234"
MAX_ATTEMPTS = 3
LOCK_DURATION = 300  # Lock duration in seconds (5 minutes)

class SecuritySystem:
    def __init__(self):
        self.face_recognized = False
        self.attempts = 0
        self.system_locked = False
        
        # Setup GPIO
        self.setup_gpio()
        
    
   
    def setup_gpio(self):
        """Configure GPIO pins for the system."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        
        # Button inputs
        GPIO.setup(SWITCH2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SWITCH3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(SWITCH4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Output pins
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        
        # Event detection for buttons
        GPIO.add_event_detect(SWITCH2, GPIO.RISING, 
                               callback=self.on_face_recognition_request, 
                               bouncetime=500)
        GPIO.add_event_detect(SWITCH3, GPIO.RISING, 
                               callback=self.reset_system, 
                               bouncetime=500)
        GPIO.add_event_detect(SWITCH4, GPIO.RISING, 
                               callback=self.emergency_shutdown, 
                               bouncetime=500)
    
    def send_request(self, endpoint, data=None):
        """Send HTTP request to the Flask server."""
        try:
            response = requests.post(f"{SERVER_URL}/{endpoint}", json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return {'status': 'ERROR'}
        except ValueError:
            print("Invalid JSON response from server")
            return {'status': 'ERROR'}
    
    def on_face_recognition_request(self, channel=None):
        """Initiate face recognition process."""
        if self.system_locked:
            print("System is locked. Reset required.")
            return
        
        print("Face recognition request received...")
        response = self.send_request('face_unlock')
        self.handle_server_response(response)
    
    def handle_server_response(self, response):
        """Process server response for authentication."""
        if response.get('status') == 'SUCCESS':
            print("Face recognized successfully!")
            self.trigger_relay()
        elif response.get('status') == 'FAILURE':
            print("Face not recognized.")
            user_choice = input("Retry face recognition? (y/n): ").strip().lower()
            if user_choice == 'y':
                self.on_face_recognition_request()
            else:
                self.initiate_password_auth()
        else:
            print("Unexpected response from server.")
    
    def initiate_password_auth(self):
        """Start password-based authentication."""
        if self.attempts >= MAX_ATTEMPTS:
            self.lock_system()
            return
        
        print("Face not recognized. Requesting password authentication.")
        password = input("Enter password: ")
        self.verify_password(password)
    
    def verify_password(self, password):
        """Verify entered password."""
        if password == CORRECT_PASSWORD:
            print("Password accepted.")
            self.trigger_buzzer(pattern='short')
            self.trigger_relay()
            self.attempts = 0
        else:
            print("Incorrect password.")
            self.attempts += 1
            self.trigger_buzzer(pattern='short')
            
            if self.attempts >= MAX_ATTEMPTS:
                self.lock_system()
    
    def trigger_relay(self):
        """Activate relay for access."""
        print("Access granted. Unlocking ignition...")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(5)  # Keep relay on for 5 seconds
        GPIO.output(RELAY_PIN, GPIO.LOW)
    
    def trigger_buzzer(self, pattern='short'):
        """Activate buzzer with different patterns."""
        if pattern == 'short':
            print("Short buzz for feedback.")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.5)
        elif pattern == 'long':
            print("Long buzz for lock indication.")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(2)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    def reset_system(self, channel=None):
        """Reset system state."""
        print("System reset triggered.")
        self.face_recognized = False
        self.attempts = 0
        self.system_locked = False
        GPIO.output(RELAY_PIN, GPIO.LOW)
    
    def lock_system(self):
        """Lock the system after maximum authentication attempts."""
        print("System locked due to multiple failed attempts.")
        self.system_locked = True
        self.trigger_buzzer(pattern='long')
        
        # Lock for a fixed duration
        print(f"System locked for {LOCK_DURATION // 60} minutes.")
        time.sleep(LOCK_DURATION)
        
        # Automatically reset after lock duration
        self.reset_system()
    
    def emergency_shutdown(self, channel=None):
        """Emergency system shutdown with confirmation."""
        confirmation = input("Are you sure you want to shut down? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            print("Emergency shutdown initiated.")
            GPIO.cleanup()
            exit()
        else:
            print("Emergency shutdown canceled.")
    
    def run(self):
        """Main system run method."""
        try:
            print("Security System Initialized...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.emergency_shutdown()
        finally:
            GPIO.cleanup()

def main():
    security_system = SecuritySystem()
    security_system.run()

if __name__ == "__main__":
    main()
