import requests
from dotenv import load_dotenv
import os
from apscheduler.schedulers.blocking import BlockingScheduler

# Load environment variables from .env file
load_dotenv()

# Telegram setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(new_ip):
    message = f"Your Raspberry Pi's IP address has changed to {new_ip}"
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}")

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def check_ip_change():
    current_ip = get_public_ip()
    saved_ip = None

    # Read the saved IP if it exists
    if os.path.exists("ip_address.txt"):
        with open("ip_address.txt", "r") as file:
            saved_ip = file.read().strip()

    # Compare IPs
    if current_ip != saved_ip:
        # If there's a change, save the new IP and send a notification
        with open("ip_address.txt", "w") as file:
            file.write(current_ip)
        return current_ip  # Return the new IP for notification
    return None

def job():
    new_ip = check_ip_change()
    if new_ip:
        print(f"IP changed to {new_ip}")
        send_telegram_message(new_ip)
    else:
        print("IP has not changed.")

# Create an instance of BlockingScheduler
scheduler = BlockingScheduler()

# Schedule the job every 60 minutes
scheduler.add_job(job, 'interval', seconds=10)

# Start the scheduler
scheduler.start()