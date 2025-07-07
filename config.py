#!/usr/bin/env python3
"""
Excel Schedule Email Notification System - Configuration
"""

# Web server configuration
PORT = 12000

# Schedule file path
SCHEDULE_FILE = 'sample_schedule.csv'

# Email configuration
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'
EMAIL_FROM = 'your_email@example.com'

# Notification configuration
CHECK_INTERVAL_SECONDS = 60  # Check for events every minute
NOTIFICATION_WINDOW_MINUTES = 30  # Send notifications 30 minutes before events