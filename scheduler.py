#!/usr/bin/env python3
"""
Excel Schedule Email Notification System - Schedule Manager
"""

import csv
import time
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

import config

class ScheduleManager:
    """Manages schedule data and sends email notifications"""
    
    def __init__(self, schedule_file):
        """Initialize the schedule manager"""
        self.schedule_file = schedule_file
        self.lock = threading.Lock()
    
    def get_schedule(self):
        """Get the schedule data from the CSV file"""
        schedule = []
        
        with self.lock:
            try:
                with open(self.schedule_file, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        schedule.append(row)
            except Exception as e:
                print(f"Error reading schedule file: {e}")
        
        return schedule
    
    def update_schedule(self, schedule_data):
        """Update the schedule data in the CSV file"""
        with self.lock:
            try:
                with open(self.schedule_file, 'w', newline='') as file:
                    if not schedule_data:
                        writer = csv.writer(file)
                        writer.writerow(['Date', 'Time', 'Event', 'Description', 'Email'])
                        return True
                    
                    fieldnames = schedule_data[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(schedule_data)
                
                return True
            except Exception as e:
                print(f"Error updating schedule file: {e}")
                return False
    
    def send_email(self, to_email, subject, body):
        """Send an email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_FROM
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
            server.starttls()
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_test_email(self, to_email):
        """Send a test email notification"""
        subject = "Test Email from Excel Schedule System"
        body = f"""
        <html>
        <body>
            <h2>Test Email</h2>
            <p>This is a test email from the Excel Schedule Email Notification System.</p>
            <p>Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>If you received this email, the notification system is working correctly.</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body)
    
    def send_event_notification(self, event):
        """Send an event notification email"""
        subject = f"Upcoming Event: {event['Event']}"
        body = f"""
        <html>
        <body>
            <h2>Upcoming Event Reminder</h2>
            <p>You have an upcoming event scheduled:</p>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Event</th>
                    <td>{event['Event']}</td>
                </tr>
                <tr>
                    <th>Date</th>
                    <td>{event['Date']}</td>
                </tr>
                <tr>
                    <th>Time</th>
                    <td>{event['Time']}</td>
                </tr>
                <tr>
                    <th>Description</th>
                    <td>{event['Description']}</td>
                </tr>
            </table>
            <p>This is an automated notification from the Excel Schedule Email Notification System.</p>
        </body>
        </html>
        """
        
        return self.send_email(event['Email'], subject, body)
    
    def check_upcoming_events(self):
        """Check for upcoming events and send notifications"""
        schedule = self.get_schedule()
        now = datetime.now()
        
        for event in schedule:
            try:
                event_date = datetime.strptime(event['Date'], '%Y-%m-%d')
                event_time = datetime.strptime(event['Time'], '%H:%M')
                
                event_datetime = datetime.combine(
                    event_date.date(),
                    event_time.time()
                )
                
                # Check if the event is within the notification window
                time_diff = event_datetime - now
                
                if timedelta(0) <= time_diff <= timedelta(minutes=config.NOTIFICATION_WINDOW_MINUTES):
                    print(f"Sending notification for event: {event['Event']}")
                    self.send_event_notification(event)
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def run_notification_loop(self):
        """Run the notification loop in a separate thread"""
        while True:
            try:
                self.check_upcoming_events()
            except Exception as e:
                print(f"Error in notification loop: {e}")
            
            # Sleep for the check interval
            time.sleep(config.CHECK_INTERVAL_SECONDS)