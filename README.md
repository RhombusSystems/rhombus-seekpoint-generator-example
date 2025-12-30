# Rhombus Custom Seekpoint Generator Example

This example demonstrates how to programmatically create custom seekpoints for Rhombus cameras using the Rhombus API. The script simulates a package scanning system on a conveyor belt, generating seekpoints with carrier-specific information.

## Overview

This Python script showcases:

- Creating custom seekpoints via the Rhombus API
- Generating seekpoints with different colors and metadata
- Simulating a real-world use case (package tracking system)
- Batch posting of multiple seekpoints

## Features

- **Multiple Carriers**: Simulates 5 different shipping carriers (UPS, DHL, FedEx, Amazon, USPS)
- **Color Coding**: Each carrier has a distinct color for easy visual identification
- **Realistic Data**: Generates tracking numbers, customer names, and package details
- **Batch Processing**: Creates and posts ~100 seekpoints in a single API call
- **Time-based Generation**: Distributes seekpoints across a 24-hour period

## Prerequisites

- Python 3.7 or higher
- Rhombus API key
- Camera UUID from your Rhombus system

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RhombusSystems/rhombus-seekpoint-generator-example.git
cd rhombus-seekpoint-generator-example
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API key and camera UUID
```

## Configuration

Create a `.env` file with your credentials:
```env
RHOMBUS_API_KEY=your-api-key-here
RHOMBUS_CAMERA_UUID=your-camera-uuid-here
```

## Usage

Run the script manually:
```bash
python generate_seekpoints.py
```

The script will:
1. Generate ~100 seekpoints for the previous 24-hour period
2. Assign random carriers, tracking numbers, and package details
3. Post all seekpoints to your specified camera via the Rhombus API

## Carrier Configuration

Each carrier has specific attributes:

| Carrier | Color  | Tracking Format |
|---------|--------|----------------|
| UPS     | BLUE   | 1Z + 18 digits |
| DHL     | RED    | DHL + 9 digits |
| FedEx   | PURPLE | FEDEX + 9 digits |
| Amazon  | ORANGE | TBA + 10 digits |
| USPS    | TEAL   | 92XX + 20 digits |

## API Integration

The script uses the following Rhombus API endpoint:
- `POST /api/camera/createCustomFootageSeekpoints`

### Seekpoint Structure

Each seekpoint contains:
```json
{
  "color": "BLUE",
  "name": "UPS",
  "description": "UPS Package Scan | Tracking: 1Z123456... | Customer: John Doe | ...",
  "timestampMs": 1234567890000,
  "displayOverlay": true
}
```

## Customization

You can modify the script to:
- Change the number of seekpoints generated
- Add new carriers or modify existing ones
- Adjust the time range for seekpoint generation
- Customize the description format
- Add additional metadata fields

## Example Output

```
Rhombus Package Scan Seekpoints Generator
============================================================

Generating 100 seekpoints for period:
  From: 2024-01-01 00:00:00 PST
  To: 2024-01-02 00:00:00 PST

Sample of generated seekpoints:
  1. [UPS] 2024-01-01 08:15:23 - UPS Package Scan | Tracking: 1Z123456...
  2. [DHL] 2024-01-01 09:42:11 - DHL Package Scan | Tracking: DHL987654...
  ... and 95 more

Validating seekpoints...
✓ All 100 seekpoints validated successfully

Posting 100 seekpoints to Rhombus API...
✓ Successfully posted 100 seekpoints!
```

## Automation Options

This example can be automated using:
- **Cron jobs** for Linux/Mac systems
- **Task Scheduler** for Windows
- **GitHub Actions** for cloud-based scheduling
- **AWS Lambda** or other serverless platforms

## Security Notes

- Never commit API keys or sensitive credentials to version control
- Use environment variables or secure secret management systems
- Rotate API keys regularly
- Limit API key permissions to only what's necessary

## Support

For questions about the Rhombus API, please refer to:
- [Rhombus API Documentation](https://apidocs.rhombussystems.com)
- [Rhombus Support](https://support.rhombussystems.com)

## License

This example code is provided as-is for demonstration purposes. Feel free to modify and use it according to your needs.

## Contributing

This is an example repository for customer reference. For suggestions or improvements, please contact Rhombus support.
