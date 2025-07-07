#!/usr/bin/env python3
"""
Scheduler module for reading Excel/CSV schedules and sending email notifications.
"""

import csv
import smtplib
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import config

class ScheduleManager:
    def __init__(self, schedule_file=config.SCHEDULE_FILE):
        self.schedule_file = schedule_file
        self.schedule_data = []
        self.last_refresh = None
        self.refresh_schedule()

    def refresh_schedule(self):
        """Read the schedule data from the CSV file."""
        try:
            with open(self.schedule_file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                self.schedule_data = list(reader)
            self.last_refresh = datetime.now()
            print(f"Schedule refreshed at {self.last_refresh}")
            return True
        except Exception as e:
            print(f"Error refreshing schedule: {e}")
            return False

    def get_schedule(self):
        """Return the current schedule data."""
        # Refresh if needed based on the configured interval
        if (self.last_refresh is None or 
            (datetime.now() - self.last_refresh).total_seconds() > config.REFRESH_INTERVAL):
            self.refresh_schedule()
        return self.schedule_data

    def update_notification_status(self, row_index, status="Yes"):
        """Update the notification status in the CSV file."""
        if 0 <= row_index < len(self.schedule_data):
            self.schedule_data[row_index]['NotificationSent'] = status
            
            # Write the updated data back to the CSV
            with open(self.schedule_file, 'w', newline='') as csvfile:
                fieldnames = self.schedule_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.schedule_data)
            return True
        return False

    def get_upcoming_events(self, hours_ahead=24):
        """Get events scheduled within the next specified hours."""
        now = datetime.now()
        upcoming = []
        
        for i, event in enumerate(self.get_schedule()):
            try:
                event_date = datetime.strptime(event['Date'], '%Y-%m-%d')
                event_time = datetime.strptime(event['Time'], '%H:%M').time()
                event_datetime = datetime.combine(event_date.date(), event_time)
                
                # Check if the event is in the future and within the specified time window
                if now <= event_datetime <= now + timedelta(hours=hours_ahead):
                    upcoming.append((i, event))
            except (ValueError, KeyError) as e:
                print(f"Error processing event: {e}")
                
        return upcoming

    def send_notification_email(self, event):
        """Send an email notification for the given event."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_FROM
            msg['To'] = event['Email']
            msg['Subject'] = config.EMAIL_SUBJECT_TEMPLATE.format(
                task=event['Task'],
                time=event['Time']
            )
            
            # Format the email body
            body = config.EMAIL_BODY_TEMPLATE.format(
                employee=event['Employee'],
                task=event['Task'],
                date=event['Date'],
                time=event['Time']
            )
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"Notification sent to {event['Email']} for {event['Task']}")
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

    def process_notifications(self):
        """Check for upcoming events and send notifications if needed."""
        # Get events coming up in the next few hours
        notification_window = config.NOTIFICATION_ADVANCE_TIME / 60  # Convert minutes to hours
        upcoming_events = self.get_upcoming_events(hours_ahead=notification_window)
        
        notifications_sent = 0
        for index, event in upcoming_events:
            # Only send if notification hasn't been sent yet
            if event['NotificationSent'].lower() != 'yes':
                if self.send_notification_email(event):
                    self.update_notification_status(index, "Yes")
                    notifications_sent += 1
        
        return notifications_sent

def run_scheduler():
    """Run the scheduler as a standalone process."""
    scheduler = ScheduleManager()
    
    print("Scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            notifications = scheduler.process_notifications()
            if notifications > 0:
                print(f"Sent {notifications} notifications.")
            
            # Sleep for a while before checking again
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("Scheduler stopped.")

if __name__ == "__main__":
    run_scheduler()