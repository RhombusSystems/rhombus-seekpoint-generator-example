#!/usr/bin/env python3
"""
Generate random package scan seekpoints for a conveyor belt camera.
Posts ~100 seekpoints to Rhombus API for the previous 24 hours.
"""

import os
import random
import requests
import json
from datetime import datetime, timedelta
import pytz

# API Configuration
API_KEY = os.getenv('RHOMBUS_API_KEY')
CAMERA_UUID = os.getenv('RHOMBUS_CAMERA_UUID')
API_URL = 'https://api2.rhombussystems.com/api/camera/createCustomFootageSeekpoints'
PACIFIC_TZ = pytz.timezone('America/Los_Angeles')

# Carrier configuration
CARRIERS = {
    'UPS': {
        'color': 'BLUE',
        'tracking_prefix': '1Z',
        'tracking_format': lambda: f"1Z{random.randint(100000, 999999)}{random.randint(10, 99)}{random.randint(1000000000, 9999999999)}"
    },
    'DHL': {
        'color': 'RED',
        'tracking_prefix': 'DHL',
        'tracking_format': lambda: f"DHL{random.randint(100000000, 999999999)}"
    },
    'FEDEX': {
        'color': 'PURPLE',
        'tracking_prefix': 'FEDEX',
        'tracking_format': lambda: f"FEDEX{random.randint(100000000, 999999999)}"
    },
    'Amazon': {
        'color': 'ORANGE',
        'tracking_prefix': 'AMZN',
        'tracking_format': lambda: f"TBA{random.randint(1000000000, 9999999999)}"
    },
    'USPS': {
        'color': 'TEAL',
        'tracking_prefix': 'USPS',
        'tracking_format': lambda: f"{random.randint(9200, 9299)}{random.randint(10000000000000000000, 99999999999999999999)}"
    }
}

# Sample data for random generation
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
    'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Sanchez',
    'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams'
]

CITIES = [
    'Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'Fresno',
    'Seattle', 'Portland', 'Las Vegas', 'Phoenix', 'Denver',
    'Chicago', 'New York', 'Boston', 'Miami', 'Atlanta',
    'Dallas', 'Houston', 'Austin', 'Nashville', 'Memphis'
]

PACKAGE_TYPES = [
    'Envelope', 'Small Box', 'Medium Box', 'Large Box', 'Pallet',
    'Tube', 'Mailer', 'Bubble Mailer', 'Flat Rate Box'
]


