# WFM-openhands

A simple web application for managing schedules from Excel files and sending automated email notifications.

## Features

- Display schedules from Excel/CSV files
- Automatically send email notifications based on schedule
- No external dependencies (uses Python standard library)
- No database required (uses Excel/CSV as data source)
- Simple web interface to view and manage schedules
- Responsive design for mobile and desktop

## Requirements

- Python 3.6 or higher
- Microsoft Exchange account for sending emails

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/WFM-openhands.git
   cd WFM-openhands
   ```

2. Configure the application:
   - Edit `config.py` to set your SMTP server details and other settings
   - Prepare your Excel schedule file or use the sample CSV provided

3. Convert your Excel file to CSV format (if needed):
   ```
   python excel_to_csv.py your_excel_file.csv
   ```

4. Start the web server:
   ```
   python app.py
   ```

5. Access the web interface:
   - Open your browser and navigate to `http://localhost:12000`

## Schedule File Format

The application expects a CSV file with the following columns:
- Date: The date of the scheduled task (YYYY-MM-DD)
- Time: The time of the scheduled task (HH:MM)
- Employee: The name of the employee
- Task: Description of the scheduled task
- Email: The email address to send notifications to
- NotificationSent: Whether a notification has been sent (Yes/No)

## How It Works

1. The application reads schedule data from the CSV file
2. The web interface displays the schedule in a table
3. A background process checks for upcoming events
4. Email notifications are sent automatically before scheduled events
5. The notification status is updated in the CSV file

## Customization

- Edit `templates/index.html` to customize the web interface
- Modify `config.py` to change email templates and other settings
- Adjust the notification timing in `config.py` (NOTIFICATION_ADVANCE_TIME)

## Running as a Service

To run the application as a background service:

### On Windows:
Use Windows Task Scheduler to run `pythonw app.py` at system startup.

### On Linux:
Create a systemd service file or use cron to start the application at boot.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
