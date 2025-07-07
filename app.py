#!/usr/bin/env python3
"""
Excel Schedule Email Notification System - Main Web Server
"""

import os
import json
import csv
import threading
import http.server
import socketserver
import urllib.parse
from datetime import datetime
from pathlib import Path

import config
from scheduler import ScheduleManager

# Create directories if they don't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Initialize the schedule manager
schedule_manager = ScheduleManager(config.SCHEDULE_FILE)

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for the web server"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Serve static files
        if parsed_path.path.startswith('/static/'):
            self.path = parsed_path.path
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # Serve the main page
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('templates/index.html', 'r') as file:
                content = file.read()
                
            # Replace placeholders with actual data
            content = content.replace('{{port}}', str(config.PORT))
            
            self.wfile.write(content.encode())
            return
        
        # API endpoint to get schedule data
        if parsed_path.path == '/api/schedule':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            schedule_data = schedule_manager.get_schedule()
            self.wfile.write(json.dumps(schedule_data).encode())
            return
        
        # API endpoint to test email notification
        if parsed_path.path == '/api/test-email':
            query = urllib.parse.parse_qs(parsed_path.query)
            email = query.get('email', [''])[0]
            
            if email:
                success = schedule_manager.send_test_email(email)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'success': success}
                if not success:
                    response['message'] = 'Failed to send test email'
                
                self.wfile.write(json.dumps(response).encode())
                return
            
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Email parameter is required'}).encode())
            return
        
        # Default: return 404
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API endpoint to update schedule
        if parsed_path.path == '/api/schedule':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            schedule_data = json.loads(post_data)
            
            success = schedule_manager.update_schedule(schedule_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'success': success}
            if not success:
                response['message'] = 'Failed to update schedule'
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Default: return 404
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 Not Found')

def start_notification_thread():
    """Start the notification thread"""
    notification_thread = threading.Thread(target=schedule_manager.run_notification_loop)
    notification_thread.daemon = True
    notification_thread.start()

def main():
    """Main function to start the web server"""
    # Create a sample schedule file if it doesn't exist
    if not os.path.exists(config.SCHEDULE_FILE):
        with open(config.SCHEDULE_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Time', 'Event', 'Description', 'Email'])
            writer.writerow([datetime.now().strftime('%Y-%m-%d'), '09:00', 'Meeting', 'Team meeting', 'example@example.com'])
    
    # Start the notification thread
    start_notification_thread()
    
    # Start the web server
    handler = RequestHandler
    httpd = socketserver.TCPServer(("0.0.0.0", config.PORT), handler)
    
    print(f"Server started at http://localhost:{config.PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()