def generate_customer_name():
    """Generate a random customer name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_tracking_number(carrier_name):
    """Generate a carrier-specific tracking number."""
    carrier = CARRIERS[carrier_name]
    return carrier['tracking_format']()


def generate_package_description(carrier_name, tracking_number, customer_name):
    """Generate a description with package details."""
    package_type = random.choice(PACKAGE_TYPES)
    weight = f"{random.uniform(0.5, 50.0):.1f} lbs"
    destination = random.choice(CITIES)
    
    return (
        f"{carrier_name} Package Scan | "
        f"Tracking: {tracking_number} | "
        f"Customer: {customer_name} | "
        f"Type: {package_type} | "
        f"Weight: {weight} | "
        f"Destination: {destination}"
    )


def calculate_previous_day_range():
    """Calculate the previous 24 hours in Pacific time (midnight to midnight)."""
    now_pacific = datetime.now(PACIFIC_TZ)
    midnight_today = now_pacific.replace(hour=0, minute=0, second=0, microsecond=0)
    midnight_yesterday = midnight_today - timedelta(days=1)
    
    # Convert to epoch milliseconds
    start_ms = int(midnight_yesterday.timestamp() * 1000)
    end_ms = int(midnight_today.timestamp() * 1000)
    
    return start_ms, end_ms, midnight_yesterday, midnight_today


def generate_seekpoints(count=100):
    """Generate random seekpoints for the previous 24 hours."""
    start_ms, end_ms, start_dt, end_dt = calculate_previous_day_range()
    seekpoints = []
    
    print(f"Generating {count} seekpoints for period:")
    print(f"  From: {start_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  To: {end_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()
    
    for _ in range(count):
        # Random timestamp within the 24-hour period
        timestamp_ms = random.randint(start_ms, end_ms)
        
        # Random carrier
        carrier_name = random.choice(list(CARRIERS.keys()))
        carrier_config = CARRIERS[carrier_name]
        
        # Generate data
        tracking_number = generate_tracking_number(carrier_name)
        customer_name = generate_customer_name()
        description = generate_package_description(carrier_name, tracking_number, customer_name)
        
        seekpoint = {
            'color': carrier_config['color'],
            'description': description,
            'displayOverlay': True,
            'name': carrier_name,
            'timestampMs': timestamp_ms
        }
        
        seekpoints.append(seekpoint)
    
    # Sort by timestamp for cleaner output
    seekpoints.sort(key=lambda x: x['timestampMs'])
    
    return seekpoints


def validate_seekpoint(sp):
    """Validate a seekpoint structure."""
    required_fields = ['color', 'description', 'displayOverlay', 'name', 'timestampMs']
    for field in required_fields:
        if field not in sp:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate timestamp is a positive integer
    if not isinstance(sp['timestampMs'], int) or sp['timestampMs'] <= 0:
        raise ValueError(f"timestampMs must be a positive integer, got: {sp['timestampMs']}")
    
    # Validate color is in allowed list
    allowed_colors = ['BLUE', 'RED', 'PURPLE', 'TAN', 'ORANGE', 'TEAL', 'GRAY', 'BLACK']
    if sp['color'] not in allowed_colors:
        raise ValueError(f"Color must be one of {allowed_colors}, got: {sp['color']}")
    
    return True


def post_seekpoints(seekpoints):
    """POST seekpoints to the Rhombus API."""
    # Validate all seekpoints before posting
    print("Validating seekpoints...")
    for i, sp in enumerate(seekpoints):
        try:
            validate_seekpoint(sp)
        except ValueError as e:
            print(f"✗ Validation error for seekpoint {i}: {e}")
            print(f"  Seekpoint data: {json.dumps(sp, indent=2)}")
            return False
    print(f"✓ All {len(seekpoints)} seekpoints validated successfully")
    print()
    
    headers = {
        'Content-Type': 'application/json',
        'x-auth-scheme': 'api-token',
        'x-auth-apikey': API_KEY
    }
    
    payload = {
        'cameraUuid': CAMERA_UUID,
        'footageSeekPoints': seekpoints
    }
    
    print(f"Posting {len(seekpoints)} seekpoints to Rhombus API...")
    print(f"Camera UUID: {CAMERA_UUID}")
    
    # Check if API key is set
    if not API_KEY or API_KEY == '':
        print("⚠ Warning: API key is empty or not set!")
    else:
        print(f"API key: {'*' * (len(API_KEY) - 4)}{API_KEY[-4:]}")  # Show last 4 chars
    print()
    
    try:
        # Debug: Print request details (without sensitive info)
        print(f"Request URL: {API_URL}")
        print(f"Headers: {dict((k, v) for k, v in headers.items() if k != 'x-auth-apikey')}")
        print(f"Payload structure: cameraUuid={payload['cameraUuid']}, {len(payload['footageSeekPoints'])} seekpoints")
        print()
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Print response status
        print(f"Response status: {response.status_code}")
        
        # Try to get response text first
        response_text = response.text
        print(f"Response body: {response_text[:500]}...")  # First 500 chars
        
        # Check status code
        response.raise_for_status()
        
        # Try to parse JSON
        try:
            result = response.json()
            print(f"✓ Successfully posted {len(seekpoints)} seekpoints!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        except json.JSONDecodeError as json_err:
            print(f"⚠ Warning: Response is not valid JSON")
            print(f"Response text: {response_text}")
            # If status was 200, maybe it's still successful?
            if response.status_code == 200:
                print("Status was 200, assuming success despite JSON decode error")
                return True
            return False
        
    except requests.exceptions.HTTPError as http_err:
        print(f"✗ HTTP Error: {http_err}")
        # HTTPError is raised by raise_for_status(), response should be available
        if hasattr(http_err, 'response') and http_err.response is not None:
            print(f"Response status: {http_err.response.status_code}")
            try:
                print(f"Response body: {http_err.response.text}")
            except:
                print("Could not read response body")
        return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False
    except Exception as e:
        print(f"✗ Unexpected Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to generate and post seekpoints."""
    print("=" * 60)
    print("Rhombus Package Scan Seekpoints Generator")
    print("=" * 60)
    print()
    
    # Generate seekpoints
    seekpoints = generate_seekpoints(count=100)
    
    # Print sample of generated seekpoints
    print("Sample of generated seekpoints:")
    for i, sp in enumerate(seekpoints[:5]):
        dt = datetime.fromtimestamp(sp['timestampMs'] / 1000, tz=PACIFIC_TZ)
        print(f"  {i+1}. [{sp['name']}] {dt.strftime('%Y-%m-%d %H:%M:%S')} - {sp['description'][:60]}...")
    print(f"  ... and {len(seekpoints) - 5} more")
    print()
    
    # Post to API
    success = post_seekpoints(seekpoints)
    
    print()
    print("=" * 60)
    if success:
        print("Generation and posting completed successfully!")
        print("=" * 60)
        return 0
    else:
        print("Failed to post seekpoints. Check error messages above.")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    exit(main())

