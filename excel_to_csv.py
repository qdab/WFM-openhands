#!/usr/bin/env python3
"""
Utility script to convert Excel files to CSV format.
This script uses Python's csv module and doesn't require external dependencies.

Note: This script assumes the Excel file has been exported to CSV format first.
If you need to directly read .xlsx files, you would need to install openpyxl or a similar library.
"""

import csv
import os
import sys

def convert_excel_to_csv(input_file, output_file=None):
    """
    Convert an Excel CSV export to our application's CSV format.
    
    Args:
        input_file: Path to the input CSV file exported from Excel
        output_file: Path to save the converted CSV file (default: input_file with .csv extension)
    
    Returns:
        Path to the converted CSV file
    """
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + '_converted.csv'
    
    try:
        # Read the input CSV file
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile)
            headers = next(reader)  # Read the header row
            
            # Map Excel headers to our application's headers
            # This is a simple example - adjust based on your Excel format
            header_map = {
                'Date': 'Date',
                'Time': 'Time',
                'Name': 'Employee',
                'Task Description': 'Task',
                'Email Address': 'Email'
            }
            
            # Find indices of required columns
            indices = {}
            for i, header in enumerate(headers):
                for app_header, excel_header in header_map.items():
                    if header.strip() == excel_header:
                        indices[app_header] = i
            
            # Check if all required columns are present
            required_headers = ['Date', 'Time', 'Employee', 'Task', 'Email']
            missing_headers = [h for h in required_headers if h not in indices]
            
            if missing_headers:
                print(f"Error: Missing required columns: {', '.join(missing_headers)}")
                print("Available columns:", ', '.join(headers))
                return None
            
            # Write to the output CSV file
            with open(output_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                
                # Write the header row
                writer.writerow(['Date', 'Time', 'Employee', 'Task', 'Email', 'NotificationSent'])
                
                # Write the data rows
                for row in reader:
                    if len(row) >= max(indices.values()):
                        writer.writerow([
                            row[indices['Date']],
                            row[indices['Time']],
                            row[indices['Employee']],
                            row[indices['Task']],
                            row[indices['Email']],
                            'No'  # Default notification status
                        ])
            
            print(f"Conversion successful. Output saved to {output_file}")
            return output_file
    
    except Exception as e:
        print(f"Error converting Excel to CSV: {e}")
        return None

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python excel_to_csv.py <input_file> [output_file]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_excel_to_csv(input_file, output_file)

if __name__ == "__main__":
    main()