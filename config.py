# Configuration settings

# Web server settings
HOST = '0.0.0.0'  # Allow access from any host
PORT = 12000      # Use the provided port for work-1-evijddjpxojlnogi.prod-runtime.all-hands.dev

# Schedule file settings
SCHEDULE_FILE = 'sample_schedule.csv'
REFRESH_INTERVAL = 300  # Refresh schedule data every 5 minutes

# Email settings for Microsoft Exchange
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_exchange_username'  # Replace with actual credentials
SMTP_PASSWORD = 'your_exchange_password'  # Replace with actual credentials
EMAIL_FROM = 'scheduler@yourcompany.com'  # Replace with actual sender email

# Email notification settings
NOTIFICATION_ADVANCE_TIME = 60  # Send notifications 60 minutes before scheduled time
EMAIL_SUBJECT_TEMPLATE = "Reminder: {task} at {time}"
EMAIL_BODY_TEMPLATE = """
Hello {employee},

This is a reminder that you have a scheduled task:

Task: {task}
Date: {date}
Time: {time}

Best regards,
Automated Scheduler
"""