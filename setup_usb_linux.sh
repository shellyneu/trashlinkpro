#!/bin/bash
# USB Printer Setup for Linux (Linux Mint)

echo "=== USB PRINTER SETUP FOR LINUX ==="

# Create udev rules for thermal printer access
echo "Setting up USB permissions for thermal printers..."

# Create udev rule for Woya 58mm thermal printer
sudo tee /etc/udev/rules.d/99-thermal-printer.rules > /dev/null << 'EOF'
# Woya 58mm Thermal Printer USB Rules
SUBSYSTEM=="usb", ATTR{idVendor}=="0fe6", ATTR{idProduct}=="811e", MODE="0666", GROUP="dialout"
EOF

echo "✓ Created udev rules for Woya 58mm printer"

# Add current user to dialout group
sudo usermod -a -G dialout $USER
echo "✓ User added to dialout group"

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
echo "✓ Udev rules reloaded"

echo -e "\n=== SETUP COMPLETE ==="
echo "Please unplug and replug your USB printer"
echo "Your Woya 58mm printer should now work without sudo!"
