# Printer Setup Guide for Trashlink Pro

This guide will help you set up your Woya 58mm WP58D thermal printer for printing receipts.

## Prerequisites

1. **Connect your printer**: Connect the Woya 58mm WP58D via USB
2. **Power on**: Make sure the printer is powered on
3. **Paper**: Load thermal paper (58mm width)

## Setup Steps

### Step 1: Find Your Printer

Run the printer finder script to identify your printer's USB ID:

```bash
python find_printer.py
```

This will show all USB devices and help identify your printer's vendor:product ID.

# Printer Setup Guide for Trashlink Pro

This guide will help you set up your Woya 58mm WP58D thermal printer for printing receipts.

## Prerequisites

1. **Connect your printer**: Connect the Woya 58mm WP58D via USB
2. **Power on**: Make sure the printer is powered on
3. **Paper**: Load thermal paper (58mm width)

## Setup Steps

### Step 1: Run the USB Setup Script

The easiest way to set up your printer is to run our automated setup script:

```bash
chmod +x setup_usb_linux.sh
sudo ./setup_usb_linux.sh
```

This script will:
- Create USB permissions for your thermal printer
- Add your user to the dialout group
- Reload udev rules automatically

After running this script, **unplug and replug your USB printer** for the changes to take effect.

### Step 2: Verify Printer Connection

Check if your printer is detected:

```bash
lsusb | grep 0fe6
```

You should see output like: `Bus 001 Device 005: ID 0fe6:811e ICS Advent Parallel Adapter`

### Step 3: Update Printer Configuration (if needed)

If your printer is not automatically detected, you may need to update the printer configuration:

1. Open `utils/printer.py`
2. Find the `connect_printer` function
3. Check if your printer's vendor:product ID is supported (default: 0x0fe6:0x811e for Woya 58mm)

### Step 4: Test the Printer

Test your printer connection with Python:

```bash
# Activate virtual environment
source env/bin/activate

# Test printer connection
python -c "
from utils.printer import connect_printer, print_receipt
printer = connect_printer()
if printer:
    print('✅ Printer connected successfully!')
    # Test print
    test_data = {
        'name': 'Test User',
        'bottles': 5,
        'points': 25,
        'timestamp': '2025-01-15 10:30:00'
    }
    print_receipt(test_data)
    print('✅ Test receipt printed!')
else:
    print('❌ Printer connection failed')
"
```

## Troubleshooting

### Printer Not Found
- Check USB connection
- Ensure printer is powered on
- Try different USB ports
- Run the setup script again: `sudo ./setup_usb_linux.sh`
- Reboot after running setup script

### Permission Denied
If you still get permission errors:
```bash
# Make sure setup script was run
sudo ./setup_usb_linux.sh

# Check if user is in dialout group
groups $USER

# Manually add user to groups if needed
sudo usermod -a -G lp,dialout $USER

# Log out and log back in for group changes to take effect
```

### USB Device Not Recognized
Check if your printer has the correct USB ID:
```bash
# List all USB devices
lsusb

# Look for device with ID 0fe6:811e
lsusb | grep 0fe6
```

### Paper Issues
- Make sure you're using 58mm thermal paper
- Check paper is loaded correctly (print side down)
- Ensure paper roll is not empty
- Paper should feed from the bottom of the roll

## Receipt Format

The printed receipt will include:
- **Header**: "TRASHLINK PRO" and logo
- **Divider lines**: Decorative separators
- **User Info**: Name and details
- **Transaction**: Bottle count and points earned
- **Date/Time**: When the receipt was printed
- **Footer**: Thank you message

## Testing

You can test the printer at any time by running the test code above, or by using the main application and completing a recycling transaction.

## Usage in Application

Once configured, the print function will be available in the application:
1. User completes bottle recycling process
2. Goes to the end page showing points earned
3. Clicks "Cetak" (Print) button
4. Receipt is printed automatically with transaction details

## Supported Printer Configuration

The current configuration supports:
- **Vendor ID**: 0x0fe6
- **Product ID**: 0x811e
- **Model**: Woya 58mm WP58D thermal printer
- **Connection**: USB only
- **Paper Width**: 58mm thermal paper
- **Protocol**: ESC/POS commands

If you have a different thermal printer model, you may need to update the vendor/product IDs in `utils/printer.py`.

## Quick Setup Summary

1. Run: `sudo ./setup_usb_linux.sh`
2. Unplug and replug printer
3. Test with the Python command above
4. Start using the application!
````