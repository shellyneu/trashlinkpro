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

### Step 2: Update Printer Configuration (if needed)

If your printer is not automatically detected, you may need to update the printer configuration:

1. Open `utils/printer.py`
2. Find the `printer_configs` list in the `connect_printer` method
3. Add your printer's vendor:product ID to the list:

```python
printer_configs = [
    {'idVendor': 0x0fe6, 'idProduct': 0x811e},  # Common thermal printer
    {'idVendor': 0x04b8, 'idProduct': 0x0202},  # Epson
    {'idVendor': 0x28e9, 'idProduct': 0x0289},  # Another common config
    {'idVendor': 0x0519, 'idProduct': 0x0003},  # Another thermal printer
    {'idVendor': 0xYOUR_VENDOR_ID, 'idProduct': 0xYOUR_PRODUCT_ID},  # Your printer
]
```

### Step 3: Test the Printer

Run the printer setup script to test your printer:

```bash
python setup_printer.py
```

This script will:
1. List USB devices
2. Test printer connection
3. Run a test print
4. Print a sample receipt

## Troubleshooting

### Printer Not Found
- Check USB connection
- Ensure printer is powered on
- Try different USB ports
- Check if you need to run with sudo: `sudo python setup_printer.py`

### Permission Denied
Some systems require special permissions to access USB devices:
```bash
sudo python setup_printer.py
```

Or add your user to the appropriate group:
```bash
sudo usermod -a -G lp $USER
sudo usermod -a -G dialout $USER
```

### Paper Issues
- Make sure you're using 58mm thermal paper
- Check paper is loaded correctly
- Ensure paper roll is not empty

### Driver Issues
On some Linux systems, you might need to install printer drivers:
```bash
sudo apt update
sudo apt install printer-driver-all
```

## Receipt Format

The printed receipt will include:
- **Header**: "TRASHLINK PRO" and "Voucher Recycling"
- **User Info**: NIM and Name
- **Bottle Count**: Total bottles recycled
- **Points**: Total points earned (10 points per bottle)
- **Date/Time**: When the receipt was printed
- **Footer**: Environmental message

## Testing

You can test the printer at any time by running:
```bash
python setup_printer.py
```

## Usage in Application

Once configured, the print function will be available in the application:
1. User completes bottle recycling
2. Goes to the end page showing points
3. Clicks "Cetak" (Print) button
4. Confirms print dialog
5. Receipt is printed automatically

## Common Printer IDs for Thermal Printers

Here are some common vendor:product IDs for thermal printers:
- `0fe6:811e` - Common thermal printer
- `04b8:0202` - Epson thermal printer
- `28e9:0289` - Another common thermal printer
- `0519:0003` - Generic thermal printer

If none of these work, use the `find_printer.py` script to identify your specific printer ID.