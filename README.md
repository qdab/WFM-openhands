# Excel Schedule Email Notification System

A simple web application for managing schedules from Excel files and sending automated email notifications.

## Features

- Display schedules from Excel/CSV files
- Automatically send email notifications based on schedule
- No external dependencies (uses Python standard library)
- No database required (uses Excel/CSV as data source)
- Simple web interface to view and manage schedules
- Responsive design for mobile and desktop
- Configurable email templates

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository
2. No additional dependencies to install (uses Python standard library)

## Configuration

Edit the `config.py` file to set your:
- SMTP server details
- Email credentials
- Schedule file path
- Web server port

## Usage

1. Start the web server:
   ```
   python app.py
   ```

2. Access the web interface at:
   ```
   http://localhost:12000
   ```

3. Upload or edit your schedule file
4. The system will automatically send notifications based on the schedule

## File Structure

- `app.py`: Main web server application
- `scheduler.py`: Schedule parsing and email notification logic
- `excel_to_csv.py`: Utility to convert Excel files to CSV
- `config.py`: Configuration settings
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
- `sample_schedule.csv`: Example schedule data
