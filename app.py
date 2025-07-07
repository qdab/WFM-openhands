#!/usr/bin/env python3
"""
Main web application for displaying schedules and managing email notifications.
Uses Python's built-in http.server to avoid external dependencies.
"""

import http.server
import socketserver
import json
import os
import threading
import time
from urllib.parse import parse_qs, urlparse
import config
from scheduler import ScheduleManager

# Initialize the schedule manager
schedule_manager = ScheduleManager()

class ScheduleHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the schedule application."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Serve static files
        if path.startswith('/static/'):
            self.path = path
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        # API endpoint to get schedule data as JSON
        elif path == '/api/schedule':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
            self.end_headers()
            
            schedule_data = schedule_manager.get_schedule()
            self.wfile.write(json.dumps(schedule_data).encode())
            return
        
        # Serve the main page for any other path
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('templates/index.html', 'rb') as file:
                self.wfile.write(file.read())
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API endpoint to refresh the schedule
        if path == '/api/refresh':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            success = schedule_manager.refresh_schedule()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
            self.end_headers()
            
            response = {'success': success}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API endpoint to send a test notification
        elif path == '/api/send_test':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_params = parse_qs(post_data.decode())
            
            try:
                index = int(post_params.get('index', ['0'])[0])
                schedule_data = schedule_manager.get_schedule()
                
                if 0 <= index < len(schedule_data):
                    success = schedule_manager.send_notification_email(schedule_data[index])
                else:
                    success = False
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                self.end_headers()
                
                response = {'success': success}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                self.end_headers()
                
                response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
            return
        
        # Default response for unknown endpoints
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())

def start_notification_thread():
    """Start a background thread to process notifications."""
    def notification_worker():
        while True:
            try:
                schedule_manager.process_notifications()
            except Exception as e:
                print(f"Error in notification worker: {e}")
            
            # Sleep for a while before checking again
            time.sleep(60)  # Check every minute
    
    thread = threading.Thread(target=notification_worker, daemon=True)
    thread.start()
    return thread

def main():
    """Start the web server and notification thread."""
    # Create handler with custom directory
    handler = ScheduleHandler
    
    # Start the notification thread
    notification_thread = start_notification_thread()
    
    # Start the web server
    with socketserver.TCPServer((config.HOST, config.PORT), handler) as httpd:
        print(f"Server started at http://{config.HOST}:{config.PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    main()